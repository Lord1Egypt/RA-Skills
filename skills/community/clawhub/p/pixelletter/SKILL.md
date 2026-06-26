---
name: pixelletter
version: 1.0.0
description: Send letters, PDFs, postcards, faxes, registered mail, or query account credit through the PixelLetter HTTPS interface. Use for automating physical mail dispatch via PixelLetter from OpenClaw. External action: real sends can cost money and send postal mail/faxes.
metadata:
  openclaw:
    requires:
      bins:
        - node
    safety: external-action
---

# PixelLetter

Use this skill when a user wants to send or test a letter/PDF/fax through PixelLetter, query PixelLetter account information, or build workflows around PixelLetter's HTTPS API.

## Setup

1. Create a free account at https://www.pixelletter.de
2. Add credit to your account (letters cost approx. €0.79–€1.99 each)
3. Provide credentials via environment variables:

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

4. Test with a dry-run first — no mail is sent, no costs incurred.

## Safety rules

- PixelLetter dispatches real postal mail/faxes and may create costs.
- Default to test mode. Never run a productive send unless the user explicitly confirms the exact recipient, document/text, options, and cost/dispatch intent.
- Never store credentials in the skill or examples. Use environment variables or secret injection:
  - `PIXELLETTER_EMAIL`
  - `PIXELLETTER_PASSWORD`
- Do not expose credentials in logs, dry-runs, commits, screenshots, or community-shared examples.
- Prefer PDF upload for already-rendered letters. Use text mode only for simple letters where PixelLetter handles layout.
- Treat API success code `100` as "transmission accepted", not final delivery. PixelLetter sends final confirmation later by email.

## CLI wrapper

Bundled script: `scripts/pixelletter.mjs`

Run from the skill directory or pass the full script path.

```bash
PIXELLETTER_EMAIL="..." PIXELLETTER_PASSWORD="..." \
node scripts/pixelletter.mjs account
```

### Dry-run a text letter

```bash
node scripts/pixelletter.mjs send-text \
  --address-file /path/address.txt \
  --message-file /path/message.txt \
  --subject "Betreff" \
  --destination DE \
  --dry-run
```

### Test-mode PDF upload (safe, no real dispatch)

```bash
PIXELLETTER_EMAIL="..." PIXELLETTER_PASSWORD="..." \
node scripts/pixelletter.mjs send-upload \
  --file /path/letter.pdf \
  --destination DE
```

### Real dispatch

Only after explicit user confirmation:

```bash
PIXELLETTER_ALLOW_REAL_SEND=true \
PIXELLETTER_EMAIL="..." PIXELLETTER_PASSWORD="..." \
node scripts/pixelletter.mjs send-upload \
  --file /path/letter.pdf \
  --destination DE \
  --production \
  --confirm-real-send
```

## Important options

- `--action 1|2|3`
  - `1` = postal letter only (default)
  - `2` = fax only
  - `3` = postal letter and fax
- `--fax "+49 ..."` is required for action `2` or `3`.
- `--destination DE` is required for postal letter actions `1` or `3`.
- `--location 1|2|3`
  - `1` = München (default)
  - `2` = Hausleiten bei Wien
  - `3` = Hamburg
- `--addoption` registered-mail options, comma-separated:
  - `27` Einschreiben
  - `28` Rückschein, only with `27`
  - `29` Eigenhändig, only with `27`
  - `30` Einschreiben Einwurf, not combinable

## API reference

For endpoint details and response shape, read `references/api.md` only when needed.
