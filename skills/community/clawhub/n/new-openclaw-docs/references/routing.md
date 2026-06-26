# Routing Guide

Use this quick map to pick the first doc category.

## Intent to category

- Setup and onboarding -> `/start/`, `/install/`
- Provider setup (Discord, Telegram, WhatsApp, etc.) -> `/providers/`
- Gateway configuration and operations -> `/gateway/`
- Concept explanations -> `/concepts/`
- Tool usage -> `/tools/`
- Automation (cron/webhooks/polling) -> `/automation/`
- Platform deployment -> `/platforms/`
- CLI usage -> `/cli/`
- Low-level references -> `/reference/`

## First-pass workflow

1. Run `sitemap.sh` to identify category breadth.
2. Run `search.sh <keywords>` for candidate docs.
3. Run `fetch-doc.sh <path>` for concrete content.
4. Return config guidance with source path and URL.
