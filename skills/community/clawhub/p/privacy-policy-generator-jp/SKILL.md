# Privacy Policy Generator

Generate a professional, legally-compliant privacy policy for any website or app. Supports GDPR (EU), CCPA (California), and APPI (Japan) regulations.

## When to use

Use this skill when the user needs to:
- Create a privacy policy for their website or application
- Generate GDPR-compliant privacy documentation
- Create CCPA-compliant privacy notices
- Draft a privacy policy that covers data collection, cookies, third-party services, and user rights

## How it works

1. Ask the user for their business details (company name, website URL, contact email)
2. Ask what data they collect (personal info, cookies, analytics, payments)
3. Ask which regulations apply (GDPR, CCPA, APPI, or auto-detect by region)
4. Ask about third-party services used (Google Analytics, Stripe, social logins, etc.)
5. Generate a complete, professional privacy policy in Markdown format

## Template

When generating a privacy policy, always include these sections:

### Required Sections
1. **Introduction** — Who operates the site and what this policy covers
2. **Information We Collect** — Personal data, automatically collected data, cookies
3. **How We Use Your Information** — Purpose of data collection
4. **Legal Basis for Processing** (GDPR) — Consent, legitimate interest, contract
5. **Data Sharing and Third Parties** — List all third-party services
6. **Cookies and Tracking** — Types of cookies, how to manage them
7. **Data Retention** — How long data is stored
8. **Your Rights** — Access, deletion, portability, opt-out
9. **Children's Privacy** — COPPA compliance statement
10. **International Data Transfers** — Cross-border data handling
11. **Changes to This Policy** — How updates are communicated
12. **Contact Information** — How to reach the data controller

### GDPR-Specific Additions
- Data Protection Officer contact (if applicable)
- Right to lodge complaints with supervisory authority
- Automated decision-making disclosure

### CCPA-Specific Additions
- "Do Not Sell My Personal Information" section
- Categories of personal information collected
- Right to know, delete, and opt-out

### APPI-Specific Additions (Japan)
- Purpose of use specification
- Joint use disclosure
- Cross-border transfer requirements

## Output Format

Generate the policy in clean Markdown with:
- Clear headings and subheadings
- Bullet points for lists of data types and rights
- Placeholder brackets [COMPANY NAME] for customizable fields
- Last updated date
- Professional, plain-language tone (avoid excessive legal jargon)

## Example Prompt

User: "I need a privacy policy for my SaaS app that uses Google Analytics and Stripe payments. We're based in the US but have EU users."

Response: Generate a full privacy policy covering GDPR + CCPA, with specific sections for Google Analytics tracking and Stripe payment processing.
