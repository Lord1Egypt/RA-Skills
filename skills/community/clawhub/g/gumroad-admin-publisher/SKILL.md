---
name: "gumroad-admin"
description: "Manage Gumroad and batch-publish digital products with the official CLI."
status: proposal
version: "v3"
date: "2026-06-14T16:57:39.556Z"
---

# Gumroad Admin

Use this skill to administer Gumroad stores and publish digital products safely. Prefer the official `gumroad` CLI for product/file/content workflows because it handles local file upload, local cover images, local thumbnails, and content writes without needing temporary public hosting.

## Requirements

- `gumroad` CLI available on `PATH`.
- `GUMROAD_ACCESS_TOKEN` set in the environment, or run `gumroad auth login`.
- Optional OAuth app values may exist as `GUMROAD_APP_ID` and `GUMROAD_APP_SECRET`, but do not require them for personal store administration.

Never store credentials in skill files, manifests, logs, examples, or Clawhub metadata.

## Safety

Treat Gumroad as a live external commerce system.

- Read-only commands may run when requested.
- Use `--dry-run`, `--json`, `--no-input`, and `--non-interactive` for planning and machine-readable checks.
- Ask for explicit confirmation before product creation, publication, unpublication, deletion, file replacement, content replacement, refunding, receipt resending, license disable/rotate, webhook mutation, or bulk changes.
- For any batch publish, run one product first, verify it fully, then continue.
- Keep resumable manifests in a local state folder outside the skill, for example `state/gumroad-admin/`.
- Do not use public web hosting for local covers/thumbnails when the CLI supports `--cover-image` and `--thumbnail`.
- Do not trust command success until verification confirms product state.

## Quick Checks

```powershell
gumroad auth status --json
gumroad user --json
gumroad products list --json
gumroad products view PRODUCT_ID --json
```

## Product Publishing

For a single local digital product, prefer:

```powershell
gumroad products create --json --no-input --yes \
  --name "Product Name" \
  --price 8.00 \
  --description "<p>HTML description</p>" \
  --custom-summary "Short summary" \
  --file "D:\path\product.zip" \
  --file-name "Product Name.zip" \
  --cover-image "D:\path\cover.jpg" \
  --thumbnail "D:\path\cover.jpg" \
  --tag "t-shirt mockup" \
  --tag "psd mockup"
```

Then verify:

```powershell
gumroad products view PRODUCT_ID --json
```

A complete product should have:

- `published` in the expected state.
- `files` contains the downloadable file.
- `covers` contains at least one cover.
- `thumbnail_url` is present.
- `preview_url` is present.
- `rich_content` contains a `fileEmbed` pointing to a file id. If `rich_content` is empty, buyer-facing Content is empty even if `files` exists.

Publish only after verification if the product was created as a draft:

```powershell
gumroad products publish PRODUCT_ID --json --no-input --yes
```

## Batch Publishing

Use `scripts/gumroad_batch_publish.py` for repeatable local folder batches.

Typical flow:

```powershell
python scripts\gumroad_batch_publish.py manifest --source "D:\Products" --out state\gumroad-admin\products.json --price 8.00
python scripts\gumroad_batch_publish.py plan --manifest state\gumroad-admin\products.json --limit 1
python scripts\gumroad_batch_publish.py publish --manifest state\gumroad-admin\products.json --limit 1 --yes
python scripts\gumroad_batch_publish.py verify --manifest state\gumroad-admin\products.json
python scripts\gumroad_batch_publish.py publish --manifest state\gumroad-admin\products.json --yes
```

The manifest command expects each product archive to have a matching cover image by stem, for example:

```text
Product Folder/
  my-product.zip
  my-product.jpg
```

The script writes product ids and verification status back to the manifest so interrupted batches can resume. It uses the Gumroad CLI for file, cover, thumbnail, and content operations.

## Content Pitfall

Gumroad distinguishes attached files from buyer-facing rich content. A product can have `files` but still show an empty Content section. After product creation, verify `rich_content`. If needed, use:

```powershell
gumroad products content set PRODUCT_ID content.json --json --no-input --yes
```

The JSON should be an array containing a ProseMirror document with a `fileEmbed` whose `attrs.id` is the Gumroad file id returned by `gumroad products view PRODUCT_ID --json`.

## Daily Limits

Gumroad may enforce daily product creation limits. If a batch receives a limit error, stop, keep the manifest checkpoint, and resume after the limit resets. Do not loop aggressively or try to bypass the limit.

## Admin Areas

Use the CLI where possible:

- `gumroad products ...` for products, covers, thumbnails, content, publish/unpublish.
- `gumroad files ...` for file upload helpers.
- `gumroad sales ...` for sales, buyers, refunds, receipt resend, shipping.
- `gumroad payouts ...` for payout reads.
- `gumroad licenses ...` for license verification and management.
- `gumroad offer-codes ...`, `gumroad variants ...`, `gumroad custom-fields ...`, `gumroad subscribers ...`, `gumroad webhooks ...` for store operations.

Use direct API only when the CLI lacks a required operation. If using API directly, check both HTTP status and JSON `success`.

## Clawhub Publication Checklist

Before publishing:

1. Ensure the skill contains no credentials, real access tokens, account secrets, private paths, or temporary public URLs.
2. Keep personal machine details in `TOOLS.md`, not the skill.
3. Validate scripts with `python -m py_compile scripts/gumroad_batch_publish.py`.
4. Test read-only CLI commands: `gumroad user --json`, `gumroad products list --json`.
5. Do not include generated manifests or state in the skill package.
6. Publish from the applied skill folder with a clean version and changelog:

```powershell
clawhub publish .\skills\gumroad-admin --slug gumroad-admin --name "Gumroad Admin" --version 1.0.0 --changelog "Initial Gumroad admin and publishing workflow"
```