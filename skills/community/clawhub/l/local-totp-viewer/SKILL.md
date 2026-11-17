---
name: local-totp-viewer
description: Set up and use a zero-dependency local TOTP code viewer on a Linux PC. Use when a user wants 2FA/TOTP codes shown on the desktop, wants to migrate secrets out of Google Authenticator, or needs one-time codes without a phone.
license: MIT
---

# Local TOTP Viewer

Show and manage TOTP (RFC 6238) codes directly on a PC with a single-file Python script — no phone, no external app, no dependencies.

## When to use

- The user wants 2FA codes displayed on their desktop instead of a phone.
- Migrating secrets from Google Authenticator to a desktop workflow.
- A headless/CLI workflow needs one-time codes (e.g. automated login steps where a human confirms each code).

## The script

Save this as `~/2fa_view.py` (pure stdlib + optional system `qrcode` not required):

```python
#!/usr/bin/env python3
"""Zero-dependency TOTP viewer. Usage:
  python3 2fa_view.py                    # live view of all codes
  python3 2fa_view.py <base32> <name>    # register a secret
  python3 2fa_view.py "otpauth://..."    # register from URI
  python3 2fa_view.py -l                 # list
  python3 2fa_view.py -r <name>          # remove
"""
import base64, hashlib, hmac, json, os, struct, sys, time, urllib.parse

STORE = os.path.expanduser("~/.2fa_secrets.json")

def load():
    if os.path.exists(STORE):
        with open(STORE) as f:
            return json.load(f)
    return {}

def save(d):
    with open(STORE, "w") as f:
        json.dump(d, f)
    os.chmod(STORE, 0o600)

def totp(secret_b32, digits=6, period=30, algo="sha1"):
    key = base64.b32decode(secret_b32.upper() + "=" * (-len(secret_b32) % 8))
    counter = int(time.time()) // period
    msg = struct.pack(">Q", counter)
    h = hmac.new(key, msg, hashlib.sha1 if algo == "sha1" else hashlib.sha256).digest()
    o = h[-1] & 0x0F
    code = (struct.unpack(">I", h[o:o+4])[0] & 0x7FFFFFFF) % (10 ** digits)
    return str(code).zfill(digits)

def main():
    d = load()
    args = sys.argv[1:]
    if not args:
        try:
            while True:
                now = int(time.time())
                left = 30 - (now % 30)
                line = []
                for name, s in sorted(d.items()):
                    line.append(f"{name}: {totp(s)} ({left:2d}s)")
                print("  |  ".join(line) + "    ", end="\r")
                time.sleep(0.25)
        except KeyboardInterrupt:
            print()
        return
    if args[0] == "-l":
        for name, s in sorted(d.items()):
            print(f"{name}  {s[:8]}...")
        return
    if args[0] == "-r":
        d.pop(args[1], None); save(d); print("removed"); return
    if args[0].startswith("otpauth://"):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(args[0]).query)
        d[q.get("issuer", ["?"])[0] + ":" + q["secret"][0][:6]] = q["secret"][0]
        save(d); print("registered from URI"); return
    d[args[1]] = args[0]
    save(d)
    print(f"registered {args[1]}")

if __name__ == "__main__":
    main()
```

Verify against the RFC 6238 test vector (secret `GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ`, T=59s, SHA1 → `94287082`) before trusting it.

## Migrating secrets from Google Authenticator

Google Authenticator can export all accounts as a single QR code:

1. In the app: menu → Transfer accounts → Export accounts → select accounts.
2. Screenshot the QR code and pass the image to the agent.
3. Decode it with a QR library (e.g. `pyzbar`); OpenCV's QR detector often fails on app screenshots.
4. The payload is an `otpauth-migration://offline?data=<base64>` URI. URL-decode, then parse the protobuf:
   - field 1 (`otp_parameters`): secret = field 1 (bytes), name = field 2, issuer = field 3, algo = field 4 (1=SHA1), digits = field 5 (1=6 digits), type = field 6 (2=TOTP).
   - Encode each secret as base32: `base64.b32encode(secret).rstrip(b"=")`.
5. Register each secret with the viewer script.

## Pitfalls

- Generate a code immediately before entering it. TOTP windows are 30 seconds; a pre-generated code can expire mid-entry.
- Keep the secrets file at mode 600 and never print full secrets into chat logs or transcripts.
- When automating a login form, type the code within the window and handle rejection by waiting for the next window rather than retrying the same code.
