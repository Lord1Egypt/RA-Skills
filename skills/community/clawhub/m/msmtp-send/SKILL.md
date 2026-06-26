---
name: msmtp-send
description: Send plain-text emails using your local msmtp config (Gmail app password already set up in ~/.msmtprc). Strictly send-only; no reading, fetching, or inbox access.
command-dispatch: tool
command-tool: exec
metadata:
  openclaw:
    emoji: "✉️"
    requires:
      bins: ["msmtp"]
    homepage: "https://docs.openclaw.ai/tools/skills"  # optional reference
---

## msmtp-send Skill

This skill sends simple emails by executing your local `{baseDir}/send.sh` script via the exec tool. It relies on your existing `~/.msmtprc` for authentication (no new credentials stored here).

### When to use
- Quick notifications, test messages, alerts, or short plain-text emails.
- Recipient is known/trusted.
- Keep bodies concise (plain text only; no attachments/HTML in this minimal version).

### How the agent invokes it
The agent will automatically dispatch to the exec tool with a command like:
