# Styx Enrichment Pipeline

The pipeline resolves garbled/obfuscated transaction names into real businesses.

## When to enrich

1. Initial load — after first Plaid historical pull
2. After each incremental sync (new transactions)
3. On-demand — when a consumer skill needs a specific merchant resolved

## Pipeline stages

```
Stage 1: EXACT MATCH
  → Check if merchant_name or name already matches a known merchant
  → If yes, create link with confidence 1.0, skip remaining stages

Stage 2: FUZZY MATCH
  → Normalize the transaction name (strip prefixes like ABM-, TCB*, MED*, DD *)
  → Fuzzy match against existing merchants table
  → If similarity > 0.85, create link with confidence 0.9

Stage 3: SEARCH (SearXNG)
  → Query SearXNG with cleaned name + "San Francisco" (user's city)
  → Parse results for business name, address, category
  → If found, create merchant + link with confidence 0.8

Stage 4: LLM RESOLUTION
  → For remaining unresolved transactions, use LLM to identify the business
  → Input: transaction name, amount, category, personal_finance_category
  → Output: business name, category, confidence
  → Create merchant + link with LLM-assessed confidence

Stage 5: MANUAL REVIEW QUEUE
  → Transactions with confidence < 0.5 go to review queue
  → File: {agent_root}/data/styx/review_queue.jsonl
  → User can review and confirm/reject
```

## Name cleaning rules

Common patterns in Plaid transaction names:

| Pattern | Type | Cleaning |
|---------|------|----------|
| `ABM-350 MISSION GARAGE` | Prefix | Strip `ABM-` prefix |
| `TCB*MTA METER MTA P` | Prefix | Strip `TCB*` prefix |
| `MED*UCSF HEALTH` | Prefix | Strip `MED*` prefix |
| `DD *DOORDASH ROYALINDI` | Prefix | Strip `DD *DOORDASH ` prefix |
| `FSP*ALVES CLEANING SF` | Prefix | Strip `FSP*` prefix |
| `ABC*BAKAR FITNESS CENT` | Prefix | Strip `ABC*` prefix |
| `TST*TARTINE MANUFACTOR` | Prefix | Strip `TST*` prefix |
| `***************` | Redacted | Skip, no enrichment possible |
| `eBay O***-*****-*****` | Redacted | Use base name (eBay) |
| `UNITED **************` | Redacted | Use base name (United) |
| `UBER *ONE MEMBERSHIP` | Asterisk | Strip after ` *` for matching |