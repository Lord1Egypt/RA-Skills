# OpenClaw WhatsApp @Mention Skill

Make WhatsApp @mentions work reliably with **any AI model** in [OpenClaw](https://openclaw.ai).

## The Problem

When OpenClaw bots try to @mention group members in WhatsApp:
- Different AI models output mentions differently (`@John`, `@1234567890`, `@123456789012345`)
- WhatsApp requires a specific format: `@LID` in text + `LID@lid` in the `mentions` array
- Switching models breaks mentions because each model formats them differently

## The Solution

A **model-agnostic patch** that intercepts all outgoing messages and automatically:

1. Converts `@Name` → `@LID` (using a local LID cache)
2. Converts `@PhoneNumber` → `@LID`  
3. Keeps `@LID` as-is
4. Builds the correct Baileys `mentions` array with `LID@lid` format

The AI model just needs to write `@Someone` — the patch handles the rest.

## How It Works

```
AI outputs: "Hello @John @Jane Doe!"
                    ↓ patch intercepts
LID Cache lookup: John → 123456789012345
                    ↓
Sent to WhatsApp: text="Hello @123456789012345 @987654321098765!"
                  mentions=["123456789012345@lid", "987654321098765@lid"]
                    ↓
WhatsApp renders: Blue clickable @mentions ✅
```

## Installation

### Via ClawHub (recommended)

```bash
openclaw skills install whatsapp-mention
```

### Manual Install

```bash
# 1. Clone and review the code first
git clone https://github.com/junwei1213/openclaw-mention-skill.git
cd openclaw-mention-skill

# 2. Review install.sh before running — it patches OpenClaw core files
cat install.sh

# 3. Run the installer
bash install.sh
```

> **Note:** This skill patches OpenClaw's `deliver-reply` and `login` files. Backups are created automatically before patching. Run `bash uninstall.sh` to restore originals.

## What Gets Installed

| File | Purpose |
|------|---------|
| `deliver-reply` patch | Intercepts outgoing messages, converts @mentions |
| `login` patch | Makes `reply()` accept `{text, mentions}` objects |
| `LID_CACHE.json` | Maps names/phones/aliases to WhatsApp LIDs |
| `mention-guide.md` | AI memory file with LID lookup table |

## Configuration

### LID Cache

The skill auto-discovers group member LIDs when messages are received. You can also manually add members:

```bash
# View current cache
cat /home/openclaw/.openclaw/workspace/LID_CACHE.json | python3 -m json.tool

# Add a member manually
node add-member.js --lid 123456789012345 --name "John" --phone 1234567890 --group "120363400000000000@g.us"
```

### Finding a Member's LID

If a member's LID isn't auto-discovered, check Baileys' LID mapping files in your WhatsApp credential directory. The filename pattern is `lid-mapping-<LID>_reverse.json` and contains the phone number.

### AI Memory

The installer creates `mention-guide.md` in the bot's memory directory. Edit it to add/update member LIDs:

```bash
nano /home/openclaw/.openclaw/workspace/memory/mention-guide.md
```

## Compatibility

- **OpenClaw**: 2026.3.x+
- **Baileys**: Built-in (bundled with OpenClaw)
- **AI Models**: Works with ALL models (Claude, GPT, Qwen, Gemma, etc.)
- **Node.js**: 18+

## Important Notes

- **OpenClaw updates will overwrite patches.** Re-run `install.sh` after updating OpenClaw.
- The `const chunk` in OpenClaw's delivery loop is automatically fixed to `let chunk` by the installer.
- LIDs are WhatsApp's internal user identifiers (not phone numbers). They look like `123456789012345`.

## Technical Details

### Why LID format?

WhatsApp's mention system requires:
1. Text contains `@IDENTIFIER` where IDENTIFIER matches a JID prefix
2. `mentions` array contains full JIDs (`IDENTIFIER@lid` or `IDENTIFIER@s.whatsapp.net`)

Only `@LID_NUMBER` in text + `LID@lid` in mentions produces **blue clickable mentions**. Using `@Name` in text does NOT work even with correct mentions array.

### Patch Architecture

```
deliverWebReply()
  └─ for each text chunk:
      └─ _LID_PATCH_V10:
          ├─ @name → lookup _names/_aliases → @LID + add to mentions
          ├─ @phone → lookup phone→LID map → @LID + add to mentions  
          ├─ @LID (already) → add to mentions
          └─ msg.reply({ text, mentions }) → sendTrackedMessage → Baileys
```

## License

MIT

## Credits

Built for [OpenClaw](https://openclaw.ai) by [InstallMyClaw](https://installmyclaw.com).
