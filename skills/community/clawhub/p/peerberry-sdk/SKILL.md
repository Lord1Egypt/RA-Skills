---
name: peerberry-sdk
description: Use this skill when assisting with FortressQuant's peerberry-sdk for PeerBerry investor automation, P2P lending education, and alternative-investment onboarding. Apply it for authentication setup, portfolio and loan retrieval, filtering, purchase automation, risk-aware explanation, and SDK debugging.
---

# PeerBerry SDK Skill

## TL;DR Quick Start

- Start with read-only calls first (`get_profile`, `get_overview`, `get_loans`).
- Use `Decimal` for money and rates, never `float`.
- Treat `purchase_loan` as real-money action and gate it with `DRY_RUN` and `MAX_ORDERS`.
- Use SDK filter arguments before local filtering (`min_interest_rate`, `countries`, `loan_types`).
- Catch specific auth/funds errors, then fall back to `PeerberryException`.

Read-only starter:

```python
from peerberry_sdk import PeerberryClient

with PeerberryClient(email="YOUR_EMAIL", password="YOUR_PASSWORD") as api:
    profile = api.get_profile()
    overview = api.get_overview()
    loans = api.get_loans(quantity=5)

    print(profile.public_id)
    print(overview.data.get("availableMoney", overview.data.get("items", {}).get("availableMoney")))
    print([loan.loan_id for loan in loans])
```

Safe invest starter:

```python
from decimal import Decimal
from peerberry_sdk import PeerberryClient

DRY_RUN = True
MAX_ORDERS = 10
TICKET_SIZE = Decimal("10.00")

with PeerberryClient(email="YOUR_EMAIL", password="YOUR_PASSWORD") as api:
    loans = api.get_loans(quantity=50, min_interest_rate=Decimal("9.5"), exclude_invested_loans=True)

    for idx, loan in enumerate(loans):
        if idx >= MAX_ORDERS or loan.loan_id is None:
            break

        if DRY_RUN:
            print(f"[DRY_RUN] would invest {TICKET_SIZE} in loan {loan.loan_id}")
            continue

        api.purchase_loan(loan_id=loan.loan_id, amount=TICKET_SIZE)
```

## Core Purpose

`peerberry-sdk` is a Python wrapper around the PeerBerry investor API. In P2P lending, investors allocate capital across many loans (or loan fractions), receive principal and interest repayments over time, and manage risk through diversification and monitoring. PeerBerry provides marketplace access to these investor workflows, and this SDK converts them into programmable Python actions for analysis, automation, and operational control.

## Scope / Non-goals

In scope:

- Explain PeerBerry and P2P lending concepts in plain language.
- Generate and debug Python code using the real SDK method surface.
- Build read-only monitoring scripts and guarded investment automation.
- Help with filtering, paging, exports, and auth/token lifecycle patterns.

Out of scope:

- Provide financial advice, suitability advice, or guaranteed-return claims.
- Promise profitability, safety, or future performance.
- Invent SDK methods that do not exist.

## Request Classifier

Classify incoming requests and respond with the matching style:

1. `educational`: user is new to P2P/PeerBerry.
   - Explain concepts first, then provide read-only demo code.
   - Load: `references/p2p-primer.md`.
2. `read_only_coding`: user wants portfolio/loan analytics.
   - Provide runnable snippets with typed model handling.
   - Load: `references/api-quickref.md`.
3. `real_money_automation`: user wants buy/invest flows.
   - Add `DRY_RUN`, `MAX_ORDERS`, funds checks, and explicit risk labels.
   - Load: `references/api-quickref.md` and `references/task-recipes.md`.
4. `debugging`: user has errors/exceptions.
   - Triage auth, enum inputs, filter metadata, then payload shape.
   - Load: `references/api-quickref.md`.

## Prerequisites

- Create and verify an investor account on the official PeerBerry website: <https://peerberry.com/>.
- Use valid PeerBerry credentials (`email`, `password`).
- If account uses TOTP 2FA, provide `tfa_secret` and install the `otp` extra.
- Treat purchase actions as real-money operations.

## Key Concepts & Objects

Primary entry point:

- `PeerberryClient`: high-level client for authentication, retrieval, and purchase actions.

Core model objects:

- `Profile`, `Overview`, `Loan`, `LoanPage`, `InvestmentPage`, `Transaction`, `AccountSummary`, `PurchaseOrder`.

Domain semantics:

- `loan`: marketplace listing that can be invested into.
- `investment`: already-owned position in a loan.
- `purchase order`: accepted order result with `order_id` (not settlement confirmation).

## Installation & Authentication

Install:

```bash
pip install peerberry-sdk
```

Install with 2FA support:

```bash
pip install "peerberry-sdk[otp]"
```

Authenticate:

```python
from peerberry_sdk import PeerberryClient

with PeerberryClient(email="YOUR_EMAIL", password="YOUR_PASSWORD") as api:
    print(api.get_profile().public_id)
```

## Core Functions & Common Workflows

Use this method map:

- Profile and portfolio: `get_profile`, `get_overview`, `get_loyalty_tier`
- Loan discovery: `get_loans`, `get_loans_page`, `get_loan_details`
- Purchase action: `purchase_loan`
- Portfolio positions: `get_investments`
- Cash flow and reporting: `get_transactions`, `get_account_summary`
- Exports: `get_mass_investments`, `get_mass_transactions`
- Metadata helpers: `get_countries`, `get_originators`

For signatures, enums, and exception patterns, load `references/api-quickref.md`.
For copy-paste user prompts and intent routing, load `references/task-recipes.md`.

## Safety Defaults (Real-Money Flows)

Always apply unless the user explicitly overrides:

- Default to read-only path first.
- Add `DRY_RUN = True` for first run.
- Set a hard cap with `MAX_ORDERS`.
- Skip records missing `loan_id`.
- Validate `available_to_invest >= ticket_size` when field is present.
- Stop on `InsufficientFunds`.
- Log each resulting `order_id`.

## Known SDK Quirks

- `get_overview` payload can be flat or nested under `items`.
- `get_loans` internally paginates with max page size 40.
- `get_loans` defaults `group_guarantee=True`.
- Country/originator filters require display names from metadata helpers.
- Export methods return raw `bytes`, not typed rows.

## Reference Files (Progressive Loading)

Load only what is needed:

- `references/p2p-primer.md`
  - Use for beginner education, plain-language explanations, and trust-first communication rules.
- `references/api-quickref.md`
  - Use for method signatures, accepted values, parameter semantics, exceptions, and debugging.
- `references/task-recipes.md`
  - Use for copy-paste prompts mapped to common investor intents.

## Maintenance Contract

When SDK changes, update this skill in this order:

1. Verify method signatures and accepted values against:
   - `src/peerberry_sdk/client.py`
   - `docs/api/client.md`
2. Update `references/api-quickref.md` first.
3. Update affected recipes in `references/task-recipes.md`.
4. Keep this root `SKILL.md` concise and routing-focused.
5. Re-check safety defaults for any new write action methods.

## Project Resources

- Repository: <https://github.com/FortressQuant/peerberry-sdk>
- Docs index: <https://github.com/FortressQuant/peerberry-sdk/tree/main/docs>
- Client API reference: <https://github.com/FortressQuant/peerberry-sdk/blob/main/docs/api/client.md>
- Issues: <https://github.com/FortressQuant/peerberry-sdk/issues>

## Skill Authoring References (March 2026)

- OpenAI Academy skills guide: <https://academy.openai.com/public/clubs/work-users-ynjqu/resources/how-to-build-and-use-skills>
- Anthropic memory guidance: <https://docs.anthropic.com/en/docs/claude-code/memory>
- GitHub Copilot custom instructions: <https://docs.github.com/en/copilot/how-tos/custom-instructions/adding-custom-instructions-for-github-copilot?tool=vscode>
- OpenAI AGENTS.md spec: <https://github.com/openai/agents.md>
