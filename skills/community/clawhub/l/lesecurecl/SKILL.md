---
name: LESecureCl
description: "LESecure Cloud Skills — encrypt or decrypt data using the LESecure API with layered locks (pin, password, MFA, time lock). Use this skill whenever the user mentions LESecure, LESecureCl, LESecure Cloud, layered encryption, multi-lock encryption, or wants to protect data with combinations of pin codes, passwords, phone-based MFA, or time-based access windows. Also trigger when the user wants to decrypt LESecure-encrypted data."
---

# LESecureCl — LESecure Cloud Skills

Encrypt and decrypt **plain text data only** through the LESecure REST API. The API supports layered security "locks" that can be combined for defense-in-depth protection.

## Project Links

| Resource | URL |
|---|---|
| Source code & documentation | <https://github.com/SPAlgorithm/LE> |
| API endpoint | `https://api.lesecure.ai/exec` |
| Local/on-prem alternative | LESecureLocal skill (no data leaves your machine) |

If you cannot verify the LESecure service or its privacy practices, use the **LESecureLocal** skill instead — it runs entirely on your device with no network calls.

## Requirements (MANDATORY)

Before running any command in this skill, confirm the following are available. If any is missing, tell the user and stop — do not invent values or fall back silently.

| Requirement | Purpose | How to check |
|---|---|---|
| `curl` on `PATH` | Make the HTTPS request to the LESecure API | `command -v curl` |
| `python3` ≥ 3.9 on `PATH` | Compute time-lock windows (`-l`, `-r`) in EST/EDT cross-platform. Requires `zoneinfo` module (built-in from Python 3.9+). | `python3 -c "from zoneinfo import ZoneInfo; print('ok')"` |
| `LESECURE_API_KEY` env var | Bearer token for the API. Must be set in the shell that runs `curl`; the skill never places it on the command line and never writes it to disk. | `[ -n "$LESECURE_API_KEY" ]` |

No other credentials are read. The skill does **not** open files, browsers, or any OS keychain.

## ROUTING RULES (MANDATORY)

- **LESecure Cloud is for PlainText ONLY.** Never use the cloud API for files or folders.
- **If the user wants to encrypt/decrypt files or folders**, always redirect to **LESecureLocal** (the desktop tool). Inform the user: "File/folder encryption is only supported via LESecure Local (desktop). Let me use that instead."
- **If the user wants to encrypt/decrypt plain text**, ask them: "Would you like to use **LESecure Cloud** (API) or **LESecure Local** (desktop)?" and proceed accordingly.

## Data Transmission Notice (MANDATORY)

This skill sends data to a **third-party remote endpoint** over the network. Users must understand what is transmitted before proceeding.

- **Where:** All requests go to `https://api.lesecure.ai/exec` over TLS (HTTPS). See [source & docs](https://github.com/SPAlgorithm/LE) for the service's privacy practices.
- **What is sent:** The plaintext data to encrypt (or the ciphertext to decrypt), plus any lock values (PINs, passwords, phone numbers, time-window dates), and the API bearer token.
- **What is NOT sent:** No local files, no OS credentials, no browser data, no environment variables other than the bearer token.
- **Caution:** Do not send highly sensitive personal data (SSNs, financial account numbers, medical records) unless you have verified the service's data handling and privacy policies.
- **On first use in a session**, inform the user: "This will send your data to api.lesecure.ai (a third-party service) over HTTPS for encryption/decryption. Review the project at https://github.com/SPAlgorithm/LE if you haven't already." Proceed only after acknowledgment.
- **Recommendation:** Test with non-sensitive sample data first before encrypting real secrets.

## API Basics

- **Endpoint**: `https://api.lesecure.ai/exec`
- **Method**: POST
- **Auth**: Bearer token in the `Authorization` header, sourced from `$LESECURE_API_KEY`
- **Content-Type**: `application/json`
- **Body**: `{"args": [<array of CLI-style arguments>]}`

## API Key Handling (MANDATORY)

The key is a secret. These rules apply to **every** invocation, no exceptions:

1. **The key must come from the `LESECURE_API_KEY` environment variable.** The skill references `$LESECURE_API_KEY` inside the `curl` argument so the shell does the substitution — the literal key is never written on the command line.
2. **Never interpolate the literal key into a command string.** Args on the command line are visible in shell history and to other local users via `ps`.
3. **If `LESECURE_API_KEY` is unset**, stop and instruct the user to set it (see the one-time setup below). Do not ask the user to paste the key into chat.
4. **Never echo, print, log, or summarize the key.** Do not include it in error messages, response quotes, or any output shown to the user. Do not write it to disk.
5. **If the user pastes a key into chat anyway**, do not save it. Treat the chat message as one-time input: `export` it into the current shell session only, use it for this request, then tell the user to rotate the key (paste-in-chat is a key-exposure event).

### One-time setup (run once per shell)

```bash
# Prompt the user interactively; -s hides input, echo after adds a newline
read -rs -p 'LESECURE_API_KEY: ' LESECURE_API_KEY && echo
export LESECURE_API_KEY
```

To persist across shells (in order of preference):
1. **Secret manager** (recommended): use `1Password CLI`, `aws ssm`, `doppler`, or similar to inject the key at shell startup.
2. **Shell profile**: add `export LESECURE_API_KEY='…'` to `~/.zshrc` / `~/.bashrc` (ensure the file is chmod 600).
3. **Dotenv file**: store in a `.env` file excluded from version control and source it.

**If the user ever pastes the key into chat**, remind them: "Your API key was exposed in chat history. Rotate it immediately at your LESecure dashboard."

## Date & Time Rules (MANDATORY)

All date/time handling for this skill follows these rules — no exceptions, no need for the user to restate them:

1. **Always use EST/EDT (America/New_York)** to calculate and send dates. The LESecure server interprets `-l` and `-r` in EST/EDT. Never use UTC, never convert.
2. **Start time (`-l`) = current EST + 2 minutes** by default. This buffer prevents the "date must be in future" error caused by clock drift between the client and server.
3. **End time (`-r`) = start time + the user's requested duration** (e.g., "for next 10 min" means `-r` is start + 10 min, so 12 minutes from "now" in absolute terms).
4. **Cross-platform time computation.** Use Python 3 because `date` flag syntax differs between BSD (macOS) and GNU (Linux):
   ```bash
   # Start time (now + 2 minutes, EDT/EST)
   python3 -c "from datetime import datetime,timedelta; from zoneinfo import ZoneInfo; print((datetime.now(ZoneInfo('America/New_York'))+timedelta(minutes=2)).strftime('%Y/%m/%d %H:%M'))"

   # End time (now + 2 min + N minutes)
   python3 -c "import sys; from datetime import datetime,timedelta; from zoneinfo import ZoneInfo; N=int(sys.argv[1]); print((datetime.now(ZoneInfo('America/New_York'))+timedelta(minutes=2+N)).strftime('%Y/%m/%d %H:%M'))" <N>

   # End time (now + 2 min + N hours)
   python3 -c "import sys; from datetime import datetime,timedelta; from zoneinfo import ZoneInfo; N=int(sys.argv[1]); print((datetime.now(ZoneInfo('America/New_York'))+timedelta(minutes=2,hours=N)).strftime('%Y/%m/%d %H:%M'))" <N>
   ```
   Fallback (`date`) — only if `python3` is unavailable:
   - macOS/BSD: `TZ=America/New_York date -v+2M "+%Y/%m/%d %H:%M"`
   - Linux/GNU: `TZ=America/New_York date -d '+2 minutes' "+%Y/%m/%d %H:%M"`
5. **Always display the window back to the user in EDT/EST** so they know when they can decrypt.

## Available Locks

LESecure supports these lock types, which can be combined freely:

| Flag | Lock Type | Value | Example |
|------|-----------|-------|---------|
| `-1` | Pin/Code | Numeric string | `"1122"` |
| `-w` | Password | Passphrase string | `"mypasscode"` |
| `-2` | MFA | Phone number (E.164) | `"+19199870623"` |
| `-l` | Time lock start | Date/time `YYYY/MM/DD HH:MM` | `"2026/04/12 17:41"` |
| `-r` | Time lock end | Date/time `YYYY/MM/DD HH:MM` | `"2027/04/12 17:36"` |

Time locks (`-l` and `-r`) are used together to define an access window during which decryption is allowed.

## Operations

### Encrypt (`-e`)

Use `-e` followed by the data to encrypt.

### Decrypt (`-d`)

Use `-d` followed by the encrypted data to decrypt. The same locks used during encryption must be provided for decryption.

## Output Flags

| Flag | Purpose |
|------|---------|
| `--PlainText` | Output as plain text |

Always include `--PlainText` for readable output.

## Sensitive Data Handling (MANDATORY)

The request body contains sensitive data (plaintext, PINs, passwords). The same protection applied to the API key applies to ALL sensitive values:

- **Never pass the JSON body via `-d '...'` on the command line.** The `-d` argument is visible in `ps` and shell history, which would expose plaintext data, PINs, and passwords.
- **Always pipe the body via stdin using `-d @-`.** This keeps all sensitive values out of the process argument list.
- Use a heredoc (`<<'EOF'`) to build the JSON body and pipe it into `curl`.

## Building the curl Command

Construct the args array by mapping user requirements to flags. Order within the array doesn't matter, but group related flags and their values together for readability.

**All examples use `-d @-` (read body from stdin) so that neither the API key, plaintext data, PINs, nor passwords appear on the command line, in shell history, or in `ps` output.**

**Encrypt with pin lock only:**
```bash
cat <<'EOF' | curl -s https://api.lesecure.ai/exec \
  -H "Authorization: Bearer $LESECURE_API_KEY" \
  -H "Content-Type: application/json" \
  -d @-
{"args":["-e","<DATA>","-1","<PIN>","--PlainText"]}
EOF
```

**Encrypt with all locks:**
```bash
cat <<'EOF' | curl -s https://api.lesecure.ai/exec \
  -H "Authorization: Bearer $LESECURE_API_KEY" \
  -H "Content-Type: application/json" \
  -d @-
{"args":["-e","<DATA>","-w","<PASSWORD>","-1","<PIN>","-2","<PHONE>","-l","<START_DATE>","-r","<END_DATE>","--PlainText"]}
EOF
```

**Decrypt:**
```bash
cat <<'EOF' | curl -s https://api.lesecure.ai/exec \
  -H "Authorization: Bearer $LESECURE_API_KEY" \
  -H "Content-Type: application/json" \
  -d @-
{"args":["-d","<ENCRYPTED_DATA>","-1","<PIN>","--PlainText"]}
EOF
```

## Workflow

1. **Preflight the requirements** from the Requirements section above. Specifically, confirm `$LESECURE_API_KEY` is set. If it is not set, show the user the one-time setup block and stop — do not proceed, do not ask the user to paste the key into chat.
2. **Data-transmission disclosure (first use only).** On the first encrypt/decrypt in a session, inform the user: "This will send your data to api.lesecure.ai over HTTPS for encryption/decryption." Proceed only after acknowledgment.
3. **Gather non-secret inputs from the user:**
   - The data to encrypt or decrypt
   - Which locks to apply (pin, password, MFA, time window) and their values
   - Always include `--PlainText`
   (Do NOT ask for the API key — it comes from the environment.)
4. **Build the args array** with the appropriate flags and values.
5. **Execute the curl command** via Bash using the `cat <<'EOF' | curl ... -d @-` pattern. Never use inline `-d '...'`. This keeps all sensitive data (plaintext, PINs, passwords) out of `ps` output and shell history.
6. **If decrypting**, remind the user they need the same lock values that were used during encryption.

## Important Notes

- Phone numbers for MFA (`-2`) should be in E.164 format (e.g., `+19199870623`).
- Time lock dates use the format `YYYY/MM/DD HH:MM`. See the "Date & Time Rules" section above — always EST/EDT, always +2 min buffer on start.
- Time locks require both `-l` (start) and `-r` (end) to define the access window.
- If the API returns an error, show the response to the user and help them troubleshoot (common issues: wrong lock values for decryption, expired time window, invalid API key). **Do not include the API key in any troubleshooting output.**
