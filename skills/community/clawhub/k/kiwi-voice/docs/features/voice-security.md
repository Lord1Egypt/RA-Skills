# Voice Security

Kiwi implements **two-layer security** that catches dangerous commands both before and after they reach the LLM.

## Layer 1: Pre-LLM Filter (Kiwi)

Before any command is sent to the LLM, Kiwi's `DangerousCommandDetector` analyzes it:

1. **Speaker identification** — determines who is speaking via voiceprint
2. **Command classification** — regex-based patterns classify commands into severity levels:

| Level | Examples | Owner | Friend | Guest |
|-------|----------|-------|--------|-------|
| `SAFE` | "What time is it?", "Tell me a joke" | Pass | Pass | Pass |
| `WARNING` | "Open the garage door" | Pass | Telegram approval | Telegram approval |
| `DANGEROUS` | "Delete all files", "Format disk" | Pass | Telegram approval | Blocked |
| `CRITICAL` | "rm -rf /", "Drop database" | Pass | Blocked | Blocked |

3. **Telegram approval** — for non-owner speakers, dangerous commands trigger a Telegram message to the owner with Approve/Deny buttons

### Security Patterns

Dangerous command patterns are defined per-language in locale files (`kiwi/locales/*.yaml` → `security_patterns` section), plus universal patterns that work across all languages.

Examples:
```yaml
security_patterns:
  dangerous:
    - "(?i)(delete|remove|destroy)\\s+(all|every)"
    - "(?i)(format|wipe)\\s+(disk|drive|partition)"
  critical:
    - "(?i)rm\\s+-rf"
    - "(?i)drop\\s+(database|table)"
  universal:
    - "(?i)(sudo|chmod|chown)\\s+"
    - "(?i)(shutdown|reboot|poweroff)"
```

## Layer 2: Post-LLM Filter (OpenClaw)

Even if a command passes the pre-filter, the actual shell execution still requires approval:

1. User gives a voice command → passes pre-filter → reaches the LLM
2. LLM decides to run a shell command via the `exec` tool
3. OpenClaw Gateway broadcasts an `exec.approval.requested` event
4. Kiwi receives the event and:
    - **Announces** the command to the owner via voice: *"The agent wants to run: git push origin main"*
    - **Sends** a Telegram message with Approve/Deny buttons
5. Owner responds by voice ("allow" or "deny") or via Telegram
6. Kiwi sends the decision back to OpenClaw via `exec.approval.resolve`
7. If no response within 55 seconds → **auto-deny**

!!! warning "Defense in depth"
    Even if someone bypasses the voice pre-filter (e.g., by crafting a prompt that doesn't trigger regex patterns), the post-filter catches the actual dangerous action at execution time.

## Telegram Setup

### Create a Bot

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow the prompts
3. Copy the bot token

### Get Your Chat ID

1. Message your new bot
2. Visit `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. Find `"chat":{"id":123456789}` in the response

### Configure

```bash
# .env
KIWI_TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
KIWI_TELEGRAM_CHAT_ID=123456789
```

```yaml
# config.yaml
security:
  telegram_approval_enabled: true
```

### Approval Flow

When a non-owner says something dangerous:

1. Kiwi announces: *"[Speaker name] wants to: [command]. Waiting for approval."*
2. Owner receives a Telegram message with the command text and two buttons: **Approve** / **Deny**
3. Owner taps a button → Kiwi executes or rejects the command
4. If no response → auto-deny after timeout
