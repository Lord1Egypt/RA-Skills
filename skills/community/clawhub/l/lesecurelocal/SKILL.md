---
name: LESecureLocal
description: LESecure Local/On-Prem — encrypt and decrypt data, files, and folders using the LE desktop tool with layered locks (pin, password, MFA, time lock, geo-location).
triggers:
  - LESecure Local
  - LESecure Desktop
  - LESecure On-Prem
  - LE local
  - LE desktop
  - encrypt file
  - decrypt file
  - encrypt folder
  - decrypt folder
  - what's my current location
  - what is my current location
  - whereami
  - where am i
  - current location
---

# LESecureLocal — LESecure Local / On-Prem Skills

Encrypt and decrypt **plain text, files, and folders** using the LE desktop binary. No API key is needed — everything runs locally. No data leaves your machine.

## Project Links

| Resource | URL |
|---|---|
| Source code & documentation | <https://github.com/SPAlgorithm/LE> |
| Cloud alternative | LESecureCl skill (uses the LESecure API) |

## ROUTING RULES (MANDATORY)

- **Files and folders MUST always use LESecure Local.** Never use LESecure Cloud for file/folder encryption. If the user asks to encrypt files/folders via cloud, inform them: "File/folder encryption is only supported via LESecure Local (desktop)." and use this skill.
- **Safe-by-default flags for files/folders.** Always pass `-z` (force overwrite) and — when the target is a directory — `-n` (recursive). **Never pass `-c` (clean/delete source) or `-j` (trio = `-z -c -n`) without explicit user confirmation**, because both delete the original file after encrypting. See the "Destructive Flags" rules below.
- **For plain text**, ask the user: "Would you like to use **LESecure Cloud** (API) or **LESecure Local** (desktop)?" and proceed accordingly.
- **Current location queries** — when the user asks "what's my current location", "whereami", "where am I", or any equivalent, run `LE -7` and share the output. No other flags are needed. **Note:** `LE -7` accesses device GPS — this is a privacy-sensitive operation. On first use in a session, inform the user: "This will query your device's GPS location via LE." Proceed only after acknowledgment.

## Destructive Flags — `-c` and `-j` (MANDATORY)

- `-c` (clean) **deletes the source file after encryption or decryption**. It is irreversible in-place data loss.
- `-j` is a trio that **includes `-c`**, so it is also destructive.
- Never silently add `-c` or `-j`. Before using either, ask the user explicitly, e.g.: "This will delete the source `<file>` after the operation. Confirm with 'yes, delete source' to proceed."
- If the user does not confirm, use only `-z` (and `-n` for folders). The source stays on disk.
- When the user explicitly asks for `-j` or "clean/delete source after", use `-j` and state in the response that the source was removed.

## Binary Location (configuration)

The skill looks for the `LE` binary in this order:

1. The `LE_BIN` environment variable, if set (e.g., `export LE_BIN=/opt/le/LE`).
2. `LE` on `PATH` (via `command -v LE`).
3. A user-supplied path if neither of the above resolves. In that case, **ask the user** for the binary path — do not guess or hardcode.

In examples below, `LE` is used as a shorthand for whichever path resolves. When actually invoking, expand it to the full resolved path so the command is reproducible.

```bash
# Resolve once, then reuse
LE_BIN="${LE_BIN:-$(command -v LE)}"
"$LE_BIN" --help
```

## Date & Time Rules (MANDATORY)

All date/time handling for this skill follows these rules — no exceptions:

1. **Always use EST/EDT (America/New_York)** to calculate and send dates. The LE tool interprets `-l` and `-r` in EST/EDT.
2. **Start time (`-l`) = current EST + 2 minutes** by default. This buffer prevents the "date must be in future" error.
3. **End time (`-r`) = start time + the user's requested duration**.
4. **Cross-platform time computation.** Prefer Python because `date` flag syntax differs between BSD (macOS) and GNU (Linux). Python 3 is available on both.

   **Input safety:** The `<N>` duration value is passed as `sys.argv[1]` and cast via `int()` inside the Python script — any non-integer input raises `ValueError` and the script exits without executing. **Never concatenate or interpolate user input directly into the `python3 -c` string.** Always pass values as positional arguments (`sys.argv`).

   ```bash
   # Start time (now + 2 minutes, EDT/EST) — no user input needed
   python3 -c "from datetime import datetime,timedelta; from zoneinfo import ZoneInfo; print((datetime.now(ZoneInfo('America/New_York'))+timedelta(minutes=2)).strftime('%Y/%m/%d %H:%M'))"

   # End time (now + 2 min + N minutes) — N is passed as argv[1], cast to int()
   python3 -c "import sys; from datetime import datetime,timedelta; from zoneinfo import ZoneInfo; N=int(sys.argv[1]); print((datetime.now(ZoneInfo('America/New_York'))+timedelta(minutes=2+N)).strftime('%Y/%m/%d %H:%M'))" <N>

   # End time (now + 2 min + N hours) — N is passed as argv[1], cast to int()
   python3 -c "import sys; from datetime import datetime,timedelta; from zoneinfo import ZoneInfo; N=int(sys.argv[1]); print((datetime.now(ZoneInfo('America/New_York'))+timedelta(minutes=2,hours=N)).strftime('%Y/%m/%d %H:%M'))" <N>
   ```
   Fallback (`date`) — only if Python is unavailable:
   - macOS/BSD: `TZ=America/New_York date -v+2M "+%Y/%m/%d %H:%M"`
   - Linux/GNU: `TZ=America/New_York date -d '+2 minutes' "+%Y/%m/%d %H:%M"`
5. **Always display the window back to the user in EDT/EST**.

## Two Modes

### 1. PlainText Mode (`--PlainText` / `-p`)

Encrypt/decrypt inline strings. The LE binary expects the data wrapped in triple single quotes (`'''...'''`).

#### Input Sanitization (MANDATORY)

**Never interpolate raw user input directly into the shell command.** The `'''...'''` quoting breaks if the data contains single quotes, enabling shell injection. Before building the command:

1. **Validate:** reject or escape any single quotes (`'`) in the user's plaintext. Replace each `'` with `'\''` (end quote, escaped literal quote, reopen quote).
2. **Alternatively, use a shell variable** to isolate user data from the command string:
   ```bash
   # Store user data in a variable — shell expansion is safe inside triple quotes
   LEDATA='user provided text here'
   LE -e "'''${LEDATA}'''" <LOCK_FLAGS> --PlainText
   ```
3. **Never use `eval`** or backtick interpolation with user-supplied text.

```bash
# Encrypt (with sanitized data)
LE -e '''<SANITIZED_DATA>''' <LOCK_FLAGS> --PlainText

# Decrypt (encrypted output is safe — no special chars)
LE -d '''<ENCRYPTED_DATA>''' <LOCK_FLAGS> --PlainText
```

### 2. File / Folder Mode

Default flags (safe):
- **File:** `-z`
- **Folder:** `-z -n`

Destructive extras (only with explicit user confirmation, see rules above): add `-c` to also delete the source, or use `-j` (= `-z -c -n`).

```bash
# Safe file encrypt / decrypt (source file preserved)
LE -e <FILE>   <LOCK_FLAGS> -z
LE -d <FILE.letxt> <LOCK_FLAGS> -z

# Safe folder encrypt / decrypt (source folder preserved)
LE -e <FOLDER> <LOCK_FLAGS> -z -n
LE -d <FOLDER> <LOCK_FLAGS> -z -n

# Destructive — only after explicit user confirmation
LE -e <FILE_OR_FOLDER> <LOCK_FLAGS> -j
```

**Naming notes:**
- Encrypted files get a `.le` prefix on the extension (e.g., `example.txt` becomes `example.letxt`); use the `.letxt` filename when decrypting.
- For folders, the individual files inside get the `.le` prefix on their extensions. The folder name itself stays the same.

## Available Locks

| Flag | Lock Type | Value | Example |
|------|-----------|-------|---------|
| `-1` | Pin/Code | Numeric string | `"1122"` |
| `-w` | Password | Password file (`.letxt`) or passphrase | `pass.letxt` |
| `-2` | MFA | Phone number (E.164) | `"+19199870623"` |
| `-3` | OTP | OTP code for decryption | `"123456"` |
| `-l` | Time lock start | `YYYY/MM/DD HH:MM` | `"2026/04/12 17:41"` |
| `-r` | Time lock end | `YYYY/MM/DD HH:MM` | `"2027/04/12 17:36"` |
| `-b` | Location lock — use existing `.lecsv` key file (**encrypt only**; omit on decrypt) | Path to `.lecsv` file | `location.lecsv` |
| `-v` | Location lock — create a new `.lecsv` key file from a GPS CSV (switch, no value) | (no value) | `-v` |

### Additional Flags

| Flag | Purpose | Safety |
|------|---------|--------|
| `-z` | Force — overwrite existing encrypted file | Safe |
| `-n` | Recursive — process folders recursively | Safe |
| `-c` | Clean — **delete source after encrypt/decrypt** | DESTRUCTIVE — opt-in with confirmation |
| `-j` | Trio = `-z -c -n` — **includes delete-source** | DESTRUCTIVE — opt-in with confirmation |
| `-i` | Get info on an encrypted file | Safe (read only) |
| `-o` | Specify output file name | Safe |
| `-7` | Print the device's current GPS location (no other flags needed) | PRIVACY-SENSITIVE — requires user consent on first use |

## MFA Workflow

1. **Encrypt with MFA**: Use `-2 "+1XXXXXXXXXX"` to register the phone number.
2. **Decrypt with MFA**: First run decrypt with `-4 <encrypted_file>` to trigger OTP delivery, then run again with `-3 <OTP_CODE>`.

## Examples

### PlainText — Pin only
```bash
LE -e '''hello world''' -1 "1234" --PlainText
LE -d '''<ENCRYPTED>''' -1 "1234" --PlainText
```

### PlainText — All locks
```bash
LE -e '''secret data''' -w pass.letxt -1 "1122" -2 "+19199870623" -l "2026/04/12 17:41" -r "2027/04/12 17:36" --PlainText
```

### File — Pin only (safe, source preserved)
```bash
LE -e /path/to/myfile.txt -1 "1234" -z
LE -d /path/to/myfile.letxt -1 "1234" -z
```

### Folder — Pin + Password (safe, sources preserved)
```bash
LE -e /path/to/my_folder -w pass.letxt -1 "1234" -z -n
LE -d /path/to/my_folder -w pass.letxt -1 "1234" -z -n
```

### File — destructive (user asked to delete source)
```bash
# Only after explicit user confirmation
LE -e /path/to/myfile.txt -1 "1234" -j
```

### Get info on encrypted file
```bash
LE -i /path/to/myfile.letxt
```

### Get current device location
Requires user consent on first use in a session (privacy-sensitive — accesses device GPS).
```bash
LE -7
```

## Workflow

1. **Determine the mode:** PlainText (`--PlainText`) for inline strings, or File/Folder for files and directories.
2. **Resolve the binary** via `$LE_BIN`, `command -v LE`, or ask the user.
3. **Gather lock inputs:** Which locks to apply and their values.
4. **Pick safe defaults:** `-z` for files; `-z -n` for folders. Do not add `-c` or `-j` unless the user explicitly confirmed source deletion.
5. **Build the command** with the appropriate flags.
6. **Execute via Bash** and return the result.
7. **For decryption**, remind the user they need the same lock values used during encryption.

## Important Notes

- No API key is needed — LE runs entirely locally.
- Phone numbers for MFA (`-2`) must be in E.164 format.
- Time lock dates use `YYYY/MM/DD HH:MM` format. Follow the Date & Time Rules above.
- Time locks require both `-l` (start) and `-r` (end).
- The password file (`.letxt`) should be an encrypted password file created with `LE -e pass.txt -q`.
- Geo-location locks work in two stages: **create a key file once**, then **reuse it** to lock as many files/folders as you want.

  **Stage 1 — Create the `.lecsv` key file from a GPS CSV (`-v`):**
  - Input: a plain CSV of GPS locations with distance (e.g., `location.csv`).
  - `-v` is a switch (no value); LE produces `location.lecsv` alongside the input.
  - MUST be paired with `-1` (pin) or `-2` (MFA) — otherwise LE errors with "Either Pin or MFA should be enabled for Password/Location file".
  ```bash
  LE -e location.csv -v -1 1122 -z
  LE -e location.csv -v -2 "+1YourPhoneNumber" -z
  ```

  **Stage 2 — Use the `.lecsv` key file to lock files/folders (`-b`):**
  - `-b <path.lecsv>` is used **only on encryption**.
  - **On decryption, do NOT pass `-b`** — LE reads the embedded location reference from the encrypted file itself. Just run `LE -d <file> -z`.
  - No pin/MFA pairing required — the key file is self-contained.
  ```bash
  # Encrypt (pass -b with the key file)
  LE -e example.txt -b location.lecsv -z

  # Decrypt (do NOT pass -b)
  LE -d example.letxt -z
  ```
