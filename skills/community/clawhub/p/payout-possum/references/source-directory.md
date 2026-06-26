# Payout Possum Source Directory

Use this file for concrete source coverage. Start with official sources, then use discovery sites only when there is no authoritative master list.

Verify links if a page redirects or changes.

## 1. State Unclaimed Property

Official directories and hubs:

- NAUPA directory: https://unclaimed.org/
- MissingMoney: https://www.missingmoney.com/
- USA.gov unclaimed money hub: https://www.usa.gov/unclaimed-money

Notes:

- Search every state where the user lived, worked, banked, studied, or held utilities.
- Use all name variants and prior addresses.

## 2. Federal and State Government Money

Official sources:

- Treasury unclaimed assets hub: https://fiscal.treasury.gov/unclaimed-assets.html
- TreasuryDirect unclaimed money FAQ: https://www.treasurydirect.gov/help-center/unclaimed-money-and-assets-faqs/
- HUD / FHA refunds: https://www.hud.gov/hud-partners/housing-premium-refunding-qa
- NCUA unclaimed deposits from liquidated credit unions: https://ncua.gov/support-services/conservatorships-liquidations/unclaimed-deposits

Check this category when the user had mortgage insurance, a failed credit union, federal payments, or agency correspondence.

## 3. Tax Refunds and Offset-Related Follow-up

Official sources:

- IRS refund tracker: https://www.irs.gov/wheresmyrefund
- IRS amended return tracker: https://www.irs.gov/filing/wheres-my-amended-return
- IRS transcripts: https://www.irs.gov/individuals/get-transcript
- Treasury Offset Program: https://www.fiscal.treasury.gov/TOP/

Notes:

- Use this category for missing refunds, reduced refunds, or old notices showing offsets.
- Route state tax checks to the relevant state revenue department.

## 4. Retirement and Pension Money

Official sources:

- PBGC unclaimed retirement benefits search: https://www.pbgc.gov/workers-retirees/find-unclaimed-retirement-benefits/search-unclaimed
- PBGC retirement benefits overview: https://www.pbgc.gov/workers-retirees/learn/find-your-retirement-benefits

Notes:

- Ask for former employer names, unions, and plan administrators.
- Government and military pensions may require separate systems.

## 5. Banking, Brokerage, Insurance, Mortgage, Escrow, and Utilities

Priority sources:

- Institution directly
- State unclaimed-property office if funds were escheated
- User statements, old mail, and email notices

Common leads:

- Dormant bank and brokerage accounts
- Insurance proceeds
- Mortgage escrow overages
- Utility deposits
- Demutualization or policyholder proceeds

There is no single official national index for this whole category beyond state escheat systems and institution-specific lookup flows.

## 6. Bankruptcy Unclaimed Funds

Official sources:

- U.S. Courts bankruptcy unclaimed funds: https://www.uscourts.gov/court-programs/bankruptcy/unclaimed-funds-bankruptcy
- Unclaimed Funds Locator: https://ucf.uscourts.gov/

Notes:

- Use this when the user was a creditor, claimant, employee, shareholder, or vendor in a bankruptcy case.
- Search by name variants and business names.

## 7. Class Actions

Official-first approach:

- Use the settlement administrator site named in the notice, court filing, or order.
- Use the court-approved notice as the source of truth.

Discovery-only lead sources:

- ClassAction.org settlements: https://www.classaction.org/settlements
- OpenClassActions: https://openclassactions.org/settlements/

Rules:

- Treat these sites as discovery tools only.
- Confirm the actual administrator domain before giving filing guidance.

## 8. Agency Refunds and Restitution

Official sources:

- FTC consumer refunds: https://www.ftc.gov/terms/consumer-refunds
- CFPB payments to harmed consumers: https://www.consumerfinance.gov/enforcement/payments-harmed-consumers/
- CFPB enforcement hub: https://www.consumerfinance.gov/enforcement

Notes:

- Look for the agency’s named payments administrator.
- Some consumers are paid automatically and do not need to file.

## 9. Employment, Healthcare, Education, and Other Niche Categories

Typical source types:

- Employer settlement pages
- State labor department pages
- Health system or insurer refund notices
- University bursar or student-account credit notices
- Utility or telecom settlement pages

High-yield evidence sources:

- Gmail or email search
- Paper mail
- HR portals
- Benefits portals

## 10. Gmail Evidence Search

Preferred skill:

- `steipete/gog` on ClawHub for direct Google-backed access

Search themes:

- settlement
- "class action"
- refund
- reimbursement
- restitution
- escrow
- surplus
- pension
- retirement
- benefit
- administrator
- "claims administrator"
- bankruptcy
- trustee
- insurance
- demutualization
- unclaimed
- escheat

Suggested combinations:

```text
from:(settlement OR administrator OR claims) (refund OR settlement OR payment)
(class action OR settlement) (deadline OR claim OR claimant)
(pension OR retirement OR benefit) (former employer OR administrator)
(escrow OR surplus OR overpayment) (mortgage OR servicer OR utility)
```

Default behavior:

- Read and summarize only
- Extract deadlines, claimant IDs, links, company names, and actions required
- Do not modify mail unless the user asks
