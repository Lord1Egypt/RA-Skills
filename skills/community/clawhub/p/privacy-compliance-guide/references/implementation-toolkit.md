# Privacy Compliance Implementation Toolkit

## Recommended Tools by Function

### Cookie Consent Management

| Tool | Price | Best For | Key Features |
|---|---|---|---|
| Cookiebot | $12-46/mo | SMB Shopify/WooCommerce | Auto-scan, GDPR + CCPA, easy setup |
| OneTrust | Free-Enterprise | Growing businesses | Full privacy suite, scalable |
| Termly | $10-39/mo | Budget-conscious | Simple generator + consent |
| Osano | $0-199/mo | Multi-site businesses | Cross-domain consent |
| CookieYes | $10-49/mo | WordPress/Shopify | Auto-blocking, geo-targeting |

**Selection criteria**:
- Does it auto-scan and categorize cookies?
- Does it block cookies before consent?
- Does it support geo-targeted consent (GDPR banner for EU, CCPA for CA)?
- Does it integrate with your e-commerce platform?
- Does it store consent records?

### Privacy Policy Generators

| Tool | Price | Best For | Customization |
|---|---|---|---|
| Termly | $10-39/mo | Quick generation | Template-based, moderate |
| Iubenda | $9-29/mo | Multi-language | High, regulation-specific |
| PrivacyPolicies.com | $19-99/yr | One-time setup | Template-based |
| Legal counsel | $500-3,000 | High-risk businesses | Fully custom |

**Recommendation**: Use a generator for v1, then have legal counsel review. Full custom drafting for businesses processing sensitive data or operating in heavily regulated categories.

### Data Subject Request Management

| Method | Cost | Best For | Features |
|---|---|---|---|
| Dedicated email inbox | Free | < 10 requests/month | Manual, simple |
| Google Form + Sheet | Free | < 25 requests/month | Structured intake, tracking |
| OneTrust DSR module | Included | 25+ requests/month | Automated workflows |
| DataGrail | Enterprise | 100+ requests/month | Full automation, integrations |

### Email Compliance Tools

Most email marketing platforms include compliance features:

| Platform | Double Opt-In | Unsubscribe | Physical Address | Consent Tracking |
|---|---|---|---|---|
| Klaviyo | ✅ | ✅ | ✅ (template) | ✅ |
| Mailchimp | ✅ | ✅ | ✅ (template) | ✅ |
| Omnisend | ✅ | ✅ | ✅ (template) | ✅ |
| ActiveCampaign | ✅ | ✅ | ✅ (template) | ✅ |

**Configuration checklist** (do this in your email platform):
- [ ] Enable double opt-in for all signup forms
- [ ] Add physical address to email footer template
- [ ] Test unsubscribe link in every email type
- [ ] Configure preference center (granular opt-out)
- [ ] Set up consent timestamp logging
- [ ] Configure auto-suppression for bounces and complaints

## Platform-Specific Implementation

### Shopify Privacy Setup

1. **Cookie consent**: Install Cookiebot or OneTrust app from Shopify App Store
2. **Privacy policy**: Settings → Legal → Privacy Policy (add custom or generated policy)
3. **Cookie policy**: Add as separate page linked from privacy policy
4. **CCPA "Do Not Sell" link**: Add to footer navigation (Online Store → Navigation → Footer)
5. **Customer data requests**: Settings → Legal → Customer privacy → Enable data request processing
6. **Data retention**: Use Shopify's customer data API for automated erasure workflows
7. **Checkout consent**: Add marketing consent checkbox at checkout (Settings → Checkout → Marketing consent)

### Amazon/eBay Seller Privacy

On marketplaces, the platform handles most customer-facing privacy (cookie consent, privacy policy for marketplace transactions). Your obligations:
- Maintain your own privacy policy for your seller profile/About page
- Comply with marketplace data use policies (don't use buyer data for unauthorized purposes)
- Don't export buyer data to external marketing lists without consent
- Handle any direct customer communications (support emails) in compliance with CAN-SPAM/GDPR
- Maintain DPAs with your own tools that process marketplace order data

### WordPress/WooCommerce Privacy Setup

1. **Cookie consent**: Install CookieYes or Complianz plugin
2. **Privacy policy**: Settings → Privacy → Create/select privacy policy page
3. **Cookie blocking**: Configure consent plugin to block scripts until consent
4. **Data export/erasure**: Built-in under Tools → Export/Erase Personal Data
5. **Checkout consent**: Add GDPR consent checkbox to checkout (WooCommerce → Settings → Accounts & Privacy)

## Template: Data Processing Agreement (Key Clauses)

When you can't use a vendor's standard DPA, ensure your agreement includes:

1. **Subject matter and duration**: What data, what processing, how long
2. **Nature and purpose**: Why you're sharing the data
3. **Types of personal data**: Categories of data processed
4. **Categories of data subjects**: Whose data (customers, visitors, etc.)
5. **Processor obligations**: Security measures, confidentiality, sub-processors
6. **Audit rights**: Your right to verify compliance
7. **Breach notification**: Processor must notify you without undue delay
8. **Data return/deletion**: What happens when the relationship ends
9. **International transfers**: Safeguards if data crosses borders
10. **Sub-processor management**: How sub-processors are approved and monitored

## Template: Breach Notification (Supervisory Authority)

**To**: [Supervisory Authority]
**From**: [Company Name, DPO Contact]
**Date**: [Date of notification]

1. **Nature of breach**: [Description — e.g., unauthorized access to customer database]
2. **Date/time of breach**: [When discovered, estimated when occurred]
3. **Categories of data**: [e.g., names, emails, order history, payment last-4]
4. **Approximate number of individuals**: [Number]
5. **Approximate number of records**: [Number]
6. **DPO contact**: [Name, email, phone]
7. **Likely consequences**: [e.g., identity theft risk, spam, phishing]
8. **Measures taken**: [e.g., contained breach, reset passwords, engaged forensics]
9. **Measures proposed**: [e.g., enhanced monitoring, security audit, customer notification]
