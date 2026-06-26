---
name: luca-assistant
description: "Credit card rewards optimizer — query 150+ cards, compare benefits, track portfolio, check 5/24 status, and get the best sign-up bonuses (撸卡助手)"
user-invocable: true
metadata:
  openclaw:
    requires:
      bins: [python3, uv]
    install:
      - kind: uv
        package: luca-assistant
        bins: [luca, luca-mcp]
    os: [darwin, linux]
    emoji: "💳"
    homepage: "https://github.com/troyt-666/luca-assistant"
---

# Luca Assistant (撸卡助手)

A credit card rewards optimization tool. Query 150+ US credit cards, compare benefits, track your portfolio, and find the best sign-up bonuses.

## When to use this skill

Trigger this skill when the user asks about:
- Credit card recommendations or comparisons
- Sign-up bonuses (SUBs) or welcome offers
- Chase 5/24 status or bank application rules
- Adding/removing cards in their portfolio
- Card benefits, category multipliers, or annual credits

## Setup

### Check if already installed

Before running setup, check whether Luca is already available:

```bash
export PATH="$HOME/.local/bin:$PATH"
command -v luca-mcp && luca-mcp --help
```

If `luca-mcp` responds, skip to **How to use**. Otherwise run setup below.

### First-run setup

```bash
export PATH="$HOME/.local/bin:$PATH"
bash {baseDir}/scripts/setup.sh
```

This installs `luca-assistant` from PyPI via `uv` and seeds the database (~150 cards from Offer Optimist).

> **PATH note:** `uv tool install` places binaries in `~/.local/bin`. If `luca-mcp` is not found after setup, ensure `~/.local/bin` is on PATH (`export PATH="$HOME/.local/bin:$PATH"`).

### Verify setup

```bash
luca-mcp --help        # should print MCP server usage
luca cards | head -5   # should list cards from the database
```

## How to use

Luca is an MCP tool server. The database lives at `~/.local/share/luca/luca.db`.

If Luca is already configured as an MCP server in the agent's environment, call `luca_*` tools directly. Otherwise, call tools via the bundled script:

```bash
export PATH="$HOME/.local/bin:$PATH"
bash {baseDir}/scripts/mcp_call.sh <tool_name> '<json_args>'
```

### Available MCP tools

**Card queries:**
- `luca_query_card_details(card_name, bank?)` — look up a card's benefits, current offers, and fees
- `luca_find_highest_offers(bank?, min_bonus_usd?, is_business?, limit?)` — best current sign-up bonuses
- `luca_compare_card_benefits(card_names)` — side-by-side benefit comparison
- `luca_get_bank_rules(bank)` — issuer application rules (Chase 5/24, Amex lifetime language, Citi 8/65, etc.)

**Card enrichment:**
- `luca_update_card_benefit(card_name, category, multiplier, points_type, notes?, bank?, annual_credit?, credit_category?)` — add or update a card's category multiplier or credit
- `luca_import_cards(source?, force?)` — refresh data from 'offer-optimist' (cards + SUBs) or 'cfpb' (APRs + fees)

**Portfolio tracking:**
- `luca_get_user_portfolio()` — user's open and closed cards
- `luca_check_chase_524_status()` — 5/24 count and remaining slots
- `luca_add_user_card(card_name, opened_date, bank?, credit_limit?, bonus_earned?, bonus_met_date?, notes?)` — add a card to portfolio
- `luca_close_user_card(card_name, closed_date, bank?)` — mark a card as closed

### Examples

```bash
# Look up Chase Sapphire Preferred
bash {baseDir}/scripts/mcp_call.sh luca_query_card_details '{"card_name":"Chase Sapphire Preferred"}'

# Find top 5 offers worth at least $500
bash {baseDir}/scripts/mcp_call.sh luca_find_highest_offers '{"min_bonus_usd":500,"limit":5}'

# Compare two cards
bash {baseDir}/scripts/mcp_call.sh luca_compare_card_benefits '{"card_names":["Amex Gold","Chase Sapphire Preferred"]}'

# Check Chase 5/24 status
bash {baseDir}/scripts/mcp_call.sh luca_check_chase_524_status '{}'
```

## Enrichment workflow

When `luca_query_card_details` returns a `multiplier_hint`, the card has missing category multiplier data. To fill the gap:

1. **Web search** for the card on `site:doctorofcredit.com OR site:thepointsguy.com`
2. Find the earning rates (e.g., "3x on dining, 2x on travel")
3. Call `luca_update_card_benefit` for each category to persist the data

## Optional: USCardForum integration

For community data points from USCardForum (美卡论坛), install the companion [nitan](https://clawhub.ai/nitansde/nitan) skill. It provides `discourse_search`, `discourse_read_topic`, `discourse_list_hot_topics`, and more.

## Guidelines

- All card data comes from the database — never fabricate card details
- If a card isn't found, tell the user rather than guessing
- Respond in the user's language (Chinese or English)
- Use `luca_import_cards` to refresh data if it seems stale
