#!/usr/bin/env python3
"""
generate_qr.py - Capture WhatsApp QR code and write to a PNG file.

Forks a background process to keep the OpenClaw WhatsApp login session alive
(so the QR stays scannable), writes the PNG, then exits. The background child
dies automatically when the session completes or times out.

Usage:
  python3 generate_qr.py [OUTPUT_PNG] [--scale N] [--quiet N] [--timeout N]

Defaults:
  OUTPUT_PNG  /tmp/whatsapp_qr.png
  --scale     10   (pixels per QR module)
  --quiet     6    (quiet zone modules)
  --timeout   55   (seconds to keep session alive after PNG is written)

Exit codes:
  0  PNG written successfully; path printed to stdout
  1  Error — message printed to stderr (already linked, capture failed, etc.)

Interactive use:
  python3 generate_qr.py /tmp/test.png
  # watch stderr for progress; on success stdout shows the written path
  # then open /tmp/test.png to verify
"""

import argparse
import os
import pty
import re
import select
import subprocess
import sys
import tempfile
import time

BLOCK_CHARS = set('▄▀█ ')
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))


def strip_ansi(text):
    text = re.sub(r'\x1b\][^\x07]*\x07', '', text)
    return re.sub(r'\x1b\[[0-9;]*[mKHFABCDJlhABCDEFGHSTfr]', '', text)


def extract_qr_lines(raw_bytes):
    text = raw_bytes.decode('utf-8', errors='replace')
    clean = strip_ansi(text).replace('\r\n', '\n').replace('\r', '\n')
    return [l.rstrip() for l in clean.split('\n')
            if l.strip() and re.match(r'^[▄█▀ ]+$', l.strip())]


def write_png(lines, output_path, scale, quiet):
    """Write QR lines to PNG via qr_decode.py. Returns (ok, message)."""
    decoder = os.path.join(SCRIPTS_DIR, 'qr_decode.py')
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write('\n'.join(lines))
        tmpfile = f.name
    try:
        r = subprocess.run(
            ['python3', decoder, tmpfile, output_path,
             '--scale', str(scale), '--quiet', str(quiet)],
            capture_output=True, text=True
        )
        if r.returncode == 0:
            return True, r.stdout.strip()
        else:
            return False, r.stderr.strip() or r.stdout.strip()
    finally:
        os.unlink(tmpfile)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('output', nargs='?', default='/tmp/whatsapp_qr.png',
                        help='Output PNG path (default: /tmp/whatsapp_qr.png)')
    parser.add_argument('--scale', type=int, default=10,
                        help='Pixels per QR module (default: 10)')
    parser.add_argument('--quiet', type=int, default=6,
                        help='Quiet zone size in modules (default: 6)')
    parser.add_argument('--timeout', type=int, default=55,
                        help='Seconds to keep session alive after PNG written (default: 55)')
    args = parser.parse_args()

    print(f"[generate_qr] Starting WhatsApp login...", file=sys.stderr)

    master_fd, slave_fd = pty.openpty()
    os.set_inheritable(slave_fd, True)
    env = os.environ.copy()
    env['COLUMNS'] = '120'
    env['TERM'] = 'xterm-256color'

    proc = subprocess.Popen(
        ['openclaw', 'channels', 'login', '--channel', 'whatsapp'],
        stdin=slave_fd, stdout=slave_fd, stderr=slave_fd,
        close_fds=True, env=env
    )
    os.close(slave_fd)

    output = b''
    qr_detected_at = None
    deadline = time.time() + 20  # max time to wait for QR to appear

    while time.time() < deadline:
        try:
            r, _, _ = select.select([master_fd], [], [], 0.3)
            if r:
                chunk = os.read(master_fd, 4096)
                if not chunk:
                    break
                output += chunk
        except OSError:
            break

        if proc.poll() is not None:
            # Process exited before QR appeared
            text = output.decode('utf-8', errors='replace')
            if 'already linked' in text.lower() or 'linked!' in text.lower():
                print("ERROR: WhatsApp is already linked — unlink first", file=sys.stderr)
            elif 'logged out' in text.lower():
                print("ERROR: Session logged out — run again", file=sys.stderr)
            else:
                print(f"ERROR: Login exited unexpectedly", file=sys.stderr)
                print(strip_ansi(text[-500:]), file=sys.stderr)
            sys.exit(1)

        if not qr_detected_at and b'Scan this QR' in output:
            qr_detected_at = time.time()
            print(f"[generate_qr] QR detected, waiting 3s for full render...", file=sys.stderr)

        # Wait 3s after QR detected to ensure all 30 lines are buffered
        if qr_detected_at and (time.time() - qr_detected_at) >= 3.0:
            lines = extract_qr_lines(output)
            print(f"[generate_qr] Extracted {len(lines)} QR lines", file=sys.stderr)

            if len(lines) < 20:
                print(f"ERROR: Only {len(lines)} QR lines found (need ≥20)", file=sys.stderr)
                proc.terminate()
                proc.wait()
                sys.exit(1)

            ok, msg = write_png(lines, args.output, args.scale, args.quiet)
            if not ok:
                print(f"ERROR: PNG write failed: {msg}", file=sys.stderr)
                proc.terminate()
                proc.wait()
                sys.exit(1)

            print(f"[generate_qr] {msg}", file=sys.stderr)

            # Fork: child keeps login alive; parent exits with the result
            child_pid = os.fork()
            if child_pid > 0:
                # Parent — print result and exit cleanly
                print(args.output)
                sys.exit(0)

            # ---- Child process ----
            # Close parent's stdout/stderr so they don't block
            sys.stdout.close()
            sys.stderr.close()
            # Keep the login session alive until timeout or natural exit
            remaining = args.timeout - (time.time() - qr_detected_at)
            child_deadline = time.time() + max(remaining, 0)
            while time.time() < child_deadline:
                try:
                    r2, _, _ = select.select([master_fd], [], [], 1.0)
                    if r2:
                        chunk = os.read(master_fd, 4096)
                        if not chunk:
                            break
                except OSError:
                    break
                if proc.poll() is not None:
                    break
            try:
                os.close(master_fd)
            except OSError:
                pass
            proc.terminate()
            proc.wait()
            sys.exit(0)

    # Timed out waiting for QR
    try:
        os.close(master_fd)
    except OSError:
        pass
    proc.terminate()
    proc.wait()
    print("ERROR: Timed out waiting for QR code to appear", file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    main()
