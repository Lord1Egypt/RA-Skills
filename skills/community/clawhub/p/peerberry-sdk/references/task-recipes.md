# Task Recipes (Copy-Paste Prompts)

Use these prompts directly for intent routing.

## Recipe 1: Portfolio Snapshot

- Tags: `read-only`, `beginner`
- Prompt:

```text
Using peerberry-sdk, authenticate with PeerberryClient and return my profile public_id, availableMoney, and estimated invested principal from current investments. Use Decimal-safe math and read-only calls only.
```

- Likely methods: `get_profile`, `get_overview`, `get_investments(current=True)`

## Recipe 2: Loan Discovery By Yield

- Tags: `read-only`, `screening`
- Prompt:

```text
Fetch the top 30 available loans with interest rate >= 10.0%, sorted descending by interest_rate. Print loan_id, country, originator, interest_rate, and available_to_invest.
```

- Likely methods: `get_loans(quantity=30, min_interest_rate=..., sort="interest_rate", ascending_sort=False)`

## Recipe 3: Country-Scoped Loan Search

- Tags: `read-only`, `screening`
- Prompt:

```text
Find available loans for Germany only, with interest > 9.5%, and show the first 20 results. Resolve country display name via get_countries() before filtering.
```

- Likely methods: `get_countries`, `get_loans(countries=[...], min_interest_rate=...)`

## Recipe 4: Safe Auto-Invest Loop

- Tags: `writes-money`, `guarded`
- Prompt:

```text
Build an auto-invest script that finds loans with interest >= 9.5% and invests EUR 10.00 in each. Include DRY_RUN mode, MAX_ORDERS cap, and stop on InsufficientFunds.
```

- Likely methods: `get_loans`, `purchase_loan`

## Recipe 5: Single-Loan Purchase

- Tags: `writes-money`, `manual`
- Prompt:

```text
Purchase a specific loan by ID with a EUR 10.00 ticket size and return the resulting order_id. Handle InsufficientFunds and PeerberryException.
```

- Likely methods: `purchase_loan`

## Recipe 6: Current vs Finished Investments

- Tags: `read-only`, `portfolio`
- Prompt:

```text
Show me the difference between my current and finished investments: fetch both sets, print totals, and display the first 5 entries from each.
```

- Likely methods: `get_investments(current=True)`, `get_investments(current=False)`

## Recipe 7: Account Summary Plus Transactions

- Tags: `read-only`, `reporting`
- Prompt:

```text
For the last 30 days, fetch account summary and transactions filtered to deposit, investment, principal_repayment, and interest_payment. Print totals and transaction count.
```

- Likely methods: `get_account_summary`, `get_transactions`

## Recipe 8: Export Workflow

- Tags: `read-only`, `reporting`, `exports`
- Prompt:

```text
Export current investments and last-year transactions to XLSX bytes and save them locally as investments.xlsx and transactions.xlsx.
```

- Likely methods: `get_mass_investments`, `get_mass_transactions`

## Recipe 9: Secondary Market Scan

- Tags: `read-only`, `secondary-market`
- Prompt:

```text
Scan secondary market listings with remaining term <= 24 months and interest >= 10%. Sort by loan_interest descending and print top 25 listings.
```

- Likely methods: `get_secondary_loans`

## Recipe 10: Authentication Diagnostics

- Tags: `debugging`, `auth`
- Prompt:

```text
Create a diagnostic script for PeerberryClient login with clear handling for InvalidCredentials, AuthenticationError (2FA), and TokenRefreshError, then run a read-only get_overview check.
```

- Likely methods: `PeerberryClient(...)`, `get_overview`

## Recipe 11: New To P2P (Explain Plus Demo)

- Tags: `educational`, `beginner`, `read-only`
- Prompt:

```text
I am new to P2P lending. Explain PeerBerry in simple terms, then show a read-only Python script using peerberry-sdk that fetches profile, overview, and 5 sample loans. Avoid any purchase call.
```

- Likely methods: `get_profile`, `get_overview`, `get_loans(quantity=5)`

## Recipe 12: Alternative Investment Exploration

- Tags: `educational`, `guarded`
- Prompt:

```text
I want to explore alternative investments safely. Build a two-phase script: phase 1 read-only loan analysis (interest, country, originator distribution), phase 2 optional DRY_RUN investment plan with EUR 10 ticket size and no real purchases.
```

- Likely methods: `get_loans`, `get_countries`, local aggregation

## Recipe 13: Loan Detail Due Diligence

- Tags: `read-only`, `analysis`
- Prompt:

```text
Given a shortlist of loan IDs, fetch detailed borrower/loan/schedule data and summarize key fields in a compact table for due diligence.
```

- Likely methods: `get_loan_details`

## Recipe 14: Cash-Flow Audit Trail

- Tags: `read-only`, `audit`
- Prompt:

```text
Generate a monthly cash-flow audit for the past 6 months using transactions and account summaries, grouped by transaction type and month.
```

- Likely methods: `get_transactions`, `get_account_summary`

## Recipe 15: Token Refresh Health Check

- Tags: `debugging`, `lifecycle`
- Prompt:

```text
Build a health-check script that validates login, forces token refresh with token(), and verifies a follow-up read-only call succeeds.
```

- Likely methods: `login`, `token`, `get_overview`

## Recipe 16: Country/Originator Distribution Snapshot

- Tags: `read-only`, `risk-monitoring`
- Prompt:

```text
Create a snapshot report of available loans grouped by country and originator to identify concentration risk before investing.
```

- Likely methods: `get_loans`, `get_countries`, `get_originators`
