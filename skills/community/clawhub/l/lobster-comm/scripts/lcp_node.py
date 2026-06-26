#!/usr/bin/env python3
"""
LCP/1.1 Node — Production UDP Daemon for Lobster-Comm

Features:
- UDP peer-to-peer messaging over Tailscale
- Ed25519 message signing & verification
- Application-layer ACK with retry (reliable delivery)
- Heartbeat keep-alive (detect peer offline)
- Local control socket (send/check/ack via IPC)
- Inbox/Outbox file persistence
- Duplicate detection (idempotent receive)
- Graceful shutdown

Usage:
    python3 lcp_node.py                    # Start daemon (foreground)
    python3 lcp_node.py --background       # Daemonize (nohup)

Architecture:
    [UDP :9528] ←→ Peer communication (DATA/ACK/HEARTBEAT)
    [Unix socket /tmp/lcp.sock] ←→ Local agent IPC (SEND/CHECK/ACK/STATUS)
"""

import sys
import os
import json
import uuid
import socket
import struct
import threading
import time
import signal
import glob
import logging
from datetime import datetime, timezone, timedelta

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from lcp_crypto import sign_message, verify_message

# ── Config ──────────────────────────────────────────────────────────────
LCP_PORT = 9528
IPC_SOCKET = "/tmp/lcp.sock"
MAGIC = b'LCP1'
MAX_RETRIES = 5
RETRY_BASE_MS = 500       # exponential backoff base
ACK_TIMEOUT_S = 3.0
HEARTBEAT_INTERVAL_S = 30
PEER_TIMEOUT_S = 120       # consider peer offline after this

MY_NAME = "AgentA"
PEER_NAME = "AgentB"
# Tailscale IPs
MY_IP = "100.x.x.x"  # Your Tailscale IP
PEER_IP = "100.y.y.y"  # Peer Tailscale IP

# Directories
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(SKILL_DIR, "data")
INBOX_DIR = os.path.join(DATA_DIR, "inbox")
INBOX_ARCHIVE = os.path.join(DATA_DIR, "inbox_archive")
OUTBOX_DIR = os.path.join(DATA_DIR, "outbox")
SEEN_FILE = os.path.join(DATA_DIR, "seen_ids.json")
PID_FILE = "/tmp/lcp_node.pid"

for d in [INBOX_DIR, INBOX_ARCHIVE, OUTBOX_DIR]:
    os.makedirs(d, exist_ok=True)

# ── Logging ─────────────────────────────────────────────────────────────
LOG_FILE = os.path.join(DATA_DIR, "lcp_node.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("lcp")

# ── Packet Format ───────────────────────────────────────────────────────
# [Magic 4B][Seq 4B][Type 1B][Payload...]
# Type: 0x01=DATA, 0x02=ACK, 0x03=HEARTBEAT

MSG_DATA = 0x01
MSG_ACK = 0x02
MSG_HEARTBEAT = 0x03

seq_counter = 0
seq_lock = threading.Lock()

def next_seq():
    global seq_counter
    with seq_lock:
        seq_counter = (seq_counter + 1) % 0xFFFFFFFF
        return seq_counter

def pack(msg_type, seq, payload=b''):
    return struct.pack('!4sIB', MAGIC, seq, msg_type) + payload

def unpack(data):
    if len(data) < 9:
        return None
    magic, seq, msg_type = struct.unpack('!4sIB', data[:9])
    if magic != MAGIC:
        return None
    return seq, msg_type, data[9:]

# ── Seen IDs (duplicate detection) ─────────────────────────────────────
seen_ids = set()
seen_lock = threading.Lock()
MAX_SEEN = 10000

def load_seen():
    global seen_ids
    try:
        if os.path.exists(SEEN_FILE):
            with open(SEEN_FILE, 'r') as f:
                seen_ids = set(json.load(f))
    except:
        seen_ids = set()

def save_seen():
    with seen_lock:
        # Trim to last MAX_SEEN
        ids = list(seen_ids)[-MAX_SEEN:]
        with open(SEEN_FILE, 'w') as f:
            json.dump(ids, f)

def mark_seen(msg_id):
    with seen_lock:
        seen_ids.add(msg_id)
    # Save periodically (every 50)
    if len(seen_ids) % 50 == 0:
        save_seen()

def is_seen(msg_id):
    with seen_lock:
        return msg_id in seen_ids

# ── Pending ACKs ───────────────────────────────────────────────────────
pending_acks = {}  # seq -> threading.Event
ack_lock = threading.Lock()

# ── Peer Status ─────────────────────────────────────────────────────────
peer_last_seen = 0  # timestamp
peer_status_lock = threading.Lock()

def update_peer_seen():
    global peer_last_seen
    with peer_status_lock:
        peer_last_seen = time.time()

def is_peer_online():
    with peer_status_lock:
        return (time.time() - peer_last_seen) < PEER_TIMEOUT_S

# ── UDP Socket ──────────────────────────────────────────────────────────
udp_sock = None

def init_udp():
    global udp_sock
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind to all interfaces on LCP_PORT
    udp_sock.bind(("0.0.0.0", LCP_PORT))
    udp_sock.settimeout(1.0)  # for clean shutdown
    log.info(f"UDP bound on 0.0.0.0:{LCP_PORT}")

def udp_send_raw(packet, target_ip=PEER_IP):
    try:
        udp_sock.sendto(packet, (target_ip, LCP_PORT))
    except Exception as e:
        log.error(f"UDP send error: {e}")

# ── Reliable Send ───────────────────────────────────────────────────────
def send_message(payload_dict):
    """Sign, pack, send with ACK retry. Returns (success, msg_dict)."""
    tz = timezone(timedelta(hours=8))

    if "id" not in payload_dict:
        payload_dict["id"] = str(uuid.uuid4())
    if "from" not in payload_dict:
        payload_dict["from"] = MY_NAME
    if "to" not in payload_dict:
        payload_dict["to"] = PEER_NAME
    if "timestamp" not in payload_dict:
        payload_dict["timestamp"] = datetime.now(tz).isoformat()

    # Sign
    try:
        signed = sign_message(payload_dict)
    except Exception as e:
        log.error(f"Signing failed: {e}")
        return False, payload_dict

    payload_bytes = json.dumps(signed, ensure_ascii=False).encode('utf-8')
    seq = next_seq()
    packet = pack(MSG_DATA, seq, payload_bytes)

    # Setup ACK event
    ack_event = threading.Event()
    with ack_lock:
        pending_acks[seq] = ack_event

    success = False
    for attempt in range(MAX_RETRIES):
        delay = (RETRY_BASE_MS * (2 ** attempt)) / 1000.0
        udp_send_raw(packet)
        log.info(f"Sent seq={seq} attempt={attempt+1}/{MAX_RETRIES}")

        if ack_event.wait(min(delay, ACK_TIMEOUT_S)):
            success = True
            log.info(f"ACK received for seq={seq}")
            break

    with ack_lock:
        pending_acks.pop(seq, None)

    if success:
        # Save to outbox
        fname = f"msg_{signed['id'][:8]}.json"
        with open(os.path.join(OUTBOX_DIR, fname), 'w', encoding='utf-8') as f:
            json.dump(signed, f, ensure_ascii=False, indent=2)
        log.info(f"Delivered: [{signed.get('type')}] {signed.get('message','')[:60]}")
    else:
        log.warning(f"Failed to deliver seq={seq} after {MAX_RETRIES} attempts")

    return success, signed

# ── UDP Listener ────────────────────────────────────────────────────────
shutdown_flag = threading.Event()

def udp_listener():
    """Main UDP receive loop."""
    while not shutdown_flag.is_set():
        try:
            data, addr = udp_sock.recvfrom(65535)
        except socket.timeout:
            continue
        except OSError:
            break

        parsed = unpack(data)
        if not parsed:
            continue

        seq, msg_type, payload = parsed
        update_peer_seen()

        if msg_type == MSG_ACK:
            with ack_lock:
                ev = pending_acks.get(seq)
                if ev:
                    ev.set()

        elif msg_type == MSG_HEARTBEAT:
            # Reply with ACK to heartbeat
            udp_send_raw(pack(MSG_ACK, seq))
            log.debug(f"Heartbeat from {addr}, replied ACK")

        elif msg_type == MSG_DATA:
            # 1. ACK immediately
            udp_send_raw(pack(MSG_ACK, seq), addr[0])

            # 2. Parse JSON
            try:
                msg = json.loads(payload.decode('utf-8'))
            except json.JSONDecodeError:
                log.warning(f"Invalid JSON from {addr}")
                continue

            msg_id = msg.get("id", "")

            # 3. Duplicate check
            if is_seen(msg_id):
                log.info(f"Duplicate msg {msg_id[:8]}, skipped")
                continue

            # 4. Verify signature
            try:
                if not verify_message(msg):
                    log.warning(f"Invalid signature from {addr}")
                    continue
            except Exception as e:
                log.warning(f"Signature check error: {e}")
                continue

            # 5. Save to inbox
            mark_seen(msg_id)
            fname = f"msg_{msg_id[:8]}.json"
            fpath = os.path.join(INBOX_DIR, fname)
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump(msg, f, ensure_ascii=False, indent=2)

            log.info(f"Received [{msg.get('type')}] from {msg.get('from')}: {msg.get('message','')[:60]}")

# ── Heartbeat Sender ───────────────────────────────────────────────────
def heartbeat_loop():
    """Periodically send heartbeat to peer."""
    while not shutdown_flag.is_set():
        seq = next_seq()
        udp_send_raw(pack(MSG_HEARTBEAT, seq))
        log.debug(f"Heartbeat sent seq={seq}")
        shutdown_flag.wait(HEARTBEAT_INTERVAL_S)

# ── IPC Server (Unix Socket) ──────────────────────────────────────────
def handle_ipc_client(conn):
    """Handle one IPC request from local agent."""
    try:
        raw = conn.recv(65536)
        if not raw:
            return
        req = json.loads(raw.decode('utf-8'))
        cmd = req.get("cmd", "").upper()

        if cmd == "SEND":
            payload = req.get("payload", {})
            ok, msg = send_message(payload)
            resp = {"ok": ok, "id": msg.get("id")}

        elif cmd == "CHECK":
            # List inbox messages (don't archive)
            messages = []
            for fp in sorted(glob.glob(os.path.join(INBOX_DIR, "msg_*.json"))):
                try:
                    with open(fp, 'r', encoding='utf-8-sig') as f:
                        m = json.load(f)
                    m["_filepath"] = fp
                    messages.append(m)
                except:
                    pass
            resp = {"count": len(messages), "messages": messages}

        elif cmd == "ACK":
            # Archive processed messages
            archived = 0
            for fp in glob.glob(os.path.join(INBOX_DIR, "msg_*.json")):
                try:
                    fname = os.path.basename(fp)
                    dst = os.path.join(INBOX_ARCHIVE, fname)
                    os.rename(fp, dst)
                    archived += 1
                except:
                    pass
            resp = {"archived": archived}

        elif cmd == "STATUS":
            inbox_count = len(glob.glob(os.path.join(INBOX_DIR, "msg_*.json")))
            resp = {
                "peer": PEER_NAME,
                "peer_ip": PEER_IP,
                "peer_online": is_peer_online(),
                "peer_last_seen": peer_last_seen,
                "inbox_count": inbox_count,
                "uptime": time.time() - start_time,
            }

        elif cmd == "PING":
            # Send a ping to peer
            ok, msg = send_message({"type": "ping", "message": "ping"})
            resp = {"ok": ok}

        else:
            resp = {"error": f"Unknown command: {cmd}"}

        conn.sendall(json.dumps(resp, ensure_ascii=False).encode('utf-8'))

    except Exception as e:
        try:
            conn.sendall(json.dumps({"error": str(e)}).encode('utf-8'))
        except:
            pass
    finally:
        conn.close()

def ipc_server():
    """Listen on Unix domain socket for local agent commands."""
    if os.path.exists(IPC_SOCKET):
        os.remove(IPC_SOCKET)

    srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    srv.bind(IPC_SOCKET)
    srv.listen(5)
    srv.settimeout(1.0)
    os.chmod(IPC_SOCKET, 0o600)
    log.info(f"IPC listening on {IPC_SOCKET}")

    while not shutdown_flag.is_set():
        try:
            conn, _ = srv.accept()
            threading.Thread(target=handle_ipc_client, args=(conn,), daemon=True).start()
        except socket.timeout:
            continue
        except OSError:
            break

    srv.close()
    if os.path.exists(IPC_SOCKET):
        os.remove(IPC_SOCKET)

# ── IPC Client Helper ──────────────────────────────────────────────────
def ipc_call(cmd, **kwargs):
    """Send command to running daemon via IPC. Returns response dict."""
    req = {"cmd": cmd}
    req.update(kwargs)

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(10.0)
    try:
        sock.connect(IPC_SOCKET)
        sock.sendall(json.dumps(req, ensure_ascii=False).encode('utf-8'))
        raw = sock.recv(1048576)  # 1MB max
        return json.loads(raw.decode('utf-8'))
    finally:
        sock.close()

# ── Lifecycle ───────────────────────────────────────────────────────────
start_time = 0

def write_pid():
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))

def cleanup(_sig=None, _frame=None):
    log.info("Shutting down...")
    shutdown_flag.set()
    save_seen()
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
    if os.path.exists(IPC_SOCKET):
        os.remove(IPC_SOCKET)
    sys.exit(0)

def main():
    global start_time
    start_time = time.time()

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    load_seen()
    write_pid()
    init_udp()

    # Start threads
    threads = [
        threading.Thread(target=udp_listener, name="udp-listener", daemon=True),
        threading.Thread(target=heartbeat_loop, name="heartbeat", daemon=True),
        threading.Thread(target=ipc_server, name="ipc-server", daemon=True),
    ]
    for t in threads:
        t.start()

    log.info(f"LCP/1.1 Node started — {MY_NAME} ({MY_IP}) ↔ {PEER_NAME} ({PEER_IP})")
    log.info(f"UDP port {LCP_PORT} | IPC {IPC_SOCKET} | Heartbeat every {HEARTBEAT_INTERVAL_S}s")

    # Main thread waits
    try:
        while not shutdown_flag.is_set():
            shutdown_flag.wait(1.0)
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="LCP/1.1 Node Daemon")
    p.add_argument("--peer-ip", default=PEER_IP)
    p.add_argument("--my-ip", default=MY_IP)
    p.add_argument("--port", type=int, default=LCP_PORT)
    args = p.parse_args()
    PEER_IP = args.peer_ip
    MY_IP = args.my_ip
    LCP_PORT = args.port
    main()
