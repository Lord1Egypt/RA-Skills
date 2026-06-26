---
name: whatsapp-mention
slug: whatsapp-mention
description: Model-agnostic WhatsApp @mention skill for OpenClaw. Converts @Name, @Phone, @LID to blue clickable WhatsApp mentions with any AI model.
version: 1.0.2
author: InstallMyClaw
license: MIT
repository: https://github.com/junwei1213/openclaw-mention-skill
tags:
  - whatsapp
  - mention
  - baileys
  - group
metadata:
  openclaw:
    requires:
      bins:
        - node
        - bash
        - python3
      channels:
        - whatsapp
---

# WhatsApp @Mention Skill

Make WhatsApp @mentions work reliably with **any AI model** in OpenClaw.

## What it does

Intercepts all outgoing WhatsApp messages and automatically converts mentions to the correct format:

- `@Name` → `@LID` (blue clickable mention)
- `@PhoneNumber` → `@LID` (blue clickable mention)
- `@LID` → kept as-is (already correct)

## Installation

```bash
openclaw skills install whatsapp-mention
```

Or manually:

```bash
git clone https://github.com/junwei1213/openclaw-mention-skill.git
cd openclaw-mention-skill
bash install.sh
```

## How to use

Just write `@someone` in your messages. The skill handles the rest.

The LID cache at `/home/openclaw/.openclaw/workspace/LID_CACHE.json` maps names to WhatsApp LIDs. Members are auto-discovered when they send messages in groups.

### Add a member manually

```bash
node add-member.js --lid 123456789012345 --name "John" --phone 1234567890
```

### Find a missing LID

Check Baileys' LID mapping files in your WhatsApp credential directory. Filenames follow the pattern `lid-mapping-<LID>_reverse.json`.

## Re-install after OpenClaw updates

OpenClaw updates overwrite patched files. Re-run `install.sh` after updating.

## Uninstall

```bash
bash uninstall.sh
```
