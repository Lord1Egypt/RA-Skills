---
name: blindoracle-massat-audit
version: 1.0.0
description: Security audit for multi-agent AI systems - OWASP ASI01-ASI10
author: craigmbrown
category: security
permissions:
  - network
  - file_read
tags:
  - security
  - audit
  - owasp
  - multi-agent
  - compliance
pricing:
  model: per-use
  amount: 50
  currency: USD
  payment: x402
---

# BlindOracle MASSAT Security Audit

Run a comprehensive OWASP ASI01-ASI10 security assessment on any multi-agent system via the BlindOracle API. Returns risk scores (0-100) per category with remediation priorities.

## When to Use

- Before deploying a new multi-agent system to production
- After adding new agents or tools to an existing fleet
- As part of CI/CD pipeline security gates
- For compliance reporting (OWASP Agentic AI Top 10)
- To validate Microsoft AGT runtime governance is properly configured

## Quick Reference

```bash
# Full audit (all 10 OWASP ASI categories)
curl -X POST https://craigmbrown.com/api/v1/massat/audit \
  -H "Content-Type: application/json" \
  -H "X-Payment: x402" \
  -d '{
    "target": "https://github.com/your-org/your-agent-repo",
    "scope": "full",
    "categories": ["ASI01","ASI02","ASI03","ASI04","ASI05","ASI06","ASI07","ASI08","ASI09","ASI10"]
  }'

# Quick scan (ASI01-ASI03 only, free tier)
curl -X POST https://craigmbrown.com/api/v1/massat/audit \
  -H "Content-Type: application/json" \
  -d '{"target": "https://github.com/your-org/your-agent-repo", "scope": "quick"}'
```

## Response Format

```json
{
  "audit_id": "a1b2c3d4",
  "overall_score": 72,
  "risk_level": "MEDIUM",
  "categories": {
    "ASI01": {"score": 85, "findings": 2, "critical": 0, "name": "Prompt Injection"},
    "ASI02": {"score": 60, "findings": 4, "critical": 1, "name": "Data Exfiltration"},
    "ASI03": {"score": 90, "findings": 1, "critical": 0, "name": "Broken Access Control"}
  },
  "total_findings": 23,
  "critical_findings": 3,
  "remediation_priority": ["ASI02", "ASI04", "ASI07"],
  "report_url": "https://craigmbrown.com/audits/a1b2c3d4.html"
}
```

## Pricing

| Tier | Scope | Price | Categories |
|------|-------|-------|-----------|
| Free | Quick scan | $0 | ASI01-ASI03 |
| Full | Complete audit | $50/use | ASI01-ASI10 |
| API | Monthly subscription | $99/mo | Unlimited |

## Payment

Full audits use x402 micropayments. Include `X-Payment: x402` header with ecash token. Free quick scans require no payment (10/day limit).

## Links

- [MASSAT Framework (open-source)](https://github.com/craigmbrown/massat-framework)
- [BlindOracle Marketplace](https://craigmbrown.com/blindoracle/)
- [Whitepaper: Security Auditing a 94-Agent Fleet](https://craigmbrown.com/blindoracle/blog/agent-security-crisis.html)
