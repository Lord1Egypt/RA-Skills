---
name: keychain-bridge
description: Manage secrets via macOS Keychain instead of plaintext files. Migrate existing secrets, read/write keychain entries, bridge to files for bash tools, audit for leaks, diagnose access issues. Use when asked about secrets, keychain, credentials, API keys, or security hardening on macOS.
homepage: https://github.com/moltbot/keychain-bridge
metadata:
  openclaw:
    emoji: "🔐"
    requires:
      bins: ["bash", "python3"]
      env: []
    files: ["scripts/*"]
  clawmart:
    price: 99
    currency: USD
    category: security
    tags: ["keychain", "macos", "secrets", "credentials", "tahoe", "migration"]
---

# Keychain Bridge

## Trigger Phrases

- "migrate secrets to keychain" / "move secrets"
- "check keychain health" / "keychain status"
- "audit secrets" / "check for leaks"
- "read secret" / "get API key"
- "store secret" / "write to keychain"
- "keychain not working" / "security find-generic-password hangs"

## Example Usage

```
User: "Migrate my secrets to the keychain"
Action: python3 SKILL_DIR/scripts/migrate_secrets.py --dir ~/.openclaw/secrets/ --account moltbot --dry-run

User: "Check if the keychain bridge is healthy"
Action: Run keychain health check (test write/read/delete cycle)

User: "Audit for plaintext secret leaks"
Action: python3 SKILL_DIR/scripts/audit_secrets.py --dir ~/.openclaw/secrets/ --account moltbot
```

Manage secrets via macOS Keychain instead of plaintext files. Eliminates plaintext credential storage while maintaining compatibility with bash-based tools through a file-bridge architecture.

## Prerequisites

The `keyring` Python library must be installed for each Python version that will access secrets:

```bash
pip3 install keyring
# If multiple Python versions exist (common on macOS):
/usr/bin/python3 -m pip install keyring
/opt/homebrew/opt/python@3.14/bin/python3.14 -m pip install --break-system-packages keyring
```

## Check Keychain Health

Verify the keychain bridge is working correctly:

```bash
python3 -c "
import keyring
# Test write
keyring.set_password('keychain-bridge-test', 'test', 'hello')
# Test read
val = keyring.get_password('keychain-bridge-test', 'test')
assert val == 'hello', f'Read back {val!r}, expected hello'
# Cleanup
keyring.delete_password('keychain-bridge-test', 'test')
print('Keychain health: OK')
"
```

If this fails, see **Diagnose Issues** below.

## Migrate Secrets

Migrate plaintext secret files to macOS Keychain. The migration tool:
- Auto-detects all Python versions on the system
- Injects each secret from ALL detected Python binaries (required for ACL coverage)
- Verifies the round-trip read
- Optionally deletes the original file

```bash
python3 SKILL_DIR/scripts/migrate_secrets.py --dir ~/.openclaw/secrets/ --account moltbot --dry-run
# Remove --dry-run to actually migrate
python3 SKILL_DIR/scripts/migrate_secrets.py --dir ~/.openclaw/secrets/ --account moltbot
```

After migration, secrets fall into two groups:

### Group A — Keychain Only
Python scripts read directly via `keychain_helper.get_secret(service)`. No file on disk.

### Group B — File Bridge
Bash scripts cannot reliably use Python keyring as a subprocess (see **Known Issues**). For these, a boot-time bridge script populates files from the keychain:

```bash
# Add to your LaunchAgent or startup script:
bash SKILL_DIR/scripts/populate_secrets.sh
```

This reads each Group B secret from keychain and writes it to a `chmod 600` file that bash scripts can `cat`.

## Read a Secret

### From Python
```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from keychain_helper import get_secret

token = get_secret("my-service-name")
```

The helper tries keychain first, falls back to file read.

### From Bash (via Group B file)
```bash
MY_SECRET=$(cat ~/.openclaw/secrets/my-service-name)
```

Ensure the service is listed in `populate_secrets.sh` so the file is populated at boot.

### From Bash (via CLI helper — interactive only)
```bash
# Works from terminal, but HANGS from LaunchAgent bash scripts
MY_SECRET=$(python3 path/to/get_secret.py my-service-name)
```

## Write a Secret

**Critical**: Inject from ALL Python versions on the system. Keychain ACLs are per-binary — an item created by Python 3.9 cannot be read by Python 3.14 unless both binaries are in the ACL.

```bash
# Detect Python versions
PYTHONS=()
[ -x /usr/bin/python3 ] && PYTHONS+=(/usr/bin/python3)
[ -x /opt/homebrew/opt/python@3.14/bin/python3.14 ] && PYTHONS+=(/opt/homebrew/opt/python@3.14/bin/python3.14)

# Inject from each
for py in "${PYTHONS[@]}"; do
    $py -c "import keyring; keyring.set_password('SERVICE', 'ACCOUNT', 'VALUE')"
done
```

Or use the migration tool for batch operations.

## Audit for Leaks

Check for unexpected plaintext secret files and verify keychain health:

```bash
python3 SKILL_DIR/scripts/audit_secrets.py --dir ~/.openclaw/secrets/ --account moltbot
```

Reports:
- Unexpected files in the secrets directory (potential leaks)
- Keychain items that exist but can't be read (ACL issues)
- Files that exist but aren't in keychain (unmigrated)
- Keychain library installation status per Python version

## Diagnose Issues

### `security find-generic-password -w` hangs
**macOS Tahoe 26.x regression.** The `security` CLI hangs indefinitely (or returns exit code 36) when reading keychain items, even after `security unlock-keychain`. This affects ALL CLI-based keychain reads.

**Fix**: Use Python `keyring` library instead. It uses the Security framework C API via ctypes, bypassing the broken CLI entirely.

### Python keyring returns None or raises errSecInteractionNotAllowed (-25308)
This happens when running from an SSH session. The keychain requires a GUI session (SecurityAgent) context.

**Fix (recommended)**: Use the Group B file-bridge pattern. Write secrets from a GUI session (LaunchAgent or VNC Terminal), then read from `chmod 600` files in SSH.

**Fix (SSH write — ctypes unlock)**: The `security unlock-keychain -p` CLI command is also broken on Tahoe (returns "incorrect passphrase" with correct password). Use the Security framework C API via ctypes instead. The unlock + set + verify **must happen in a single Python process** — the unlock does not persist across invocations:

```python
python3 << 'PYEOF'
import ctypes, ctypes.util, keyring

# Unlock via Security framework (bypasses broken security CLI)
Security = ctypes.cdll.LoadLibrary(ctypes.util.find_library("Security"))
keychain = ctypes.c_void_p()
path = b"/Users/USERNAME/Library/Keychains/login.keychain-db"
Security.SecKeychainOpen(path, ctypes.byref(keychain))
pw = b"YOUR_LOGIN_PASSWORD"
Security.SecKeychainUnlock(keychain, ctypes.c_uint32(len(pw)), pw, ctypes.c_bool(True))

# Now keyring works — but ONLY within this same process
keyring.set_password("SERVICE", "ACCOUNT", "VALUE")
print("OK" if keyring.get_password("SERVICE", "ACCOUNT") else "FAIL")
PYEOF
```

**Caveats of ctypes unlock:**
- Unlock is **process-scoped** — a second `python3` invocation starts locked again
- Only `/usr/bin/python3` (Apple system Python) can write after ctypes unlock; Homebrew Pythons (3.12, 3.14) still get -25308 even in the same process
- For multi-Python ACL coverage, write from `/usr/bin/python3` first, then inject from other Pythons in a VNC Terminal session (GUI context)
- If you need SSH-only access to the secret after writing, create a Group B bridge file in the same process:

```python
# After keyring.set_password() succeeds in the same process:
import os
val = keyring.get_password("SERVICE", "ACCOUNT")
os.makedirs(os.path.expanduser("~/.my-app/secrets"), exist_ok=True)
path = os.path.expanduser("~/.my-app/secrets/SERVICE")
with open(path, "w") as f:
    f.write(val)
os.chmod(path, 0o600)
```

### Python keyring hangs when called from bash LaunchAgent
**Novel finding (macOS Tahoe 26.x).** When a bash script is the LaunchAgent program and spawns `python3 get_secret.py` as a subprocess, the Python process hangs indefinitely. The SecurityAgent session attachment is lost in the bash-to-python subprocess transition.

**Fix**: Use the Group B file-bridge pattern. Have a Python-native process populate files at boot, then bash scripts read from files.

Alternatively, make Python the direct LaunchAgent program (not a subprocess of bash).

### Different Python versions can't read each other's items
Keychain ACLs are per-binary. An item created by `/usr/bin/python3` (Python 3.9) has an ACL entry only for that binary. `/opt/homebrew/bin/python3.14` is a different binary and gets access denied.

**Fix**: Inject from both Python versions:
```python
# Read from working version, write via target version
import subprocess, keyring
value = keyring.get_password("service", "account")
subprocess.run(["/opt/homebrew/bin/python3.14", "-c",
    f"import keyring; keyring.set_password('service', 'account', '{value}')"])
```

Or use `migrate_secrets.py` which handles this automatically.

### `keyring` not installed for a Python version
Each Python binary has its own site-packages. `pip3 install keyring` only installs for one.

```bash
# Check which Python pip3 targets
pip3 --version
# Install for system Python
/usr/bin/python3 -m pip install keyring
# Install for Homebrew Python
/opt/homebrew/opt/python@3.14/bin/python3.14 -m pip install --break-system-packages keyring
```

## Architecture Reference

```
                    ┌─────────────────────┐
                    │   macOS Keychain     │
                    │  (login keychain)    │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
    ┌─────────▼─────────┐     │     ┌──────────▼──────────┐
    │   Group A          │     │     │   Group B            │
    │   (keychain only)  │     │     │   (file bridge)      │
    │                    │     │     │                      │
    │ Python scripts     │     │     │ populate_secrets.sh  │
    │ import keychain_   │     │     │ runs at boot →       │
    │ helper.get_secret()│     │     │ writes chmod 600     │
    │                    │     │     │ files for bash       │
    └────────────────────┘     │     └──────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Fallback           │
                    │   get_secret() tries │
                    │   keychain first,    │
                    │   then file read     │
                    └─────────────────────┘
```

### When to use Group A
- The consumer is a Python script
- The script runs as a LaunchAgent (or from terminal)
- The script is NOT spawned as a subprocess from a bash LaunchAgent

### When to use Group B
- The consumer is a bash script
- The bash script runs as a LaunchAgent
- The secret is referenced by a config file that expects `file:secrets/` paths

## Known Issues (macOS Tahoe 26.x)

1. **`security` CLI broken across the board**: `find-generic-password -w` hangs or exits 36. `unlock-keychain -p` returns "incorrect passphrase" with correct password. `show-keychain-info` exits 36. The entire `security` CLI is unreliable on Tahoe — use Python `keyring` (Group A) or ctypes Security framework for all keychain operations.
2. **Keychain ACL per-binary**: Must inject from every Python version that will read the item.
3. **Bash subprocess loses SecurityAgent**: `bash LaunchAgent → python3 subprocess` hangs. Use Group B file bridge.
4. **SSH sessions lack GUI context**: Keychain reads/writes fail with -25308. Use ctypes `SecKeychainUnlock` in the same Python process (see Diagnose Issues), or use Group B file bridge. The ctypes unlock is process-scoped — it does not persist across separate command invocations.
5. **`keyring` must be installed per-Python**: Each binary's site-packages is independent.
6. **Homebrew Python ignores ctypes unlock**: After `SecKeychainUnlock` via ctypes, `/usr/bin/python3` (Apple system Python 3.9) can read/write via `keyring`, but Homebrew Pythons (3.12, 3.14) still get -25308. Root cause unknown — may be entitlement or codesigning difference. Workaround: write from `/usr/bin/python3`, then inject from Homebrew Pythons in a GUI session (VNC Terminal or LaunchAgent).

These issues are specific to macOS Tahoe 26.x (macOS 26). Earlier versions (Sonoma 14, Sequoia 15) may not exhibit all of them, but the Group A/B architecture is safe on all versions.

## External Endpoints

None. This skill makes zero network requests. All operations are local to the macOS Keychain and filesystem.

## Security & Privacy

- All operations execute locally against the macOS login keychain
- No telemetry, analytics, or usage tracking
- No data leaves the machine under any circumstances
- Scripts request no network permissions
- Secrets are only read from and written to the local keychain or `chmod 600` files
- Migration tool never logs or displays secret values

## Trust Statement

All code is open for inspection — no obfuscation, no minification, no compiled binaries. The skill operates exclusively on the local macOS Keychain and filesystem. Built and tested on a production Mac Mini M4 Pro deployment running OpenClaw 24/7 with 12+ API keys and 25 automated scripts.
