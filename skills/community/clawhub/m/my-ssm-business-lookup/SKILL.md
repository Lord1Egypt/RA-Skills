---
name: my-ssm-business-lookup
description: Look up Malaysian company registration data from SSM. Returns directors, status, filings, business type.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - SKILLPAY_API_KEY
    emoji: "🏢"
    homepage: https://github.com/swmeng/myskills
---

# Malaysian Business Lookup (SSM)

Query Malaysian company registration data. Returns structured company information.

## Usage

**Input:**
- `query`: Company name or registration number (e.g., "202001012345" or "Petronas")
- `type`: "name" or "registration_number" (default: auto-detect)

**Output:**
- Company name and registration number
- Business type (Sdn Bhd, Bhd, Enterprise, LLP, etc.)
- Status (Active, Dormant, Dissolved, etc.)
- Incorporation date
- Registered address
- Directors list
- Nature of business (SSM section/division codes)

## Pricing
$0.05 USDT per call via SkillPay.me
