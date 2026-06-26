---
name: cloudflare-mail-address-creator
description: create one or many ordinary mailbox addresses in a cloudflare temporary mail system through the /admin/new_address admin api and return structured results. use when openclaw is asked to create mailbox addresses through the backend instead of the web ui, including requests such as create t2@suilong.online, create 10 mailboxes, add a mailbox in my cloudflare temp mail system, or use the cloudflare mail admin api to create addresses.
---

# Cloudflare Mail Address Creator

Use this skill to create ordinary mailbox addresses through `https://mail-api.suilong.online/admin/new_address`.

## Workflow

1. Collect or infer `name`, `domain`, and `enablePrefix`.
2. Default `enablePrefix` to `true` when the user does not specify it.
3. If the user gives a full address such as `t2@suilong.online`, split it into `name=t2` and `domain=suilong.online`.
4. Never hardcode real credentials in the skill. Read them from runtime environment variables or pass them as CLI flags.
5. Run `python3 scripts/create_address.py` for single or batch creation.
6. Return the script's JSON output directly unless the user asks for a reformatted summary.
7. Preserve the normalized statuses: `created`, `already_exists`, `auth_error`, `error`.
8. If local validation fails, fix the input before attempting the API call again.
9. Use `--output-format csv` and optionally `--output-file <path>` when the user asks for exportable results.

## Commands

Single address:

```bash
python3 scripts/create_address.py \
  --name t2 \
  --domain suilong.online \
  --admin-auth "$CLOUDFLARE_MAIL_ADMIN_AUTH"
```

Single full address:

```bash
python3 scripts/create_address.py \
  --name t2@suilong.online \
  --admin-auth "$CLOUDFLARE_MAIL_ADMIN_AUTH"
```

Batch addresses from a comma-separated list:

```bash
python3 scripts/create_address.py \
  --names alice,bob,charlie \
  --domain suilong.online \
  --enable-prefix true \
  --admin-auth "$CLOUDFLARE_MAIL_ADMIN_AUTH"
```

Batch addresses from a file:

```bash
python3 scripts/create_address.py \
  --names-file ./names.txt \
  --domain suilong.online \
  --admin-auth "$CLOUDFLARE_MAIL_ADMIN_AUTH"
```

Export batch results as CSV:

```bash
python3 scripts/create_address.py \
  --names alice,bob,charlie \
  --domain suilong.online \
  --output-format csv \
  --output-file ./created-addresses.csv \
  --admin-auth "$CLOUDFLARE_MAIL_ADMIN_AUTH"
```

## Runtime Environment

Prefer environment variables for secrets:

- `CLOUDFLARE_MAIL_ADMIN_AUTH`
- `CLOUDFLARE_MAIL_BEARER_TOKEN`
- `CLOUDFLARE_MAIL_FINGERPRINT`
- `CLOUDFLARE_MAIL_LANG`
- `CLOUDFLARE_MAIL_USER_TOKEN`
- `CLOUDFLARE_MAIL_API_URL`

## Supporting Files

- Read `references/api.md` for the endpoint contract and error mapping.
- Read `references/examples.md` for example prompts and outputs.

## OpenClaw Install Notes

Install this skill into an OpenClaw workspace under `skills/cloudflare-mail-address-creator/`, or globally under `~/.moltbot/skills/cloudflare-mail-address-creator/`.

This package intentionally keeps only the OpenClaw-compatible skill files: `SKILL.md`, `scripts/`, and `references/`.
