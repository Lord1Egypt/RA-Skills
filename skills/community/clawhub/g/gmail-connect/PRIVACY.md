# Gmail Connect privacy and access

Gmail Connect runs under your Ubuntu account. Each installer supplies their own Google Cloud project and OAuth Desktop client. The publisher does not operate a shared OAuth client or credential server.

## Permissions

- `https://www.googleapis.com/auth/gmail.readonly`: profile verification, search, plain-text reads, and inbox history checks.
- `https://www.googleapis.com/auth/gmail.send`: optional; sending is available only after you enable it, authorize it, and review the exact message in the local wizard.

The agent CLI can prepare local drafts but has no send command. Drafts are stored locally rather than in Gmail. Mailbox deletion, label editing, and attachment handling are not implemented.

## Local storage

Private state defaults to `~/.local/share/openclaw-gmail-connect/`. It contains the imported OAuth client, OAuth tokens, cached mail metadata/events, and local drafts. The directory uses owner-only permissions and credential files use mode `0600`. Files are not encrypted at rest, and processes running as your user can access them. Keep any `GMAIL_CONNECT_HOME` override outside the installed skill folder and out of Git.

The recent-events feed is bounded to 5,000 records and 30 days. It is not a complete mail archive. Searches and reads call Gmail directly. Review the installed code for exact retention and disconnect behavior.

## Network and browser

Account authorization uses Google OAuth with PKCE and state. Authenticated requests go to Google's OAuth and Gmail API endpoints. Setup links open Google Cloud Console and Google Account settings. The local wizard binds to `127.0.0.1` and protects API calls with a per-launch capability. Its private URL must stay private.

Email displays as text; the UI does not execute email HTML or load remote images. Gmail Connect does not configure telemetry or send mail content to the publisher. If your OpenClaw agent reads and summarizes email, its configured model provider and delivery destinations may receive that content under your OpenClaw configuration.

## Disconnect and recover

Use **Disconnect & clear local mail** in the wizard to clear account state, cached mail, and local drafts. Stop the optional monitor if you enabled it. Revoke the OAuth grant from [Google Account connections](https://myaccount.google.com/connections). Follow [operations](references/operations.md) before removing residual client files or uninstalling.

External Google OAuth apps in Testing may need reauthorization after seven days. This preview has not completed live Ubuntu/Gmail acceptance or a ClawHub audit. Report problems through [GitHub issues](https://github.com/svetlyoh/web-wallet/issues), using redacted diagnostics without tokens, client JSON, email contents, or private wizard links.
