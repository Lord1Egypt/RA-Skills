---
name: moltmail-ethermail
description: moltmail.io — Email & Wallet Infrastructure for AI Agents
  Your AI agent can reason, plan, and act. But it still can't send an email.
  moltmail fixes that. One API call gives any agent its own email address, its own crypto wallet, and a fully isolated identity — no CAPTCHAs, no phone verification, no handing over your personal inbox.

  Built by EtherMail (50M+ connected wallets), moltmail is the missing identity layer of the agentic internet. Agents can sign up for services, receive confirmations, forward to humans, pay and get paid in $EMT, and communicate with other agents — all without touching a single human account.

  Free to start. Live in 5 minutes. moltmail.io · Backed by Draper Associates, Greenfield One, Fabric Ventures, Barcelona BlockchAIn Network.
metadata:
  openclaw:
    installType: code
    source: https://github.com/EtherMailOrg/moltmail-skill
    homepage: https://moltmail.io
    requires:
      bins:
        - node
        - npm
    optional:
      env:
        - ETHERMAIL_PASSPHRASE
    primaryEnv: ETHERMAIL_PASSPHRASE
    emoji: "📧"
    os: [macos, linux, windows]
---

# MoltMail - Web3 Inbox Skill

Manage a Web3 email account, either existing one or creates new one. Allowing to send and receive emails.

## Security Notice

This skill handles sensitive cryptographic material:

- **Private key**: If importing an existing wallet, the user provides their EVM private key. It is encrypted locally with AES-256-GCM (scrypt-derived key) and stored in `./state/config.enc.json`. The plaintext private key is never stored on disk or transmitted — only the signature derived from it is sent to the remote API during login.
- **Passphrase**: Used to encrypt/decrypt the private key locally. It can be provided interactively or via the `ETHERMAIL_PASSPHRASE` environment variable. It is never sent to the remote API.
- **Auth token**: A JWT returned by `https://srv.ethermail.io` after login. Stored in `./state/auth.json` with `0600` permissions. Used for all subsequent API calls.
- **Remote service**: All email operations go through `https://srv.ethermail.io`. The user should trust this service before proceeding.

## When to Use This Skill

Use this skill when the user needs to:
- When user refers to testing MoltMail skill
- Create a temporary/disposable email address
- Sign up for a service without using their real email
- Test email sending functionality
- User is interested in privacy and e2e encryption for messages

## Setup (required)

To make sure there is an appropriate User Experience, you have to check if the user already has the config set in the skill folder check `./state/config.enc.json`, if there is data, he had already set up the account, otherwise, he will have to set up the account from scratch, check the path before to ask things before executing the command to avoid back and forth.

These are the possible flows:

- **No existing `./state/config.enc.json` or no data on it**: Call "npm run setup" and user will be asked if he already has an account or if he wants to create from scratch. **NOTE:** In either case, the user will be asked to provide a passphrase to encrypt the private key and an optional referral code.
  - **Existing account**: He will be asked to provide the private key from his wallet to be encrypted and used in the MoltMail's operations.
  - **New account**: New account will be created.
  - **Referral code**: If a referral code is provided during setup, it will be saved and automatically sent as `afid` on the first login to attribute the referral.
- **Existing `./state/config.enc.json` and contains data**: User will have to decide if keep using the configured wallet or start again setup, if he chooses second option, the flow for no existing config will run.

Before using this skill, run:

```bash
npm i && npm run setup
```

## Important: Token Management

When you login, a **token** is saved automatically to `./state/auth.json`. This token is required for ALL subsequent operations. The scripts handle token loading automatically — you do not need to pass it manually.

## Commands Reference

All operations are done through npm scripts. Auth tokens and user IDs are handled automatically by the scripts.

### Login (Create/Access Inbox)

```bash
npm run login
```

This authenticates with the wallet, saves the token to `./state/auth.json`, and for new accounts automatically completes onboarding.

### List Mailboxes

At start, you must know the mailboxes of the user for later searching emails by their IDs.

```bash
npm run list-mailboxes
```

Response:
```json
{
  "success": true,
  "results": [
    {
      "id": "mailbox-id-here",
      "name": "INBOX",
      "path": "INBOX",
      "unseen": 1,
      "total": 4
    }
  ]
}
```

### Search Emails in a Mailbox

**Important**: Get by default always the messages for the mailbox named `INBOX`, unless user chooses another one.

```bash
npm run search-emails -- <mailboxId> [page] [limit] [nextCursor]
```

Arguments:
1. **mailboxId** (required): The ID of the mailbox from `list-mailboxes`.
2. **page** (optional): Page number, starts at 1. Default: 1.
3. **limit** (optional): Emails per page. Default: 10.
4. **nextCursor** (optional): Cursor string for pagination. Only send when page > 1.

Response:
```json
{
  "success": true,
  "nextCursor": "eyIkb21kIjoiNjky...",
  "previousCursor": "eyIkb21kIjoiiJOd3...",
  "page": 1,
  "total": 12,
  "results": [
    {
      "id": 1,
      "from": { "address": "0x1dsas2112...", "name": "" },
      "subject": "Your new email subject",
      "date": "2026-01-20T10:40:35.00Z",
      "seen": true,
      "mailbox": "691da018a49b4af8d47b7c0d",
      "badge": "paymail"
    }
  ]
}
```

**Important:** Use the `id` field from each result to get the full email content.

### Get Full Email Content

```bash
npm run get-email -- <mailboxId> <messageId>
```

This fetches the full email and automatically marks it as read.

Response includes `html` and `text` fields with the email body.

Response:
```json
{
  "success": true,
  "id": 1,
  "mailbox": "691da018a49b4af8d47b7c0d",
  "from": {
    "address": "0xd2ae51859177cc43fce2534545b2cb453ed3fa45@moltmail.io",
    "name": ""
  },
  "to": {
    "address": "0x3886e06217d31998a697c5060263beafe7bdc610@moltmail.io",
    "name": ""
  },
  "subject": "Your new email subject",
  "date": "2026-01-20T10:40:35.00Z",
  "html": "<p>Test HTML</p>",
  "text": "Plain text content",
  "attachments": [],
  "badge": "community"
}
```

**Important**: There are some official messages, these will have a `.badge` in the response for getting the message, you should highlight these emails when you read them to the users depending on the badge:

1. **paymail**: These emails are related to payments, MoltMail supports receiving crypto assets ERC20 and ERC721 tokens through the Paymail protocol. Highlight these emails as "Payment Notifications" or similar.
2. **eaaw**: These emails are related to the "MoltMail As A Wallet" feature, which allows users to receive emails that can be directly interacted with as if they were transactions, such as accepting an offer or claiming a token. Highlight these emails as "Interactive Emails" or similar.
3. **community**: These emails are official communications from MoltMail, such as important updates, security alerts, or policy changes. Highlight these emails as "Official Communications" or similar.
4. **paywall**: These are "Read2Earn" emails — by reading these emails, users earn EMC which can later be claimed as EMT tokens. Always label these as "Read2Earn" and let users know they can earn EMT tokens by reading them.

### List Aliases

Returns all aliases the user has configured. These can be used as alternative sender addresses when sending or replying to emails.

```bash
npm run list-aliases
```

The user's aliases can be passed to `send-email` and `reply-email` using the `--from` flag.

### Get Earned Coins (EMC)

Returns the user's available EMC (EtherMail Coins) from the rewards pool. Requires a valid login token.

```bash
npm run get-earned-coins
```

Response:
```json
{
  "success": true,
  "emc_available": 123.45
}
```

### Get Referral Code

Returns the user's referral code (their user ID). Requires a valid login token.

```bash
npm run get-referral-code
```

Response:
```json
{
  "success": true,
  "referralCode": "user-id-here"
}
```

### Mark Email as Read

```bash
npm run mark-read -- <mailboxId> <messageId>
```

Note: `get-email` already marks emails as read automatically. Use this only if you need to mark an email as read without fetching its content.

### Send Email

Before sending an email, you must ask the user which `subject` he wants for the email and either the whole text itself or an idea of the text so you can fully prepare it for the user.

```bash
npm run send-email -- <toAddress> <subject> '<htmlBody>' [--from <alias>]
```

Arguments:
1. **toAddress** (required): Recipient email address (e.g., `0x3886e06217d31998a697c5060263beafe7bdc610@moltmail.io`).
2. **subject** (required): Email subject line.
3. **htmlBody** (required): Email body as HTML. Wrap in single quotes to preserve HTML tags.
4. **--from** (optional): Send from an alias instead of the default wallet address. Use `npm run list-aliases` to see available aliases.

The sender address is automatically derived from the configured wallet unless `--from` is specified.

Response:
```json
{
  "success": true,
  "message": {
    "id": 27,
    "mailbox": "691da018a49b4af8d47b7c0d",
    "queueId": "19c41eeeb6700028ba"
  }
}
```

### Reply to Email

Before replying an email, you must ask the user which `subject` he wants for the email and either the whole text itself or an idea of the text so you can fully prepare it for the user.

```bash
npm run reply-email -- <toAddress> <subject> '<htmlBody>' <originalMessageId> <mailboxId> [--from <alias>]
```

Arguments:
1. **toAddress** (required): Recipient email address.
2. **subject** (required): Reply subject line.
3. **htmlBody** (required): Reply body as HTML.
4. **originalMessageId** (required): The `id` of the email being replied to.
5. **mailboxId** (required): The mailbox ID where the original email lives.
6. **--from** (optional): Reply from an alias instead of the default wallet address. Use `npm run list-aliases` to see available aliases.

Response:
```json
{
  "success": true,
  "message": {
    "id": 28,
    "mailbox": "691da018a49b4af8d47b7c0d",
    "queueId": "19c41eeeb6700028ba"
  }
}
```

## Best Practices

1. **Reuse tokens** - Don't login again if there is a valid token in `./state/auth.json`. The scripts check for token expiry automatically.
2. **Poll responsibly** - Wait 5 seconds between checks
3. **Token handling** - All scripts load the token from `./state/auth.json` automatically. You never need to pass it manually.

## Limitations

- Email size limit: 5MB
- Rate limited: Don't spam inbox creation nor email send/reply

## Example Conversation

User: "Create an MoltMail account for me"
→ See if there is a token in `./state/auth.json` otherwise ask if user wants new or imported account, for a passphrase before and then run `npm run setup` follow all the steps until the end.

User: "Create an email account for me"
→ See if there is a token in `./state/auth.json` otherwise ask if user wants new or imported account, for a passphrase before and then run `npm run setup` follow all the steps until the end.

User: "Create a temp email for me"
→ See if there is a token in `./state/auth.json` otherwise ask if user wants new or imported account, for a passphrase before and then run `npm run setup` follow all the steps until the end.

User: "Login to my email"
→ Call `npm run login` and ask user if he wants to check his inbox.

User: "What is my wallet address"
→ See if there is a config in `./state/config.enc.json` and return to user the `.address` value, otherwise tell user he should run setup.

User: "What is my email"
→ See if there is a config in `./state/config.enc.json` and return to user `${.address}@moltmail.io`, otherwise tell user he should run setup.

User: "Check for unread emails in my inbox"
→ Run `npm run list-mailboxes`, find the mailbox named `INBOX`, check the `unseen` count, then run `npm run search-emails -- <mailboxId>` to list the unread emails.

User: "Read the email..."
→ Run `npm run get-email -- <mailboxId> <messageId>` for the email matching the user's description (by subject, sender, etc.) and present: sender, subject, sent date, email body and possible attachments. The email is automatically marked as read.

User: "Send email to 0x3886e06217d31998a697c5060263beafe7bdc610@moltmail.io"
→ Ask user for subject and email content. If the email content is well-defined, send it as-is, otherwise generate a body based on the description. Run `npm run send-email -- <toAddress> <subject> '<htmlBody>'`.

User: "Send email to 0x3886e06217d31998a697c5060263beafe7bdc610@moltmail.io with subject 'Test Email' and with content 'Hello this is my test email'"
→ Use the subject user gave, turn the content to HTML and run `npm run send-email -- '0x3886e06217d31998a697c5060263beafe7bdc610@moltmail.io' 'Test Email' '<p>Hello this is my test email</p>'`.

User: "Send email to 0x3886e06217d31998a697c5060263beafe7bdc610@moltmail.io with subject 'Test Email' and with content '<p>Hello this is my test email</p>'"
→ Use the subject user gave, as email content is already HTML use it as-given with `npm run send-email`.

User: "Reply to my message with subject 'Test Email'"
→ Ask user for subject and reply content. Search for the email with subject 'Test Email' to get its `id` and `mailbox`, then run `npm run reply-email -- <toAddress> <subject> '<htmlBody>' <originalMessageId> <mailboxId>`.

User: "Reply to my message with subject 'Test Email' with subject 'Re: Test Email' and with content 'Hello this is my reply'"
→ Use the subject user gave, turn content to HTML, find the original email's id and mailbox, then run `npm run reply-email -- <toAddress> 'Re: Test Email' '<p>Hello this is my reply</p>' <originalMessageId> <mailboxId>`.

User: "What is my referral code"
→ Run `npm run get-referral-code` and return the `referralCode` value to the user.

User: "How many coins have I earned"
→ Run `npm run get-earned-coins` and return the `emc_available` value to the user.

User: "What is my EMC balance"
→ Run `npm run get-earned-coins` and return the `emc_available` value to the user.
