---
name: Privacy Compliance Guide
description: Navigate e-commerce privacy regulations including GDPR, CCPA/CPRA, cookie consent, data collection policies, email marketing compliance, and customer data handling to protect your business from fines and build customer trust.
---

# Privacy Compliance Guide

Build a privacy-compliant e-commerce operation that protects customer data, avoids regulatory fines, and turns privacy into a competitive advantage. This skill covers the major regulations, practical implementation steps, and ongoing compliance maintenance for online sellers.

## Quick Reference

| Decision | Strong | Acceptable | Weak|
|---|---|---|---|
| **Privacy policy** | Custom-drafted, regulation-specific, regularly updated | Template-based, covers key regulations | Generic boilerplate or missing |
| **Cookie consent** | Granular opt-in banner with category controls | Basic opt-in/opt-out banner | No consent mechanism or implied consent |
| **Data inventory** | Complete map of all data collected, stored, processed, shared | Major data flows documented | No documentation of data practices |
| **Email compliance** | Double opt-in, easy unsubscribe, CAN-SPAM + GDPR compliant | Single opt-in with working unsubscribe | Purchased lists or no unsubscribe option |
| **Data retention** | Defined retention periods per data type with auto-deletion | General retention policy exists | No retention policy, data kept indefinitely |
| **Breach response** | Written plan with 72-hour notification procedure | Awareness of notification requirements | No breach response plan |

## Solves

1. **Regulatory fines** — GDPR fines up to 4% of global revenue or €20M; CCPA fines up to $7,500 per intentional violation
2. **Cookie consent gaps** — Non-compliant cookie banners that expose the business to enforcement action
3. **Email marketing violations** — CAN-SPAM penalties of $50,120 per email; GDPR consent requirements for marketing
4. **Data breach liability** — Lack of breach response plan leading to delayed notification and increased penalties
5. **Customer trust erosion** — Poor privacy practices driving customers to privacy-conscious competitors
6. **Third-party data risks** — Sharing customer data with vendors/partners without proper agreements
7. **Cross-border complexity** — Selling internationally without understanding jurisdiction-specific requirements

## Workflow

### Step 1: Conduct a Data Inventory

Map every piece of customer data your business collects, stores, and shares.

**Data collection points**:
| Touchpoint | Data Collected | Legal Basis | Retention |
|---|---|---|---|
| Account registration | Name, email, password | Contract performance | Until account deletion |
| Checkout | Address, payment info, phone | Contract performance | Order + 7 years (tax) |
| Browse behavior | Pages viewed, time on site, clicks | Legitimate interest / Consent | 90 days |
| Email signup | Email, name, preferences | Consent | Until unsubscribe |
| Customer support | Issue details, communication history | Contract / Legitimate interest | 3 years |
| Reviews | Name, rating, review text | Consent | Until withdrawal |
| Cookies/tracking | IP, device info, browsing patterns | Consent | Per cookie category |

**Third-party data sharing**:
| Partner | Data Shared | Purpose | DPA in Place? |
|---|---|---|---|
| Payment processor | Card details, billing info | Payment processing | [ ] Yes / [ ] No |
| Shipping carrier | Name, address, phone | Order fulfillment | [ ] Yes / [ ] No |
| Email platform | Email, name, segments | Marketing | [ ] Yes / [ ] No |
| Analytics | IP, behavior, device | Analytics | [ ] Yes / [ ] No |
| Ad platforms | Email (hashed), behavior | Advertising | [ ] Yes / [ ] Noo |
| Reviews platform | Email, name, order data | Review collection | [ ] Yes / [ ] No |

### Step 2: Implement Cookie Consent

**GDPR-compliant cookie banner requirements**:
- Must appear before non-essential cookies fire
- Must offer granular category choices (not just "accept all")
- Must be as easy to reject as to accept
- Must not use dark patterns (pre-checked boxes, confusing language)
- Must store consent records

**Cookie categories**:
| Category | Examples | Consent Required? |
|---|---|---|
| Strictly necessary | Cart, authentication, security | No (always active) |
| Functional | Language preference, recently viewed | Yes |
| Analytics | Google Analytics, Hotjar, Mixpanel | Yes |
| Marketing | Facebook Pixel, Google Ads, retargeting | Yes |

**Implementation options**:
- Cookiebot ($12-46/month) — Auto-scans and categorizes cookies
- OneTrust (free tier available) — Enterprise-grade, GDPR + CCPA
- Termly ($10-39/month) — Simple setup, good for Shopify
- Custom implementation — Full control but higher maintenance

### Step 3: Draft Privacy Policy

**Required sections** (GDPR + CCPA coverage):

1. **Identity and contact details** — Who you are, how to contact your DPO
2. **Data collected** — What personal data you collect and how
3. **Legal bases** — Why you process each type of data (consent, contract, legitimate interest)
4. **Data sharing** — Who you share data with and why
5. **International transfers** — If data leaves the EEA/UK, what safeguards apply
6. **Retention periods** — How long you keep each data type
7. **Individual rights** — Right to access, rectify, erase, port, restrict, object
8. **Cookie policy** — What cookies you use and how to manage them
9. **Children's data** — COPPA compliance if applicable (under 13)
10. **California-specific disclosures** — CCPA/CPRA rights for California residents
11. **Updates** — How you notify customers of policy changes

**Placement requirements**:
- Footer link on every page
- Link in account registration flow
- Link at checkout
- Link in email footer

### Step 4: Configure Email Marketing Compliance

**CAN-SPAM requirements** (US):
- Accurate "From" name and email address
- Non-deceptive subject lines
- Clear identification as advertising (if applicable)
- Physical mailing address in every email
- Working unsubscribe mechanism (honored within 10 business days)
- No purchased email lists

**GDPR requirements** (EU/UK):
- Explicit opt-in consent (pre-checked boxes are NOT valid consent)
- Double opt-in recommended (confirmation email)
- Separate consent for each purpose (newsletter vs. promotions vs. partner offers)
- Easy withdrawal of consent (one-click unsubscribe)
- Record of when and how consent was obtained

**Best practice — double opt-in flow**:
1. Customer enters email → receives confirmation email
2. Customer clicks confirmation link → added to list with timestamp
3. Welcome email sent with preference center link
4. All emails include one-click unsubscribe + physical address

### Step 5: Set Up Data Subject Request Handling

**GDPR rights you must support**:
| Right | Timeline | Implementation |
|---|---|---|
| Access (SAR) | 30 days | Export all data for the individual |
| Rectification | 30 days | Allow customers to update their data |
| Erasure ("right to be forgotten") | 30 days | Delete data (except where legal obligation to retain) |
| Data portability | 30 days | Provide data in machine-readable format (CSV/JSON) |
| Restriction | 30 days | Stop processing but retain data |
| Objection | 30 days | Stop processing for direct marketing immediately |

**CCPA/CPRA rights**:
| Right | Timeline | Notes |
|---|---|---|
| Know | 45 days | What data collected, categories, sources, purposes |
| Delete | 45 days | Delete personal information |
| Opt-out of sale/sharing | Immediate | "Do Not Sell My Personal Information" link |
| Correction | 45 days | Correct inaccurate information |
| Limit use of sensitive data | Immediate | Restrict use of sensitive PI |

**Implementation**: Create a dedicated email or web form (e.g., privacy@yourstore.com or /privacy-request page) and establish an internal process with assigned responsibilities and tracking.

### Step 6: Prepare a Data Breach Response Plan

**72-hour notification timeline (GDPR)**:
1. **Hour 0-4**: Identify and contain the breach
2. **Hour 4-12**: Assess scope — what data, how many individuals, what risk
3. **Hour 12-24**: Notify DPO/privacy lead, begin documentation
4. **Hour 24-48**: Draft notification to supervisory authority
5. **Hour 48-72**: Submit notification to supervisory authority
6. **Day 3-30**: Notify affected individuals (if high risk) without undue delay

**Breach notification must include**:
- Nature of the breach
- Categories and approximate number of individuals affected
- Categories and approximate number of records affected
- Name and contact details of DPO or contact point
- Likely consequences of the breach
- Measures taken or proposed to address the breach

### Step 7: Ongoing Compliance Maintenance

**Monthly tasks**:
- Review new third-party tools/integrations for data impact
- Check unsubscribe processing (test it works)
- Review and respond to any data subject requests

**Quarterly tasks**:
- Audit cookie consent banner functionality
- Review data retention — delete data past retention period
- Update privacy policy if any data practices changed
- Review vendor DPA status

**Annual tasks**:
- Full data inventory refresh
- Privacy policy comprehensive review
- Staff privacy training
- Data protection impact assessment (DPIA) for new high-risk processing
- Regulatory update review (new laws, enforcement trends)

## Example 1: Shopify DTC Brand — GDPR + CCPA Setup

**Scenario**: US-based skincare brand selling to US + EU customers via Shopify. 50,000 email subscribers, uses Klaviyo, Google Analytics, Facebook Ads.

**Step 1 — Data inventory findings**:
- Shopify collects: name, email, address, phone, payment, order history
- Klaviyo receives: email, name, purchase history, browse behavior
- Google Analytics: IP (anonymized), pages, sessions, device
- Facebook Pixel: IP, browsing behavior, purchase events (hashed email for Custom Audiences)
- DPAs needed: Klaviyo (has standard DPA), Facebook (Business Tools Terms), Google (Data Processing Terms)

**Step 2 — Cookie consent**: Installed Cookiebot on Shopify ($14/month). Configured categories: necessary (cart/checkout), analytics (GA4), marketing (Facebook Pixel, Klaviyo tracking). GA4 and FB Pixel only fire after consent.

**Step 3 — Privacy policy**: Drafted with GDPR + CCPA sections. Added "Do Not Sell My Personal Information" link in footer for CCPA. Listed all data categories, purposes, and third-party recipients.

**Step 4 — Email compliance**: Configured Klaviyo double opt-in. Added physical address to all email templates. Created preference center with separate toggles for promotional emails, new product alerts, and educational content.

**Step 5 — Data requests**: Created privacy@brand.com inbox monitored weekly. Built internal SOP: requests triaged within 48 hours, fulfilled within 25 days (buffer before 30-day deadline).

**Step 6 — Breach plan**: Documented response procedure. Identified Shopify's breach notification process. Assigned roles: CEO (decision authority), CTO (containment), Operations (customer communication).

**Result**: Fully compliant setup in 2 weeks. Ongoing cost: ~$15/month (Cookiebot) + 2 hours/month maintenance.

## Example 2: Amazon + Multi-Channel Seller — Minimal Viable Compliance

**Scenario**: Small team selling on Amazon, eBay, and own Shopify store. Limited resources. Need practical compliance without a legal team.

**Priorities** (risk-based approach):
1. **Email compliance** (highest fine risk): Switched to double opt-in, added physical address, tested unsubscribe links. Deleted purchased email list.
2. **Cookie consent** (EU fine risk): Installed free OneTrust banner on Shopify. Amazon/eBay handle their own cookie consent.
3. **Privacy policy** (foundation): Used Termly generator ($10/month) customized with actual data practices. Added to Shopify footer and eBay "About" page.
4. **Data retention**: Set Shopify to anonymize order data after 3 years (beyond tax retention requirement). Configured email platform to auto-remove unsubscribed contacts after 30 days.
5. **"Do Not Sell" link**: Added CCPA link to Shopify footer. Disabled Facebook Custom Audiences for California IP addresses (Shopify geolocation).

**Result**: 80% compliant in 1 week. Ongoing cost: $10/month + 1 hour/month. Remaining 20% (formal DPIA, full data inventory, breach response plan) scheduled for quarterly improvement.

## Common Mistakes

1. **Relying on "implied consent"** — Under GDPR, pre-checked boxes, continued browsing, or scroll-based consent are NOT valid. You need affirmative action (click "Accept") for non-essential cookies and marketing.

2. **Using purchased email lists** — This violates CAN-SPAM (if recipients haven't opted in) and GDPR (no consent basis). Delete purchased lists immediately and build organically.

3. **Firing tracking pixels before consent** — Many sites load Google Analytics and Facebook Pixel on page load, before the cookie banner is answered. This is a GDPR violation. Implement consent-gated loading.

4. **Missing physical address in emails** — CAN-SPAM requires a valid physical postal address in every commercial email. A PO Box counts. Missing it is a per-email violation ($50,120 each).

5. **No unsubscribe mechanism** — Every marketing email must have a visible, working unsubscribe link. Honor within 10 business days (CAN-SPAM) or immediately (GDPR best practice).

6. **Ignoring data processor agreements** — If you share customer data with any third party (email platform, analytics, payment processor), you need a Data Processing Agreement. Most major platforms offer standard DPAs.

7. **One-size-fits-all retention** — Different data types have different retention needs. Tax records require 7 years; browse behavior should be deleted within 90 days. Define retention per data category.

8. **No breach response plan** — GDPR requires notification within 72 hours. Without a pre-written plan, you'll miss the deadline. Even small businesses need a one-page breach response procedure.

9. **Treating marketplace sales as exempt** — While Amazon/eBay handle some compliance on their platforms, you're still responsible for data you collect independently (email lists, customer support data, CRM data).

10. **Neglecting state-level US laws** — Beyond California (CCPA/CPRA), Virginia (VCDPA), Colorado (CPA), Connecticut (CTDPA), and other states have privacy laws. If you sell nationally, consider the strictest standard as your baseline.

## Resources

- [Output Template](references/output-template.md) — Privacy compliance audit and implementation plan template
- [Regulation Summary](references/regulation-summary.md) — Key requirements for GDPR, CCPA, CAN-SPAM, and state laws
- [Implementation Toolkit](references/implementation-toolkit.md) — Recommended tools, templates, and configurations
- [Quality Checklist](assets/quality-checklist.md) — Compliance validation checklist
