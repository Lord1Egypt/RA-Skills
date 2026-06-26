# HK Supermarket Shopping Skill (v1.2.3)

Simple, fast price lookup for Hong Kong supermarkets.

## Usage

Ask for any product (in English or Chinese). The skill will:
- Compare prices among supermarkets
- Identify the cheapest option
- Tell you how many you can buy with a fixed budget

Example: `"Coke Zero"` → returns cheapest supermarket, price, and quantity for your budget.

Data is updated daily (CSV kept for 1 day only).

## GitHub

Source code and releases: https://github.com/StevenHo1394/openclaw/tree/main/skills/hk-supermarket-shopping

## Version History

- **v1.2.3** (2026-04-04)
  - Fixed data directory path: now anchored to skill directory (`Path(__file__).parent / "data"`) to prevent data being written to wrong location when invoked from different cwd.
  - Added missing `package.json` and `clawhub.json` for manifest consistency.
  - Version numbers synced across all manifests (`openclaw.plugin.json`, `SKILL.md`, `package.json`, `clawhub.json`, `README.md`).

