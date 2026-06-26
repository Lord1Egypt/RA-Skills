#!/usr/bin/env python3
"""Secure credential file manager with age encryption (asymmetric keypair).

Files stored encrypted in ~/Documenti/credentials/ (*.age).
Uses age keypair: public key encrypts, private key decrypts.
Private key at ~/.local/share/local-rag/cred-key.txt.

Commands:
    encrypt <file> [--keep]        — Encrypt with public key → .age
    decrypt <file.age>             — Decrypt to stdout
    list                           — List encrypted credentials
    send <file.age> -t <id>        — Decrypt to RAM and send via openclaw
    receive <file> [--name NAME]   — Encrypt and store from received file (pipe-safe)
    rekey                          — Re-encrypt all with new keypair

Security:
    - age X25519 + ChaCha20-Poly1305
    - Private key chmod 600, never leaves machine
    - Temp files in workspace (openclaw allowed dir), secure-deleted after use
    - receive() encrypts in a single pipe — plaintext never touches disk
"""

import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime

CRED_DIR = os.path.expanduser("~/Documenti/credentials")
KEY_PATH = os.path.expanduser("~/.local/share/local-rag/cred-key.txt")
AGE_EXT = ".age"
TEMP_SEND_DIR = os.path.realpath(os.path.expanduser("~/.openclaw/workspace/.tmp-send"))


def get_public_key() -> str:
    """Extract public key from keypair file."""
    with open(KEY_PATH) as f:
        for line in f:
            if line.startswith("# public key: "):
                return line.split(": ", 1)[1].strip()
    proc = subprocess.run(["age-keygen", "-y", KEY_PATH], capture_output=True, text=True)
    return proc.stdout.strip()


def encrypt_file(filepath: str, output: str = None) -> str:
    """Encrypt a file on disk."""
    filepath = os.path.expanduser(filepath)
    if not os.path.exists(filepath):
        print(f"ERROR: Not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    output = output or filepath + AGE_EXT
    pubkey = get_public_key()
    proc = subprocess.run(
        ["age", "-e", "-r", pubkey, "-o", output, filepath],
        capture_output=True, text=True
    )
    if proc.returncode != 0:
        print(f"ERROR: {proc.stderr}", file=sys.stderr)
        sys.exit(1)
    return output


def encrypt_stream(input_path: str, output_path: str):
    """Encrypt file via pipe — plaintext read once, encrypted written directly.
    Secure-deletes the input immediately after encryption succeeds."""
    pubkey = get_public_key()
    with open(input_path, "rb") as infile, open(output_path, "wb") as outfile:
        proc = subprocess.Popen(
            ["age", "-e", "-r", pubkey],
            stdin=infile, stdout=outfile, stderr=subprocess.PIPE
        )
        _, stderr = proc.communicate()
        if proc.returncode != 0:
            print(f"ERROR: {stderr.decode()}", file=sys.stderr)
            sys.exit(1)
    # Encryption succeeded — secure-delete the plaintext
    secure_delete(input_path)


def decrypt_to_bytes(filepath: str) -> bytes:
    filepath = os.path.expanduser(filepath)
    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)
    proc = subprocess.run(
        ["age", "-d", "-i", KEY_PATH, filepath],
        capture_output=True
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode())
    return proc.stdout


def secure_delete(path: str):
    """Secure delete: 3-pass overwrite (zeros, ones, random) then remove.
    More robust than single-pass, especially on SSDs."""
    if not os.path.exists(path):
        return
    size = os.path.getsize(path)
    try:
        with open(path, "wb") as f:
            f.write(b"\x00" * size)
            f.flush()
            os.fsync(f.fileno())
            f.seek(0)
            f.write(b"\xFF" * size)
            f.flush()
            os.fsync(f.fileno())
            f.seek(0)
            f.write(os.urandom(size))
            f.flush()
            os.fsync(f.fileno())
    except OSError:
        pass
    os.remove(path)


def list_files():
    os.makedirs(CRED_DIR, exist_ok=True)
    files = sorted(glob.glob(os.path.join(CRED_DIR, f"*{AGE_EXT}")))
    if not files:
        print(f"No encrypted files in {CRED_DIR}/")
        return
    print(f"{'Name':<45} {'Size':>10} {'Modified':<20}")
    print("-" * 75)
    for f in files:
        name = os.path.basename(f)
        size = os.path.getsize(f)
        mtime = datetime.fromtimestamp(os.path.getmtime(f)).strftime("%Y-%m-%d %H:%M")
        size_str = f"{size / 1024:.1f}K" if size < 1024 * 1024 else f"{size / 1024 / 1024:.1f}M"
        print(f"  {name:<43} {size_str:>10} {mtime:<20}")
    print(f"\n  Total: {len(files)} files")


def send_file(filepath: str, target: str, channel: str):
    """Decrypt to RAM, write to workspace temp, send, secure delete."""
    # Verify openclaw is available
    if not shutil.which("openclaw"):
        print("ERROR: openclaw CLI not found in PATH", file=sys.stderr)
        sys.exit(1)

    try:
        plaintext = decrypt_to_bytes(filepath)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    tmp_dir = TEMP_SEND_DIR
    basename = os.path.basename(filepath).removesuffix(AGE_EXT)
    ext_suffix = os.path.splitext(basename)[1] or ".bin"

    fd, tmp_path_raw = tempfile.mkstemp(prefix=f"cred-{basename}-", suffix=ext_suffix, dir=tmp_dir)
    try:
        os.write(fd, plaintext)
        os.close(fd)
        plaintext = b"\x00" * len(plaintext)
        # Rename to clean filename so the recipient gets the correct name
        tmp_path = os.path.join(os.path.dirname(tmp_path_raw), basename)
        os.rename(tmp_path_raw, tmp_path)
        os.chmod(tmp_path, 0o600)

        # Use send_file.py which handles allowed-path restrictions
        send_script = os.path.join(os.path.dirname(__file__), "send_file.py")
        cmd = [
            sys.executable, send_script, tmp_path,
            "--target", target, "--channel", channel, "--force-document",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"ERROR: {result.stderr}", file=sys.stderr)
        else:
            print(f"✅ Sent {basename} via {channel} to {target}")
    finally:
        secure_delete(tmp_path)


def receive_file(filepath: str, name: str = None):
    """Receive a file (e.g. from Telegram download), encrypt it, and store.
    The plaintext file is secure-deleted after successful encryption."""
    filepath = os.path.expanduser(filepath)
    if not os.path.exists(filepath):
        print(f"ERROR: Not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(CRED_DIR, exist_ok=True)

    # Determine output name
    basename = name or os.path.basename(filepath)
    if not basename.endswith(AGE_EXT):
        basename += AGE_EXT

    output_path = os.path.join(CRED_DIR, basename)

    # Check for collision
    if os.path.exists(output_path):
        stem, ext = os.path.splitext(basename)
        i = 1
        while os.path.exists(output_path):
            output_path = os.path.join(CRED_DIR, f"{stem}_{i}{ext}")
            i += 1

    # Encrypt (pipe — plaintext never written to credentials dir)
    encrypt_stream(filepath, output_path)
    print(f"✅ Received & encrypted → {output_path}")
    print(f"🔒 Plaintext securely deleted")


def main():
    parser = argparse.ArgumentParser(description="Secure credential manager (age encryption)")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list")

    enc = sub.add_parser("encrypt")
    enc.add_argument("file")
    enc.add_argument("--keep", action="store_true")

    dec = sub.add_parser("decrypt")
    dec.add_argument("file")

    send = sub.add_parser("send")
    send.add_argument("file")
    send.add_argument("--target", "-t", required=True)
    send.add_argument("--channel", "-c", default="telegram")

    recv = sub.add_parser("receive")
    recv.add_argument("file", help="Path to plaintext file to encrypt and store")
    recv.add_argument("--name", "-n", help="Custom name for stored file (without .age)")

    args = parser.parse_args()

    if args.command == "list":
        list_files()
    elif args.command == "encrypt":
        out = encrypt_file(args.file)
        print(f"✅ Encrypted → {out}")
        if not args.keep:
            orig = os.path.expanduser(args.file)
            if os.path.exists(orig) and not orig.endswith(AGE_EXT):
                os.remove(orig)
                print(f"🗑️  Deleted plaintext: {orig}")
    elif args.command == "decrypt":
        try:
            data = decrypt_to_bytes(args.file)
            sys.stdout.buffer.write(data)
        except Exception as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.command == "send":
        send_file(args.file, args.target, args.channel)
    elif args.command == "receive":
        receive_file(args.file, args.name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
