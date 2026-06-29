---
name: product-recalls-fda-safety
description: Product recall & FDA safety data for AI agents — track FDA drug recalls, medical device recalls, 510(k) clearances, and drug labels by company or keyword. Use to monitor product safety, recall events, regulatory risk, and compliance. Pay-per-call in USDC via x402 — no API key, no signup.
tags: [product-recall, fda, drug-recall, device-recall, safety, 510k, openfda, compliance, monitoring, regulatory, pharma]
author: gocreative
version: 1.0.0
license: MIT
---

# Product Recalls & FDA Safety

> Track recalls, device clearances, and drug data — by company or keyword. One install, pay-per-call, no API key.

## When to use this
- Monitor **product recalls** (drug or device) for a company or topic.
- Check **FDA 510(k) clearances** or **drug labels/approvals**.
- Feed a safety / compliance / supplier-risk agent.

## How it's paid (x402)
Plain HTTPS GET. First call returns HTTP 402; your wallet auto-pays the USDC fee and retries → JSON.

## Tools
| Call | What you get | Price |
|---|---|---|
| `GET .../v1/leads/fda-recalls/{keyword}` | Recent FDA drug recalls (company, product, reason) | ~$0.05 |
| `GET .../v1/leads/fda-devices/{keyword}` | Recent FDA 510(k) device clearances | ~$0.05 |
| `GET .../v1/leads/fda-drugs/{keyword}` | FDA-approved drug products (sponsor, dosage) | ~$0.05 |
| `GET .../v1/lookup/drug-label/{name}` | FDA-approved drug label by brand/generic | ~$0.02 |
| `GET .../v1/bundle/device-360/{company}` | Device 360: clearances + recalls + adverse events | ~$0.18 |

(Base URL: `https://api.gocreativeai.com`)

## Why GoCreative
Live openFDA data (recalls, 510(k), labels), pay-per-call, no signup — the **only native recall/FDA feed for agents**.

*Provider: GoCreative — Agent Compliance & Data API · https://api.gocreativeai.com*
