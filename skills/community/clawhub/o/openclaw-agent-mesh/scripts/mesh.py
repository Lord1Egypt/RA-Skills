#!/usr/bin/env python3
import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import urllib.request
import uuid
from typing import Any, Dict, List

STATE_DIR = pathlib.Path(os.environ.get("OPENCLAW_AGENT_MESH_DIR", "~/.openclaw/agent-mesh")).expanduser()
IDENTITY_PATH = STATE_DIR / "identity.json"
PRIVATE_KEY_PATH = STATE_DIR / "private_key.pem"
PUBLIC_KEY_PATH = STATE_DIR / "public_key.pem"
PEERS_DIR = STATE_DIR / "peers"
REQ_IN_DIR = STATE_DIR / "requests" / "incoming"
REQ_OUT_DIR = STATE_DIR / "requests" / "outgoing"
MSG_IN_DIR = STATE_DIR / "messages" / "incoming"
MSG_OUT_DIR = STATE_DIR / "messages" / "outgoing"


def ensure_dirs() -> None:
    for p in [STATE_DIR, PEERS_DIR, REQ_IN_DIR, REQ_OUT_DIR, MSG_IN_DIR, MSG_OUT_DIR]:
        p.mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_json(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def save_json(path: pathlib.Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text())


def load_identity() -> Dict[str, Any]:
    if not IDENTITY_PATH.exists():
        raise SystemExit("Identity not initialized. Run: mesh.py init")
    return load_json(IDENTITY_PATH)


def fingerprint_from_public_key_pem(public_key_pem: str) -> str:
    digest = hashlib.sha256(public_key_pem.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def run(cmd: List[str], input_bytes: bytes | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, input=input_bytes, capture_output=True, check=True)


def generate_keypair() -> tuple[bytes, bytes]:
    with tempfile.TemporaryDirectory() as td:
        priv = pathlib.Path(td) / "private.pem"
        pub = pathlib.Path(td) / "public.pem"
        run(["openssl", "genpkey", "-algorithm", "Ed25519", "-out", str(priv)])
        run(["openssl", "pkey", "-in", str(priv), "-pubout", "-out", str(pub)])
        return priv.read_bytes(), pub.read_bytes()


def sign_payload(unsigned_obj: Dict[str, Any]) -> str:
    data = canonical_json(unsigned_obj)
    with tempfile.TemporaryDirectory() as td:
        in_file = pathlib.Path(td) / "data.bin"
        sig_file = pathlib.Path(td) / "sig.bin"
        in_file.write_bytes(data)
        run(["openssl", "pkeyutl", "-sign", "-rawin", "-inkey", str(PRIVATE_KEY_PATH), "-in", str(in_file), "-out", str(sig_file)])
        return base64.b64encode(sig_file.read_bytes()).decode("ascii")


def verify_signature(unsigned_obj: Dict[str, Any], signature_b64: str, public_key_pem: str) -> bool:
    try:
        with tempfile.TemporaryDirectory() as td:
            in_file = pathlib.Path(td) / "data.bin"
            sig_file = pathlib.Path(td) / "sig.bin"
            pub_file = pathlib.Path(td) / "pub.pem"
            in_file.write_bytes(canonical_json(unsigned_obj))
            sig_file.write_bytes(base64.b64decode(signature_b64))
            pub_file.write_text(public_key_pem)
            run(["openssl", "pkeyutl", "-verify", "-rawin", "-pubin", "-inkey", str(pub_file), "-sigfile", str(sig_file), "-in", str(in_file)])
            return True
    except Exception:
        return False


def http_get_json(url: str) -> Dict[str, Any]:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_post_json(url: str, obj: Dict[str, Any]) -> Dict[str, Any]:
    body = json.dumps(obj).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST", headers={"Content-Type": "application/json", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=8) as resp:
        text = resp.read().decode("utf-8") or "{}"
        return json.loads(text)


def cmd_init(args):
    ensure_dirs()
    if IDENTITY_PATH.exists() and not args.force:
        raise SystemExit(f"Identity already exists at {IDENTITY_PATH}. Use --force to replace it.")
    private_pem, public_pem = generate_keypair()
    agent_id = args.agent_id or f"agent-{uuid.uuid4().hex[:12]}"
    public_text = public_pem.decode("utf-8")
    identity = {
        "protocol": "openclaw-agent-mesh/v1",
        "agent_id": agent_id,
        "display_name": args.display_name or agent_id,
        "endpoint": args.endpoint,
        "public_key": public_text,
        "fingerprint": fingerprint_from_public_key_pem(public_text),
        "created_at": now_iso(),
    }
    PRIVATE_KEY_PATH.write_bytes(private_pem)
    PUBLIC_KEY_PATH.write_bytes(public_pem)
    os.chmod(PRIVATE_KEY_PATH, 0o600)
    save_json(IDENTITY_PATH, identity)
    print(json.dumps(identity, indent=2))


def cmd_discovery(args):
    identity = load_identity()
    out = {"ok": True, "protocol": "openclaw-agent-mesh/v1", "agent": {k: identity[k] for k in ["agent_id", "display_name", "endpoint", "public_key", "fingerprint"]}}
    print(json.dumps(out, indent=2))


def cmd_scan(args):
    discovered: List[Dict[str, Any]] = []
    for base in args.url:
        url = base.rstrip("/") + "/agent-mesh/discovery"
        try:
            data = http_get_json(url)
            discovered.append({"url": base, "response": data})
        except Exception as e:
            discovered.append({"url": base, "error": str(e)})
    print(json.dumps(discovered, indent=2))


def peer_path(agent_id: str) -> pathlib.Path:
    return PEERS_DIR / f"{agent_id}.json"


def cmd_request_contact(args):
    identity = load_identity()
    request_id = f"req_{uuid.uuid4().hex}"
    unsigned = {
        "type": "contact_request",
        "request_id": request_id,
        "from": {k: identity[k] for k in ["agent_id", "display_name", "endpoint", "public_key", "fingerprint"]},
        "timestamp": now_iso(),
        "purpose": args.purpose or "request trusted communication",
    }
    payload = dict(unsigned)
    payload["signature"] = sign_payload(unsigned)
    out_path = REQ_OUT_DIR / f"{request_id}.json"
    save_json(out_path, payload)
    if args.send:
        resp = http_post_json(args.send.rstrip("/") + "/agent-mesh/contact-request", payload)
        print(json.dumps({"saved": str(out_path), "response": resp}, indent=2))
    else:
        print(json.dumps(payload, indent=2))


def cmd_receive_contact(args):
    payload = load_json(pathlib.Path(args.file))
    unsigned = {k: v for k, v in payload.items() if k != "signature"}
    sender = payload.get("from", {})
    ok = verify_signature(unsigned, payload.get("signature", ""), sender.get("public_key", ""))
    result = {"verified": ok, "request_id": payload.get("request_id")}
    if ok:
        path = REQ_IN_DIR / f"{payload['request_id']}.json"
        save_json(path, payload)
        result["saved"] = str(path)
    print(json.dumps(result, indent=2))


def cmd_list_requests(args):
    print(json.dumps([load_json(p) for p in sorted(REQ_IN_DIR.glob('*.json'))], indent=2))


def cmd_approve_request(args):
    p = REQ_IN_DIR / f"{args.request_id}.json"
    if not p.exists():
        raise SystemExit("Request not found")
    payload = load_json(p)
    sender = payload["from"]
    peer = {
        "agent_id": sender["agent_id"],
        "display_name": sender.get("display_name"),
        "endpoint": sender.get("endpoint"),
        "public_key": sender["public_key"],
        "fingerprint": sender["fingerprint"],
        "trusted_at": now_iso(),
        "source_request_id": payload["request_id"],
    }
    save_json(peer_path(sender["agent_id"]), peer)
    print(json.dumps(peer, indent=2))


def cmd_reject_request(args):
    p = REQ_IN_DIR / f"{args.request_id}.json"
    if not p.exists():
        raise SystemExit("Request not found")
    p.unlink()
    print(json.dumps({"ok": True, "rejected": args.request_id}, indent=2))


def load_peer(agent_id: str) -> Dict[str, Any]:
    p = peer_path(agent_id)
    if not p.exists():
        raise SystemExit(f"Peer {agent_id} is not trusted")
    return load_json(p)


def cmd_send_message(args):
    identity = load_identity()
    peer = load_peer(args.to)
    message_id = f"msg_{uuid.uuid4().hex}"
    unsigned = {
        "type": "direct_message",
        "message_id": message_id,
        "from": identity["agent_id"],
        "to": args.to,
        "timestamp": now_iso(),
        "body": {"text": args.text},
    }
    payload = dict(unsigned)
    payload["signature"] = sign_payload(unsigned)
    out_path = MSG_OUT_DIR / f"{message_id}.json"
    save_json(out_path, payload)
    if args.send:
        if not peer.get("endpoint"):
            raise SystemExit("Trusted peer has no endpoint")
        resp = http_post_json(peer["endpoint"].rstrip("/") + "/agent-mesh/message", payload)
        print(json.dumps({"saved": str(out_path), "response": resp}, indent=2))
    else:
        print(json.dumps(payload, indent=2))


def cmd_receive_message(args):
    payload = load_json(pathlib.Path(args.file))
    sender_id = payload.get("from")
    peer = load_peer(sender_id)
    unsigned = {k: v for k, v in payload.items() if k != "signature"}
    ok = verify_signature(unsigned, payload.get("signature", ""), peer["public_key"])
    result = {"verified": ok, "message_id": payload.get("message_id")}
    if ok:
        path = MSG_IN_DIR / f"{payload['message_id']}.json"
        save_json(path, payload)
        result["saved"] = str(path)
        result["ack"] = {"type": "ack", "message_id": payload["message_id"], "status": "received", "timestamp": now_iso()}
    print(json.dumps(result, indent=2))


def cmd_list_messages(args):
    print(json.dumps([load_json(p) for p in sorted(MSG_IN_DIR.glob('*.json'))], indent=2))


def build_parser():
    parser = argparse.ArgumentParser(description="OpenClaw Agent Mesh V1")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("init"); p.add_argument("--agent-id"); p.add_argument("--display-name"); p.add_argument("--endpoint", required=True); p.add_argument("--force", action="store_true"); p.set_defaults(func=cmd_init)
    p = sub.add_parser("discovery"); p.set_defaults(func=cmd_discovery)
    p = sub.add_parser("scan"); p.add_argument("url", nargs="+"); p.set_defaults(func=cmd_scan)
    p = sub.add_parser("request-contact"); p.add_argument("--purpose"); p.add_argument("--send"); p.set_defaults(func=cmd_request_contact)
    p = sub.add_parser("receive-contact"); p.add_argument("file"); p.set_defaults(func=cmd_receive_contact)
    p = sub.add_parser("list-requests"); p.set_defaults(func=cmd_list_requests)
    p = sub.add_parser("approve-request"); p.add_argument("request_id"); p.set_defaults(func=cmd_approve_request)
    p = sub.add_parser("reject-request"); p.add_argument("request_id"); p.set_defaults(func=cmd_reject_request)
    p = sub.add_parser("send-message"); p.add_argument("--to", required=True); p.add_argument("--text", required=True); p.add_argument("--send", action="store_true"); p.set_defaults(func=cmd_send_message)
    p = sub.add_parser("receive-message"); p.add_argument("file"); p.set_defaults(func=cmd_receive_message)
    p = sub.add_parser("list-messages"); p.set_defaults(func=cmd_list_messages)
    return parser


if __name__ == "__main__":
    ensure_dirs()
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
