# Threat Model

## What gmail-no-send Protects Against

1. **Autonomous email sending by AI agents.** The primary threat: an agent with Gmail access decides to send email on behalf of the user without explicit approval. This tool makes that impossible at the code level.

2. **Accidental sends.** No send command = no accidental sends. Drafts can be reviewed in Gmail UI before manual sending.

## What It Does NOT Protect Against

1. **Token reuse.** If an attacker obtains `~/.config/gmail-no-send/token.json`, they can use it with the Gmail API directly (the token has `compose` scope). Mitigate: restrict file permissions (`chmod 600`), encrypt at rest.

2. **Malicious code modification.** Someone could add a send function to the codebase. Mitigate: pin to a known version, verify checksums, review source.

3. **OAuth scope over-privilege.** Gmail's API does not offer a drafts-only OAuth scope. The `compose` scope is the minimum for draft creation, and it technically permits sending. This is a Gmail API limitation, not a tool limitation.

## Why Not a Proxy?

A more robust architecture would be a proxy server that intercepts Gmail API calls and blocks send requests at the network layer. This tool takes the simpler approach: just don't include send code. For most agent use cases (reading email, drafting replies for human review), this is sufficient.

## Audit Trail

All operations are logged to `~/.config/gmail-no-send/audit.log` as newline-delimited JSON with timestamps, action types, and account names. Review periodically.
