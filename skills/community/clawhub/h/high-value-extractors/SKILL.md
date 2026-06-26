---
name: high-value-extractors
description: Extract structured data from product pages, job listings, and company pages. Plus generate working AI endpoints from schemas. LLM-powered extraction micro-services.
---

# High-Value Extractors

Four LLM-powered extraction services for structured data.

## Services

### /extract-product — Product Page to Data
E-commerce URL to structured product data.
```
POST /x402s/extract-product
Body: {"url": "https://amazon.com/dp/..."}
Response: {"product": {"name": "...", "price": "$29.99", "brand": "...", "specs": {...}}}
Price: $0.02 USDC
```

### /extract-job — Job Listing to Data
Job listing URL to structured data.
```
POST /x402s/extract-job
Body: {"url": "https://linkedin.com/jobs/..."}
Response: {"job": {"title": "...", "company": "...", "salary": "...", "requirements": [...]}}
Price: $0.02 USDC
```

### /extract-contact — Company Intel
Company page to contact/company intelligence.
```
POST /x402s/extract-contact
Body: {"url": "https://company.com/about"}
Response: {"company": {"name": "...", "industry": "..."}, "emails": [...], "phones": [...]}
Price: $0.02 USDC
```

### /create-endpoint — Schema to Working Endpoint
Describe what you want, get working FastAPI code back.
```
POST /x402s/create-endpoint
Body: {"name": "sentiment", "description": "Analyze text sentiment", "input_schema": {...}, "output_schema": {...}}
Response: {"code": "async def sentiment(request):\n  ...", "model": "claude-sonnet-4-6"}
Price: $0.10 USDC
```

## Payment
x402 protocol — USDC on Base.
