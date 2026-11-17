---
name: glass2claw
description: Route user-selected photos from Meta Ray-Ban glasses or another camera through a configured messaging ingress to an approved specialist and destination. Use only for explicit, opt-in photo routing with allowlisted destinations and confirmation before cross-session forwarding or persistent writes.
metadata:
  openclaw:
    version: "2.3.4"
    emoji: "👁️"
    homepage: https://clawhub.ai/jonathanjing/glass2claw
---

# glass2claw: From Your Eyes to Your Database — Instantly

## 🛠️ Installation

### 1. Ask OpenClaw (Recommended)
Tell OpenClaw: *"Install the glass2claw skill."* Installation does not enable automatic photo forwarding.

### 2. Manual Installation (CLI)
If you prefer the terminal, run:
```bash
openclaw skills install @jonathanjing/glass2claw
```

You're wearing your **Meta Ray-Ban glasses**. You see a wine label, a business card, a tea tin. You say:

> *"Hey Meta, take a picture and send this to myself on WhatsApp."*

That message is an explicit routing request. OpenClaw then previews the detected category and destination before forwarding or saving anything.

The photo lands in your configured ingress. OpenClaw's Vision Router classifies it, asks for confirmation when a cross-session transfer or persistent write is required, and uses only destinations you allowlisted.

**No typing. No app switching. No friction.**

---

## 📸 How It Works

```
Meta Ray-Ban glasses
  → "Hey Meta, take a picture and send this to myself on WhatsApp"
      → Meta AI delivers the photo to your WhatsApp
          → OpenClaw (WhatsApp session) receives the image
              → classifies intent: Wine | Tea | Contacts | Cigar | ...
                  → routes to the matching specialist agent
                      → writes structured entry to your database
```

The capture can be hands-free; external forwarding and persistent writes remain visible and controlled.

---

## 🔧 What You Need to Set Up

This skill is a **routing protocol** — it defines the pattern, not the specific implementation. You bring your own:

- **Meta AI + WhatsApp connection** — enable Meta AI on your Ray-Ban glasses and link it to WhatsApp (one-time setup in the Meta View app)
- **OpenClaw with WhatsApp channel** — your OpenClaw instance needs a WhatsApp session to receive the incoming images
- **Destination databases** — connect whichever databases you want: Notion, Airtable, a local file, a Discord channel. The skill routes to wherever you configure it
- **Database credentials** — set up API access for your chosen database yourself (Notion API key, Airtable token, etc.)

> The skill templates in this package show one reference implementation using Notion + Discord. Adapt them to your own stack.

---

## 🔒 Privacy

This skill processes **photos from your personal camera**. Images flow from WhatsApp → your OpenClaw instance → your configured destination. Any external services you connect (Notion, Discord, etc.) are governed by their own privacy policies. All routing logic runs on your own OpenClaw instance.

- Route only photos the user intentionally submitted.
- Do not route photos of third parties without appropriate consent.
- Allowlist destination session keys; never infer them.
- Show the category and destination before forwarding or writing.
- Keep automatic persistence off unless the user explicitly enables it for a named destination.

---

## 📦 What's Included

- `{baseDir}/SAMPLE_AGENT.md` — reference routing logic for the hub agent
- `{baseDir}/SAMPLE_SOUL_WINE.md` — reference persona for a wine specialist agent

Use these as starting points. Customize for your own categories and destinations.

---

*Created by JonathanJing | AI Reliability Architect*
