#!/usr/bin/env python3
"""
LoRa CAD Monitor — reads LilyGo serial output
• Logs hits to lora_scan.log
• Immediately alerts on real LoRa packets (# PACKET line)
• 15-min reports via REPORT_START/END blocks
• Alerts delivered via lora_alert.txt → OpenClaw cron → Telegram
"""

import serial
import time
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, '/home/admin/.openclaw/workspace')
from lora_decoder import decode_packet, format_decoded

SERIAL_PORT = '/dev/ttyACM0'
BAUD        = 115200
LOG_FILE    = '/home/admin/.openclaw/workspace/lora_scan.log'
HITS_FILE   = '/home/admin/.openclaw/workspace/lora_hits.json'
ALERT_FILE  = '/home/admin/.openclaw/workspace/lora_alert.txt'

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')

def send_alert(msg):
    """Write alert file — OpenClaw cron picks it up and sends Telegram"""
    with open(ALERT_FILE, 'w') as f:
        f.write(msg)
    log(f"ALERT → {msg[:100]}")

def fmt_freq(hz):
    return f"{int(hz)/1e6:.3f} MHz"

def parse_packet_line(line):
    """
    Parse: # PACKET freq,bw,sf,rssi,snr,len,HEXDATA
    Returns dict or None
    """
    try:
        rest = line.replace('# PACKET ', '').strip()
        parts = rest.split(',', 6)
        if len(parts) < 7:
            return None
        return {
            'freq':    int(parts[0]),
            'bw':      int(parts[1]),
            'sf':      int(parts[2]),
            'rssi':    int(parts[3]),
            'snr':     int(parts[4]),
            'len':     int(parts[5]),
            'hex':     parts[6].strip(),
        }
    except Exception as e:
        log(f"PACKET parse error: {e} — {line}")
        return None

def hex_to_ascii(hex_str):
    """Convert hex string to ASCII with dots for non-printable"""
    result = ''
    for i in range(0, len(hex_str)-1, 2):
        try:
            b = int(hex_str[i:i+2], 16)
            result += chr(b) if 32 <= b < 127 else '.'
        except:
            pass
    return result

def format_hex_dump(hex_str, bytes_per_row=8):
    """Format hex string as multi-line dump"""
    rows = []
    for i in range(0, len(hex_str), bytes_per_row*2):
        chunk = hex_str[i:i+bytes_per_row*2]
        pairs = [chunk[j:j+2] for j in range(0, len(chunk), 2)]
        rows.append(' '.join(pairs))
    return rows

def build_packet_alert(pkt):
    """Build immediate Telegram alert for a real LoRa packet"""
    hex_rows = format_hex_dump(pkt['hex'])
    ascii_str = hex_to_ascii(pkt['hex'])

    lines = [
        f"🎯 LoRa PACKET CAUGHT!",
        f"",
        f"📻 {fmt_freq(pkt['freq'])}  BW={pkt['bw']//1000}kHz  SF{pkt['sf']}",
        f"📶 RSSI: {pkt['rssi']} dBm  SNR: {pkt['snr']:+d} dB",
        f"📦 Length: {pkt['len']} bytes",
        f"",
        f"HEX dump:",
    ]
    for row in hex_rows:
        lines.append(f"  {row}")
    if ascii_str.strip('.'):
        lines.append(f"")
        lines.append(f"ASCII: {ascii_str}")

    return '\n'.join(lines)

def parse_report(lines):
    hits = []
    for line in lines:
        line = line.strip()
        if line.startswith('#') or not line:
            continue
        parts = line.split(',')
        # NEW/OLD, PKT/CAD, freq, bw, sf, rssi_min, rssi_max, cad_count, pkt_count
        if len(parts) < 7:
            continue
        try:
            hits.append({
                'flag':      parts[0],
                'type':      parts[1] if len(parts) >= 9 else 'CAD',
                'freq':      int(parts[2] if len(parts) >= 9 else parts[2]),
                'bw':        int(parts[3] if len(parts) >= 9 else parts[3]),
                'sf':        int(parts[4] if len(parts) >= 9 else parts[4]),
                'rssi_min':  int(parts[5] if len(parts) >= 9 else parts[5]),
                'rssi_max':  int(parts[6] if len(parts) >= 9 else parts[6]),
                'cad_count': int(parts[7]) if len(parts) >= 9 else int(parts[7] if len(parts)>7 else 0),
                'pkt_count': int(parts[8]) if len(parts) >= 9 else 0,
            })
        except Exception as e:
            log(f"Report parse error: {e} — {line}")
    return hits

def build_report_alert(hits, pass_num, total_cad, total_pkt):
    new_hits = [h for h in hits if h['flag'] == 'NEW']
    pkt_hits = [h for h in hits if h['pkt_count'] > 0]

    lines = [f"📡 LoRa CAD Report — Pass {pass_num}"]
    lines.append(f"CAD hits: {total_cad}  |  Real packets: {total_pkt}")
    lines.append(f"Unique channels: {len(hits)}")

    if pkt_hits:
        lines.append(f"\n🎯 Channels with real packets:")
        for h in pkt_hits:
            lines.append(
                f"  📦 {fmt_freq(h['freq'])}  BW={h['bw']//1000}kHz  SF{h['sf']}"
                f"  RSSI={h['rssi_min']}..{h['rssi_max']}dBm  pkts={h['pkt_count']}"
            )

    if new_hits:
        lines.append(f"\n🆕 New channels:")
        for h in new_hits:
            marker = "📦" if h['pkt_count'] > 0 else "📻"
            lines.append(
                f"  {marker} {fmt_freq(h['freq'])}  BW={h['bw']//1000}kHz  SF{h['sf']}"
                f"  RSSI={h['rssi_min']}..{h['rssi_max']}dBm"
            )
    else:
        lines.append(f"\n✅ No new channels")

    if hits and not new_hits:
        lines.append(f"\nAll known channels ({len(hits)}):")
        for h in hits[:10]:  # top 10
            marker = "📦" if h['pkt_count'] > 0 else "  "
            lines.append(
                f"  {marker} {fmt_freq(h['freq'])}  BW={h['bw']//1000}kHz  SF{h['sf']}"
                f"  {h['rssi_min']}..{h['rssi_max']}dBm"
            )

    return '\n'.join(lines)

def load_known():
    if os.path.exists(HITS_FILE):
        with open(HITS_FILE) as f:
            return json.load(f)
    return {}

def save_known(known):
    with open(HITS_FILE, 'w') as f:
        json.dump(known, f, indent=2)

def main():
    log("LoRa CAD monitor v2 starting")
    known = load_known()

    while True:
        try:
            ser = serial.Serial(SERIAL_PORT, BAUD, timeout=2)
            log(f"Connected to {SERIAL_PORT}")
            in_report    = False
            report_lines = []
            pass_num     = 0
            total_cad    = 0
            total_pkt    = 0

            while True:
                raw = ser.readline()
                if not raw:
                    continue
                line = raw.decode('utf-8', errors='replace').strip()

                # Log comments and hits only (not every scan line)
                if line.startswith('#') or line.endswith(',1'):
                    log(line)

                # ── Immediate alert on real packet ───────────────────────────
                if line.startswith('# PACKET '):
                    pkt = parse_packet_line(line)
                    if pkt:
                        # Decode protocol
                        decoded = decode_packet(pkt['hex'], pkt['freq'], pkt['bw'], pkt['sf'])
                        alert = format_decoded(pkt, decoded)
                        send_alert(alert)
                        # Save
                        key = f"{pkt['freq']}_{pkt['bw']}_{pkt['sf']}"
                        known[key] = {**pkt, 'protocol': decoded['protocol']}
                        save_known(known)
                    continue

                # ── RX window timeout — log ───────────────────────────────────
                if '# RX_WINDOW' in line or '# RX_WINDOW_TIMEOUT' in line:
                    log(line)
                    continue

                # ── 15-minute report ──────────────────────────────────────────
                if '# REPORT_START' in line:
                    in_report    = True
                    report_lines = []
                    continue

                if '# REPORT_END' in line:
                    in_report = False
                    hits = parse_report(report_lines)

                    for rl in report_lines:
                        if 'PASS=' in rl:
                            try:
                                pass_num  = int(rl.split('PASS=')[1].split()[0])
                                total_cad = int(rl.split('CAD_HITS=')[1].split()[0])
                                total_pkt = int(rl.split('PACKETS=')[1].split()[0])
                            except:
                                pass

                    for h in hits:
                        key = f"{h['freq']}_{h['bw']}_{h['sf']}"
                        known[key] = h
                    save_known(known)

                    alert = build_report_alert(hits, pass_num, total_cad, total_pkt)
                    send_alert(alert)
                    log(f"Report sent: {len(hits)} channels, pkts={total_pkt}")
                    continue

                if in_report:
                    report_lines.append(line)

        except serial.SerialException as e:
            log(f"Serial error: {e} — retry in 5s")
            time.sleep(5)
        except KeyboardInterrupt:
            log("Monitor stopped")
            break
        except Exception as e:
            log(f"Error: {e} — retry in 10s")
            time.sleep(10)

if __name__ == '__main__':
    main()
