# MoltMail Skill for OpenClaw

A Web3 email skill for [OpenClaw](https://openclaw.ai) agents, powered by [MoltMail](https://moltmail.io) and [EtherMail](https://ethermail.io).

Gives your AI agent its own email address and crypto wallet — send/receive emails, manage mailboxes, earn EMC, and more.

## Prerequisites

- Node.js >= 18
- npm

## Installation

```bash
npm install
```

## Setup

Run the interactive setup to create or import a wallet:

```bash
npm run setup
```

You will be prompted to:

1. **Create a new wallet** or **import an existing one** (by providing your private key)
2. **Set a passphrase** to encrypt the wallet locally (AES-256-GCM)
3. **Enter a referral code** (optional)

The encrypted wallet config is stored in `./state/config.enc.json`.

## Login

Authenticate with MoltMail before using any other command:

```bash
npm run login
```

This saves a JWT token to `./state/auth.json`. New accounts are automatically onboarded on first login.

> You can set the `ETHERMAIL_PASSPHRASE` environment variable to skip the interactive passphrase prompt.

## Commands

| Command | Description |
|---|---|
| `npm run login` | Authenticate with MoltMail |
| `npm run list-mailboxes` | List all mailboxes with unread/total counts |
| `npm run search-emails -- <mailboxId> [page] [limit] [nextCursor]` | Search emails in a mailbox |
| `npm run get-email -- <mailboxId> <messageId>` | Get full email content (auto-marks as read) |
| `npm run mark-read -- <mailboxId> <messageId>` | Mark an email as read |
| `npm run send-email -- <to> <subject> '<html>' [--from <alias>]` | Send an email |
| `npm run reply-email -- <to> <subject> '<html>' <msgId> <mailboxId> [--from <alias>]` | Reply to an email |
| `npm run list-aliases` | List configured email aliases |
| `npm run get-referral-code` | Get your referral code |
| `npm run get-earned-coins` | Get your available EMC balance |

## Security

- Private keys are encrypted at rest with AES-256-GCM (scrypt-derived key) and never leave the machine in plaintext
- Auth tokens are stored with `0600` permissions
- All API communication goes through `https://srv.ethermail.io`

## License

Proprietary - EtherMail
