# PixelLetter

Send letters, PDFs, postcards, faxes, and registered mail via the [PixelLetter](https://www.pixelletter.de) HTTPS API — directly from OpenClaw.

## What is this?

[PixelLetter](https://www.pixelletter.de) is a German online service that lets you send physical postal mail and faxes programmatically. You upload a PDF or provide text, specify the recipient, and PixelLetter prints and mails the letter from one of their print centers in Germany (München, Hamburg, or Hausleiten near Vienna).

This skill wraps the PixelLetter HTTPS API with a CLI tool, a safety layer, and OpenClaw agent instructions. It lets your AI agent draft, preview, and — after explicit confirmation — dispatch real letters on your behalf. Useful for:

- Automating formal correspondence (Kündigung, Behördenbriefe, Mahnungen)
- Sending PDFs as registered mail (Einschreiben)
- Fax dispatch as part of a workflow
- Account balance checks before sending

> ⚠️ **External action:** Real sends dispatch physical mail/faxes and incur costs. Always test with `--dry-run` first.

## Features

- Send text letters (address + body as plain text files)
- Upload and send PDF documents
- Send faxes or combined letter+fax
- Registered mail options (Einschreiben, Rückschein, Eigenhändig)
- Query account balance and credit
- Safe by default: test mode unless explicitly overridden
- Secret injection support (Proton Pass, env vars)

## Requirements

- Node.js 18+
- A [PixelLetter account](https://www.pixelletter.de) with credit

## Setup

1. Create an account at https://www.pixelletter.de
2. Add credit (letters cost approx. €0.79–€1.99 each)
3. Provide your credentials via environment variables:

```bash
export PIXELLETTER_EMAIL="your@email.com"
export PIXELLETTER_PASSWORD="yourpassword"
```

Or use secret injection (e.g. Proton Pass):

```bash
PIXELLETTER_EMAIL='pass://Personal/Pixelletter/email' \
PIXELLETTER_PASSWORD='pass://Personal/Pixelletter/password' \
pass-cli run -- node scripts/pixelletter.mjs account
```

## Usage

### Check account balance

```bash
PIXELLETTER_EMAIL="..." PIXELLETTER_PASSWORD="..." \
node scripts/pixelletter.mjs account
```

### Dry-run a text letter (no real dispatch)

```bash
node scripts/pixelletter.mjs send-text \
  --address-file /path/address.txt \
  --message-file /path/message.txt \
  --subject "Betreff" \
  --destination DE \
  --dry-run
```

Address file format (plain text, one field per line):

```
Max Mustermann
Musterstraße 1
12345 Musterstadt
```

### Send a PDF (test mode — safe, no real dispatch)

```bash
PIXELLETTER_EMAIL="..." PIXELLETTER_PASSWORD="..." \
node scripts/pixelletter.mjs send-upload \
  --file /path/letter.pdf \
  --destination DE
```

### Real dispatch

Only after explicit confirmation of recipient, document, and cost:

```bash
PIXELLETTER_ALLOW_REAL_SEND=true \
PIXELLETTER_EMAIL="..." PIXELLETTER_PASSWORD="..." \
node scripts/pixelletter.mjs send-upload \
  --file /path/letter.pdf \
  --destination DE \
  --production \
  --confirm-real-send
```

## Options

| Option | Description |
|--------|-------------|
| `--action 1\|2\|3` | `1` = letter (default), `2` = fax, `3` = letter + fax |
| `--fax "+49 ..."` | Required for action `2` or `3` |
| `--destination CC` | Country code, required for letter actions (e.g. `DE`, `AT`, `CH`) |
| `--location 1\|2\|3` | Print location: `1` = München (default), `2` = Hausleiten, `3` = Hamburg |
| `--addoption LIST` | Registered mail: `27` = Einschreiben, `28` = Rückschein, `29` = Eigenhändig, `30` = Einwurf |
| `--dry-run` | Print XML, do not call PixelLetter |
| `--production` | Disable test mode (requires `--confirm-real-send`) |

## Security

- Never commit credentials — use env vars or secret injection
- Default mode is **test** — PixelLetter logs the request but does not dispatch
- API response code `100` means "accepted", not "delivered" — final confirmation comes by email
- The `--production` flag requires both `--confirm-real-send` and `PIXELLETTER_ALLOW_REAL_SEND=true` as a triple-confirmation safeguard

## License

MIT
