---
name: outlook-hack
version: 3.4.2
description: "Read and search Outlook, inspect attachments, and create or edit drafts without any send endpoint. Uses one short-lived Microsoft Graph access token supplied on stdin for one run; it never stores credentials. Bulk mailbox export is opt-in."
metadata:
  openclaw:
    emoji: "📧"
    os: ["linux", "darwin"]
    requires:
      capabilities: ["network", "file_write"]
    permissions:
      network: "Credentialed HTTPS requests only to graph.microsoft.com; enforced by a runtime allowlist."
      file_write: "No credential storage. Optional mailbox exports require --yes and use mode 0600 files inside a mode 0700 directory."
      mail_write: "Can create and patch drafts. No send, reply-to-network, forward-to-network, move, flag, or delete operation is shipped."
---

> Part of **[TinkerClaw](https://github.com/globalcaos/tinkerclaw)**.

# Outlook — read, search, and draft; never send

This skill reads Outlook mail and creates or edits drafts through Microsoft Graph. The shipped client has no send endpoint. It does not install packages, run subprocesses, store credentials, contact telemetry services, or transmit mailbox data anywhere except Microsoft Graph.

## What ships

One zero-dependency Node.js client: `scripts/outlook-mail-fetch.mjs`.

It can:
- list recent messages and drafts;
- read a complete message body;
- download attachments to a directory you choose;
- create or patch drafts while preserving the existing signature;
- export mailbox bodies and attachment metadata locally, only with `--fetch-all --yes`.

It cannot send, reply, forward, permanently delete, move, flag, read contacts, or read calendars. Those capabilities are intentionally outside this public package.

## Permissions, data flow, and consent

**Authentication.** Supply a short-lived Microsoft Graph access token on standard input for each invocation. This package does not extract, refresh, print, or store tokens. Obtain the token through a Microsoft-supported login tool or identity flow approved by your organisation, requesting only the mail scopes needed for the command.

**Network boundary.** Every credentialed request is runtime-checked before the token is read. The destination must be exactly `https://graph.microsoft.com` with no user information, custom port, HTTP downgrade, or lookalike subdomain. Pagination URLs are checked by the same function.

**Local mailbox data.** Normal list/read commands print to the current process and do not create a mailbox mirror. Bulk export refuses to run without `--yes`. Export directories are rejected if they are symlinks and forced to mode `0700`; exported bodies, summaries, indexes, and downloaded attachments reject symlink targets and are forced to mode `0600`, including pre-existing paths. Attachment downloads never overwrite an existing file: they allocate a unique name and create it with exclusive `wx`. Message IDs are restricted to Graph-safe characters and encoded before they enter a URL. Data is plaintext at rest.

**No command-line secrets.** The client refuses tokens as command-line arguments. Pipe the access token on stdin so it does not appear in process listings or shell history.

## Commands

```bash
printf '%s' "$OUTLOOK_ACCESS_TOKEN" | node {baseDir}/scripts/outlook-mail-fetch.mjs --test --access-token-stdin
printf '%s' "$OUTLOOK_ACCESS_TOKEN" | node {baseDir}/scripts/outlook-mail-fetch.mjs --list-drafts --access-token-stdin --limit 15
printf '%s' "$OUTLOOK_ACCESS_TOKEN" | node {baseDir}/scripts/outlook-mail-fetch.mjs --get '<message-id>' --access-token-stdin
printf '%s' "$OUTLOOK_ACCESS_TOKEN" | node {baseDir}/scripts/outlook-mail-fetch.mjs --get-attachments '<message-id>' --access-token-stdin --out '<private-dir>'
printf '%s' "$OUTLOOK_ACCESS_TOKEN" | node {baseDir}/scripts/outlook-mail-fetch.mjs --patch-draft '<draft-id>' --body-file body.html --keep-signature --access-token-stdin
printf '%s' "$OUTLOOK_ACCESS_TOKEN" | node {baseDir}/scripts/outlook-mail-fetch.mjs --fetch-all --yes --months 6 --access-token-stdin
```

Review every draft in Outlook before sending it manually. This skill never sends on your behalf.

## Cleanup

Optional exports live under `~/.openclaw/workspace/data/outlook-emails/`. Inspect that directory and remove it with your normal file manager or recovery-aware deletion tool when no longer needed.

Source and issues: **https://github.com/globalcaos/tinkerclaw**
