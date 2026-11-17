---
name: Intercom Support Channel
description: Set up an autonomous, customer-facing support agent inside an Intercom inbox — WhatsApp, Instagram, Facebook, in-app Messenger, SMS, email. The agent reads customer screenshots and transcribes voice notes, and hands conversations to humans cleanly. Use when someone wants an AI agent that answers Intercom customers directly (not an API helper for operators), wants to automate customer support conversations, or asks to connect OpenClaw to Intercom, WhatsApp support, or Instagram DMs.
---

# Intercom Support Channel

This skill sets up **@othreecodes/openclaw-intercom** — an OpenClaw *channel* plugin where
customers message any surface connected to Intercom (WhatsApp, Instagram, Facebook, in-app
Messenger, SMS, email) and the agent answers them directly: greets, resolves, tags,
annotates, escalates to a human when needed, then stays out of the human's way.

This is different from Intercom API skills, which help an *operator* list conversations or
draft replies on request. This makes the agent the support teammate customers talk to.

## What the plugin handles for you

- Hybrid inbound (polling + webhooks) with crash-safe dedupe — no double replies
- One agent session per conversation; message bursts coalesce into one coherent reply
- Reads customer screenshots (uploads and Instagram inline images) via image understanding
- **Transcribes voice notes** — WhatsApp and Instagram audio reaches the agent as text
  instead of "the customer attached a file"
- Replies render as real HTML: numbered steps, bullets, bold
- Inline actions parsed from the agent's reply: `[[close]]`, `[[escalate: reason]]`,
  `[[note: text]]`, `[[tag: label]]`
- Escalation hands the conversation back to the inbox it came from and permanently mutes
  the agent on it
- **Human ownership is absolute**: once any teammate replies in a conversation, the agent
  takes no further turn in it, even on new customer messages. On a shared team inbox a
  reopened conversation drops back to the queue, and without this the agent walks into
  threads a human is actively working
- Session labels name the channel a conversation came in on (`Ada (WhatsApp)`), so a
  multi-channel inbox stays readable
- First run absorbs the existing backlog instead of answering the whole inbox
- Channel scoping: pilot on one surface (`allowedChannels: ["instagram"]`), widen later

## Setup

1. Install the plugin — **pin the version** so you get exactly the release you reviewed
   (this skill and the plugin share the same publisher, and the package is source-linked
   on ClawHub, so every version maps to a verifiable GitHub commit):

   ```bash
   openclaw plugins install clawhub:@othreecodes/openclaw-intercom@1.0.12
   ```

   Check ClawHub for the latest version and its changelog before upgrading; treat plugin
   upgrades like any other production dependency change.

2. **Get authorization first.** This agent will reply to real customers under a real
   teammate identity — confirm with whoever owns the support workspace before enabling it.

3. In the Intercom Developer Hub, create a **dedicated app** for the bot (don't reuse a
   broader app's token), copy its **Access token**, and grant only what you'll use:
   read/write conversations, plus read contacts and read/write tags if you want those
   features. Keep the token rotatable — you'll want revocation to be one click if
   anything looks wrong.

4. Configure the channel (`~/.openclaw/openclaw.json`, or the OpenClaw dashboard's
   channel settings, where every option renders as a form):

   ```json
   {
     "channels": {
       "intercom": {
         "enabled": true,
         "token": "YOUR_ACCESS_TOKEN",
         "inbound": "both",
         "webhookSecret": "YOUR_APP_CLIENT_SECRET",
         "allowedChannels": ["instagram"]
       }
     }
   }
   ```

   `token` is the only required field. For webhooks, subscribe the app to
   `conversation.user.created` and `conversation.user.replied`, pointed at
   `https://YOUR_GATEWAY/intercom/webhook` — the signing secret is the app's client secret.

5. Restart the gateway. On first run the plugin logs how many existing conversations it
   absorbed without replying; from the next customer message onward the agent answers.

**Roll out in stages.** Start with `allowedChannels` scoped to one low-stakes pilot
channel and `escalationAssigneeId` pointed at a real human team *before* the first
customer message — an autonomous agent without a working hand-off path is not ready for
production. Watch its first days of conversations, then widen the channel list as
confidence grows.

Give the agent a support persona and grounding rules in its workspace `AGENTS.md` —
the plugin carries the messages; the agent's quality comes from its instructions.

Two things worth writing into those instructions before you go live, both learned the hard
way on a production inbox:

- **Never let the agent identify which app a screenshot belongs to.** It will get it wrong
  in both directions — naming a competitor's app, or telling a customer their own genuine
  screen is fake. Have it describe what it sees, believe the customer about their own
  screen, and ask rather than assert.
- **Scope it explicitly to your product.** Without a boundary it will cheerfully answer
  unrelated questions, which is both off-brand and the same weakness an injected
  instruction exploits.

## Full documentation

- Package: `clawhub:@othreecodes/openclaw-intercom` (ClawHub → Packages)
- Source, README and config reference: https://github.com/othreecodes/openclaw-intercom
