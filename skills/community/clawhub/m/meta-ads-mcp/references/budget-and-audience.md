# Budget Strategy & Audience Targeting

## 4. BUDGET STRATEGY

### CBO vs ABO
| Scenario | Recommended |
|---|---|
| Total daily budget ≥ $50, trust Meta's algorithm | **CBO** — Meta allocates to best-performing ad set |
| Small budget, strict testing, need visibility per audience | **ABO** — fixed budget per ad set |
| Finding winning creatives in a new account | **ABO** first, then consolidate to CBO at scale |

### Starting Budgets (per site/campaign)
- **Testing phase**: $10–$20/day per campaign (ABO) — just enough to generate signal
- **Scaling a winner**: $50–$200/day CBO, let Meta optimize
- **Learning Phase rule**: Never edit budget by more than 20% at once — it resets learning
- **Minimum for a conversion campaign to exit Learning Phase**: ~$50 total spend generating 50+ conversion events

### Budget Guardrails
- Set **Campaign Spending Limits** in Ads Manager as a hard ceiling
- Set **Account Spending Limits** in billing settings
- Review daily spend every morning during launch week
- Never launch a campaign on a Friday without someone monitoring it

---

## 5. AUDIENCE TARGETING

### Full-Funnel Audience Strategy

#### Cold (Prospecting) — People who don't know the brand
- **Advantage+ Audience** (recommended 2026): Let Meta find the right people using your pixel data as a signal. Provide broad demographics + let algorithm work.
- **Lookalike Audiences**: Build from website visitors (180-day), purchasers, or email list. Start with 1–2% LAL, test 3–5% for scale.
- **Broad Targeting**: Age + gender + country only — trust Meta's algorithm with strong creative.

#### Warm (Engagement Retargeting) — People who know the brand but haven't converted
- Facebook/Instagram page engagers (90 days)
- Video viewers (25%, 50%, 75%)
- Website visitors who didn't convert (30/60/90 days)

#### Hot (Purchase Retargeting) — People who showed strong purchase intent
- Website visitors of key pages (product page, pricing page, checkout)
- Add-to-cart but didn't purchase (7–14 days)
- Email list upload (Custom Audience from CRM)

### Exclusions (Always Set These)
- Exclude existing customers from prospecting campaigns
- Exclude retargeting pools from cold audiences
- Exclude purchasers from add-to-cart retargeting
- Use Meta's **Audience Overlap tool** to check for cannibalization

### Privacy & compliance (before any customer-data upload)

Customer-list Custom Audiences and PII in CAPI event parameters (email, phone) are regulated personal data. Before uploading or transmitting:

- **Lawful basis & consent** — document a lawful basis (consent / contract / legitimate interest) under GDPR / CCPA / PIPEDA, and ensure your privacy policy covers Meta ad targeting.
- **Hash before sending** — email and phone must be SHA‑256 hashed (normalized: lowercase + trimmed; phone in E.164) before they leave your systems. Never send plaintext PII.
- **Data minimization** — upload only the fields you need; do not bulk-export full CRM records.
- **Suppression** — honor opt-outs and right-to-be-forgotten; refresh suppression lists.
- **DPA & residency** — operate under Meta's Data Processing Terms; account for EU/UK data-residency obligations.

Do not upload customer PII without explicit sign-off from whoever owns data/privacy compliance.

### Custom Audiences to Build and Maintain
1. Website visitors (30 / 60 / 90 / 180 days)
2. Video viewers by percentage (25% / 50% / 75%)
3. Page engagers (30 / 90 days)
4. Customer list uploads (email + phone, hashed)
5. Purchasers / converters

---
