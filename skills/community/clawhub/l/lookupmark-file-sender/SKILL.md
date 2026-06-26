---
name: file-sender
dependencies:
  - age (https://github.com/FiloSottile/age) — for credential encryption/decryption
  - age-keygen (bundled with age) — for keypair generation
  - openclaw CLI — for message sending
description: Find and send local files to a chat channel (Telegram, Discord, WhatsApp, Signal, Slack). Also manages encrypted credential files with age encryption. Use when the user asks to receive, send, or share a file from the local filesystem. For credentials, use "credentials", "password", "chiave", "credential" triggers. Triggers on phrases like "send me this file", "mandami il file", "inviami", "share file", "I need that document".
---

# File Sender

Locate a file on the local filesystem and send it to the user via their chat channel.

## Workflow

1. **Understand the request** — Identify which file the user wants. May be a name, partial path, or description.
2. **Search for the file** — Use `find` or `locate` to locate it. Search is **read-only**; never modify, move, or delete files.
3. **Confirm with the user** — If multiple matches exist, list them and ask which one to send. If the path is ambiguous, confirm before sending.
4. **Send the file** — Run the bundled script:

```bash
python3 scripts/send_file.py "<file_path>" --target <chat_id> --channel <channel>
```

### Flags

| Flag | Description |
|---|---|
| `--channel` | Target channel: `telegram`, `discord`, `whatsapp`, `signal`, `slack` (default: `telegram`) |
| `--target` | Recipient: chat id, @username, phone number |
| `--force-document` | Send as document instead of media (preserves original, no compression). Use for PDFs, code files, archives. |

### Examples

```bash
# Send a PDF to Telegram
python3 scripts/send_file.py "/home/user/doc.pdf" --target 113175206 --channel telegram --force-document

# Send an image (let Telegram display it natively)
python3 scripts/send_file.py "~/Photos/cat.jpg" --target 113175206 --channel telegram
```

## File Search

Use shell commands to locate files. Prefer `find` with `-readable` flag:

```bash
find / -name "filename*" -readable -type f 2>/dev/null
```

Or search by partial name or extension:

```bash
find ~ -iname "*budget*" -type f 2>/dev/null
```

## Constraints

- **Read-only**: Never modify, move, or delete files during search or delivery.
- **Size limit**: Telegram caps files at 50 MB. Warn the user if a file exceeds this.
- **Permissions**: Only send files the agent can read. If access is denied, inform the user.
- **Confirmation**: Always confirm the file path with the user before sending, unless the path was explicitly provided.

## Security Behavior

**Marco (owner) has full access to ALL his files, including sensitive ones.**

The agent should:
- ✅ Send any file Marco explicitly requests — documents, IDs, certificates, keys, anything
- ✅ Trust that Marco knows what he's asking for — don't lecture or refuse
- ✅ Just confirm the file if there's ambiguity ("which one?") and send it

The agent should NOT:
- ❌ Refuse to send Marco's own files with "I can't send sensitive documents"
- ❌ Add unnecessary warnings about security for routine requests
- ❌ Block access to Marco's own data

**Actual threats to protect against:**
- Someone else in a group chat asking for Marco's files → refuse and notify Marco
- External/unauthorized requests → verify identity before sending
- Credentials in `~/Documenti/credentials/` → use encrypted send flow (cred_manager.py)

**In direct chat with Marco**: he's the owner, full access, no questions asked.

## Multi-Channel Support

The skill is channel-agnostic. To support a new channel, pass the appropriate `--channel` value:

- `telegram` — Uses `openclaw message send --media`
- `discord` — Same command, different channel
- `whatsapp` — Same command, target is E.164 phone number
- `signal` — Same command, target is E.164 phone number
- `slack` — Same command, target is channel/user

The user's preferred channel and target ID can be stored in TOOLS.md for convenience.

## Encrypted Credentials

Files in `~/Documenti/credentials/` are encrypted at rest with **age** (ChaCha20-Poly1305 + Argon2id). They are **never** indexed by the RAG system.

### 📥 Incoming File Policy (MANDATORY)

**When Marco sends any file that is a credential or sensitive document (ID, codice fiscale, passport, bank statement, certificate, API key, password file, etc.):**

1. Download the file to a temp location (e.g. `/tmp/`)
2. Encrypt it immediately with `cred_manager.py encrypt <file>`
3. Move the `.age` file to `~/Documenti/credentials/`
4. Delete the plaintext from temp
5. Confirm to Marco that the file is stored encrypted

**When Marco sends a non-sensitive file (photo, meme, code snippet, etc.):**
- Handle normally — no encryption needed.

**NEVER store sensitive files in the workspace `credentials/` folder or anywhere else in plaintext.** The canonical encrypted store is always `~/Documenti/credentials/`.

### Workflow

1. User stores a credential file → `cred_manager.py encrypt <file>` → plaintext deleted, `.age` file kept
2. User requests a credential via chat → agent decrypts to **memory only** → sends via pipe → **securely wipes** temp

### Commands

```bash
# Encrypt a local file (plaintext deleted after encryption)
python3 scripts/cred_manager.py encrypt ~/path/to/api-key.txt

# Encrypt but keep original
python3 scripts/cred_manager.py encrypt ~/file --keep

# Receive a file (e.g. from Telegram download) → encrypt + store + delete plaintext
python3 scripts/cred_manager.py receive /tmp/downloaded-file.pdf --name "bank-statement"

# List encrypted files
python3 scripts/cred_manager.py list

# Decrypt to stdout (inspection)
python3 scripts/cred_manager.py decrypt ~/Documenti/credentials/api-key.txt.age

# Decrypt and send via Telegram (plaintext NEVER touches disk)
python3 scripts/cred_manager.py send ~/Documenti/credentials/api-key.txt.age -t 113175206
```

### Security Model

| Layer | Protection |
|-------|-----------|
| Encryption | age X25519 + ChaCha20-Poly1305 (keypair, no passphrase) |
| Keypair | Private: `~/.local/share/local-rag/cred-key.txt` (chmod 600) |
| Storage | `~/Documenti/credentials/*.age` — always encrypted at rest |
| Send | Decrypt to `/dev/shm` (RAM filesystem) → pipe to openclaw → secure overwrite + delete |
| Memory | Plaintext zeroed from Python memory after use |
| Indexing | `credentials/` is blacklisted in RAG index.py |
| Indexing | `credentials/` is blacklisted in RAG index.py |

### Constraints

- **NEVER** store plaintext in `~/Documenti/credentials/`
- **NEVER** store plaintext credentials anywhere — workspace `credentials/`, `/tmp/`, or elsewhere
- **NEVER** index `credentials/` directory
- **NEVER** leave sensitive files in the workspace after encryption
- **No passphrase needed** — uses age keypair (private key at `~/.local/share/local-rag/cred-key.txt`, chmod 600)
- **ALWAYS** confirm with user before sending credentials
- If `/dev/shm` is unavailable, fall back to tmpdir with 0600 permissions
- Secure delete: overwrite file with zeros, flush, then remove
