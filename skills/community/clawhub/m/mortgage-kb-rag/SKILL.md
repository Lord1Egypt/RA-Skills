---
name: mortgage-kb-rag
description: Instant answers to mortgage, credit, and home-buying questions from a curated knowledge base. Ask anything about the buying process, credit repair, loan programs, or terminology — get accurate, sourced answers in seconds.
version: 1.0.2
author: drivenautoplex1
---

# Mortgage Knowledge Base RAG

Answer any mortgage or home-buying question instantly from a curated expert knowledge base. No hallucination — every answer is grounded in the indexed documents.

## What It Does

Given a plain-English question, this skill:

1. **Searches** the mortgage and real estate knowledge base using semantic similarity
2. **Retrieves** the most relevant passages (with source citations)
3. **Synthesizes** a clear, accurate answer — citing which document it came from
4. **Flags gaps** — if the question isn't in the knowledge base, says so rather than guessing

## Use Cases

- MLOs answering client questions quickly without Googling
- Real estate agents prepping for buyer consultations
- First-time buyers who need straight answers about the process
- Agents building FAQ content for their websites
- Verifying what a lender told you is actually correct

## Inputs

```json
{
  "query": "What credit score do I need to buy a house?",
  "category": "credit|loans|process|terminology|programs|investing",
  "detail_level": "brief|standard|detailed",
  "audience": "buyer|agent|mlo|investor"
}
```

- `query` (required): Any natural-language question about mortgages, credit, or home buying
- `category` (optional): Narrows search to a specific knowledge domain
- `detail_level` (optional, default: standard): How much detail to return
- `audience` (optional, default: buyer): Tailors language complexity to the reader

## Outputs

```json
{
  "answer": "To qualify for a conventional loan, most lenders require a minimum 620 credit score. FHA loans accept scores as low as 580 with 3.5% down, or 500 with 10% down. However, a score above 740 gets you the best rates — typically 0.5-1.0% lower APR than a 620, which translates to $150-300/month on a $350K loan.",
  "confidence": "high",
  "sources": [
    {
      "document": "First-Time Buyer Roadmap",
      "section": "Phase 1: Financial Snapshot",
      "relevance": 0.94
    },
    {
      "document": "90-Day Credit Repair Playbook",
      "section": "Home Price Math: Real Dollar Impact by Credit Tier",
      "relevance": 0.87
    }
  ],
  "related_questions": [
    "How do I improve my credit score in 90 days?",
    "What is the difference between FHA and conventional loans?",
    "How much does a 1-point credit score difference affect my mortgage rate?"
  ],
  "knowledge_gap": false
}
```

## Knowledge Base Coverage

The indexed knowledge base covers:

**Credit & Financing**
- Credit score tiers and their rate impact (real dollar math)
- The 5 credit factors and which to improve first
- FHA, conventional, VA, USDA loan programs
- Down payment assistance programs (national + state-level)
- Debt-to-income ratio calculation and limits
- What triggers hard vs. soft credit inquiries

**The Buying Process**
- Pre-approval vs. pre-qualification (what agents actually care about)
- Making competitive offers in different market conditions
- Inspection timelines and what to push back on
- Closing costs breakdown (who pays what)
- The 45-day closing timeline step-by-step
- What NOT to do after going under contract

**Credit Repair**
- Dispute letter process (FCRA rights)
- Pay-for-delete negotiation strategy
- Goodwill letter templates and when they work
- Credit utilization optimization (fastest score mover)
- Authorized user strategy
- 48-hour rapid rescore process

**Market & Terminology**
- 40+ glossary terms (escrow, PMI, LTV, DTI, rate lock, etc.)
- How to read a Loan Estimate (LE) vs. Closing Disclosure (CD)
- Rate lock timing strategy
- Understanding APR vs. interest rate

**Lead Nurture & Follow-Up (MLO/Agent Tools)**
- 90-day credit repair client journey
- Follow-up script patterns by lead stage
- Objection handling (rates, timing, affordability)

## Pricing

| Tier | Price | Queries |
|------|-------|---------|
| Single query | $1 | 1 question |
| Pack | $7 | 10 questions |
| Unlimited (30 days) | $19 | Unlimited |

## Technical Notes

- Knowledge base: ~450 Q&A pairs + sourced document passages
- Retrieval: TF-IDF + semantic re-ranking
- Latency: <2s for standard queries
- Hallucination guard: returns `knowledge_gap: true` if confidence < 0.70
- Updates: knowledge base refreshed monthly with new loan program data
