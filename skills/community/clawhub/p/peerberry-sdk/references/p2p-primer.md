# P2P Lending Primer (PeerBerry Context)

## What P2P Lending Is

Peer-to-peer lending lets investors fund borrower loans through a marketplace platform. Instead of earning bank deposit interest, investors allocate money into many loan positions and receive repayments over time.

## How It Works In Practice

1. Investor reviews available loans.
2. Investor places ticket-sized allocations across selected loans.
3. Borrowers repay principal and interest over time.
4. Investor tracks portfolio value, cash flow, and repayment status.
5. Investor rebalances by changing allocation rules or new purchases.

## Primary vs Secondary Market

- Primary market:
  - Investor funds newly listed loan opportunities.
  - In SDK terms, this is usually `get_loans(...)` + `purchase_loan(...)`.
- Secondary market:
  - Investor reviews existing loan positions offered for resale.
  - In SDK terms, this is `get_secondary_loans(...)`.

## Why Investors Use Automation

- Automate investments.
- Repeat filtering logic consistently.
- Reduce manual checking time.
- Standardize risk controls (caps, thresholds, dry-run passes).
- Keep records of actions and outcomes.

## Risk Concepts To Explain Clearly

- Credit/default risk:
  - Borrowers may repay late or not fully repay.
- Liquidity risk:
  - Capital may stay tied up until repayment or sale.
- Concentration risk:
  - Overexposure to one country/originator/loan type increases downside.
- Operational risk:
  - Mistakes in automation can place unintended orders.

## Beginner FAQ (LLM Ready)

### Is this risk-free?

No. P2P lending has credit, liquidity, and concentration risks. The SDK helps automate workflows but does not remove investment risk.

### Are returns guaranteed?

No. Rates shown in loan listings are not guarantees of realized portfolio return.

### What should I do first as a beginner?

Start read-only: authenticate, fetch profile/overview, sample loans, and understand fields before attempting purchase automation.

### Is this financial advice?

No. SDK guidance is technical and operational, not personal financial advice.

## PeerBerry-Specific Positioning

PeerBerry is a lending-focused investor marketplace where users track portfolio metrics, browse loan opportunities, and execute investments. `peerberry-sdk` is an unofficial integration layer that maps those actions into Python methods.

## Communication Rules For Newcomers

Use this wording style:

- Prefer:
  - "available rate", "historical performance", "risk-managed workflow", "read-only first"
- Avoid:
  - "guaranteed return", "risk-free income", "sure profit"

## Suggested Intro Paragraph Template

Use this template when user is new:

"PeerBerry is a marketplace for P2P lending where investors allocate across many loans and receive repayments over time. The Python SDK helps you automate monitoring, filtering, and controlled order placement. A good first step is read-only portfolio and loan analysis before any live purchase actions."
