# Noise-to-Gold Pipeline

The complete processing pipeline that transforms raw daily-life noise into actionable wealth opportunities.

---

## Pipeline Overview

```
INPUT (daily noise)
    |
    v
STAGE 1: INGEST
    |
    v
STAGE 2: SCAN
    |
    v
STAGE 3: CROSS-REFERENCE
    |
    v
STAGE 4: SCORE
    |
    v
STAGE 5: RANK
    |
    v
STAGE 6: RECOMMEND
    |
    v
STAGE 7: EVOLVE
    |
    v
REPEAT (next input enters at Stage 1)
```

---

## Stage 1: INGEST

### What Happens

Raw input of any format is accepted and normalized into a standardized internal representation.

### Supported Input Types

| Type | Format | Normalization |
|------|--------|---------------|
| Slack/Teams | Text dump | Speaker tags removed, timestamps normalized |
| Text/WhatsApp | Text or screenshots | OCR if needed, names anonymized if requested |
| Photos | Image files | Image analysis, text extraction |
| Browsing history | URL list or summary | Topic clustering, intent classification |
| YouTube history | Watch history export | Content categorization, engagement scoring |
| Purchase history | Receipts or order confirmations | Amount extraction, category tagging |
| Complaints | Free text | Sentiment analysis, repetition detection |
| Meeting notes | Bullet points or paragraphs | Decision extraction, action item tagging |
| Social media | Feed screenshots or exports | Topic clustering, engagement patterns |

### Normalization Rules

1. **Deduplication:** Remove exact duplicates
2. **Anonymization:** Optional name/company replacement for privacy
3. **Timestamp parsing:** Extract dates, establish sequence
4. **Source tagging:** Label input type for cross-reference weighting
5. **Volume estimation:** Count items, estimate density

### Output

```json
{
  "ingest_timestamp": "2026-04-09T10:30:00Z",
  "input_type": "slack_messages",
  "input_summary": "47 messages from #engineering channel, spanning 5 business days",
  "normalized_items": 47,
  "dedup_rate": 0.04,
  "date_range": ["2026-04-01", "2026-04-05"],
  "raw_preview": ["first 3 items for reference"]
}
```

### Failure Modes

| Failure | Cause | Solution |
|---------|-------|----------|
| Zero items parsed | Format not recognized | Fall back to raw text, manual processing |
| Over-deduplication | Similar-but-different items removed | Lower deduplication threshold |
| Timestamp confusion | Mixed formats (12h/24h, timezones) | Default to UTC, flag for user confirmation |

---

## Stage 2: SCAN

### What Happens

Normalized input is processed through all six extraction lenses simultaneously. Each item is evaluated for signal potential.

### The Six Lenses

1. **Money Signal Detection** — Where is money moving, stuck, or leaking?
2. **Demand Gap Identification** — What do people want that nobody provides?
3. **Arbitrage Window Detection** — Where is value being mispriced?
4. **Skill-to-Revenue Bridge** — What does the user know that has market value?
5. **Network Monetization Path** — Who should be talking to whom?
6. **Behavioral Leverage Point** — What repeated behavior is one pivot from revenue?

### Scanning Rules

Each normalized item goes through:
1. **Keyword extraction** — Identify financially relevant terms
2. **Sentiment scoring** — Positive/negative emotional charge
3. **Repetition check** — Has this or similar appeared before?
4. **Context mapping** — Who said this, to whom, in what context?
5. **Signal tagging** — Assign primary lens and sub-type

### Output

```json
{
  "scan_timestamp": "2026-04-09T10:32:00Z",
  "items_scanned": 47,
  "signals_found": 8,
  "lens_distribution": {
    "money_signal": 2,
    "demand_gap": 3,
    "arbitrage": 1,
    "skill_bridge": 1,
    "network_path": 0,
    "behavioral_leverage": 1
  },
  "signal_items": [
    {
      "id": "sig-001",
      "original_text": "the AWS bill is insane this month",
      "lens": "money_signal",
      "subtype": "cost_complaint",
      "raw_confidence": 0.35,
      "speakers": ["dave"],
      "mentions": ["AWS", "cost"]
    }
  ]
}
```

### Failure Modes

| Failure | Cause | Solution |
|---------|-------|----------|
| No signals found | Input genuinely has no signal | Accept as valid null result |
| Too many signals | Over-sensitive scanning | Raise keyword threshold |
| Wrong lens assignment | Ambiguous content | Flag for human review, adjust keywords |

---

## Stage 3: CROSS-REFERENCE

### What Happens

Newly found signals are compared against the existing signal database. Connections, confirmations, and convergences are identified.

### Cross-Reference Types

| Type | Description | Confidence Impact |
|------|-------------|-------------------|
| **Confirmation** | Same signal from different source | +20-40% |
| **Convergence** | Different signals pointing to same opportunity | +30-50% |
| **Contradiction** | Signal refuted by existing data | -30-50% |
| **Expansion** | New signal extends existing opportunity | +15-25% |
| **Novelty** | Completely new signal type | +10% (novelty bonus) |

### Cross-Reference Algorithm

```
For each new_signal:
  1. Find opportunities with matching topic/industry
  2. Score semantic similarity to existing signals
  3. If similarity > 0.7: CROSS-REFERENCE detected
  4. Determine reference type (confirmation/convergence/expansion)
  5. Calculate confidence adjustment
  6. Update opportunity confidence scores
```

### Evidence Chain Building

When cross-references occur, Midas builds evidence chains:

```
Opportunity: Contractor marketplace for local neighborhood

Evidence Chain:
├── Slack message (2026-04-01): "contractor costs are killing us" [confidence: 25%]
├── Photo (2026-04-02): Active construction site on Oak Street [confidence: 30%]
├── Slack message (2026-04-03): "has anyone used that new contractor referral site?" [confidence: 35%]
└── Photo (2026-04-05): New housing development permit signage [confidence: 30%]

Stacked Confidence: 68%
Pattern Match: Thiel's "small monopoly in ignored niche"
```

### Output

```json
{
  "cross_ref_timestamp": "2026-04-09T10:35:00Z",
  "new_signals": 8,
  "cross_references_found": 3,
  "opportunities_affected": 2,
  "confidence_changes": [
    {
      "opportunity_id": "opp-001",
      "opportunity_title": "Local contractor referral service",
      "before_confidence": 0.35,
      "after_confidence": 0.68,
      "change_reason": "3 converging signals from different input types",
      "new_evidence": ["slack complaint", "construction photo", "permit signage"]
    }
  ],
  "evidence_chains": [
    {
      "opportunity": "Local contractor referral service",
      "chain_length": 3,
      "chain_items": ["sig-001", "sig-004", "sig-007"]
    }
  ]
}
```

### Failure Modes

| Failure | Cause | Solution |
|---------|-------|----------|
| False connections | Over-eager semantic matching | Raise similarity threshold |
| Missing connections | Under-sensitive matching | Lower threshold, manual review |
| Circular references | Opportunities referencing each other | Deduplicate evidence chains |

---

## Stage 4: SCORE

### What Happens

Each opportunity receives a final confidence score based on all available evidence.

### Scoring Formula

```
Final_Confidence = Base_Confidence × Evidence_Multiplier × Pattern_Multiplier

Where:
- Base_Confidence = Initial signal strength (15-40%)
- Evidence_Multiplier = 1 + (cross_ref_count × 0.15) + (convergence_count × 0.25)
- Pattern_Multiplier = 1.0 (no pattern match) to 1.3 (strong billionaire pattern match)
```

### Confidence Thresholds

| Threshold | Status | Recommended Action |
|-----------|--------|-------------------|
| 0-15% | Speculation | Note, monitor |
| 15-35% | Weak signal | Keep feeding related inputs |
| 35-55% | Moderate signal | Design validation test |
| 55-70% | Strong signal | Allocate small resources |
| 70-90% | Very strong signal | ACT — commit real resources |
| 90%+ | Near certain | Execute with risk management |

### Scoring Criteria by Lens

**Money Signal:**
- Explicit price mentioned: +15%
- Multiple confirmations: +20%
- Recurring expense: +15%
- Actively seeking alternatives: +20%

**Demand Gap:**
- 3+ people with same gap: +30%
- Manual workaround visible: +15%
- Willingness to pay implied: +15%
- Feasible solution exists: +10%

**Arbitrage:**
- Price comparison available: +25%
- Access to cheaper source: +20%
- Low execution friction: +15%
- Not already exploited: +15%

**Skill Bridge:**
- 3+ months consistent activity: +20%
- Others value input: +20%
- Been paid before: +25%
- Clear monetization model: +15%

**Network Path:**
- Both parties searching: +20%
- Budget confirmed: +20%
- Relationship with both: +15%
- Finder's fee standard: +15%

**Behavioral Leverage:**
- Daily repetition: +20%
- Generates external value: +25%
- Adjacent monetization exists: +20%
- Low pivot effort: +15%

### Output

```json
{
  "score_timestamp": "2026-04-09T10:38:00Z",
  "opportunities_scored": 5,
  "score_distribution": {
    "0-15": 0,
    "15-35": 1,
    "35-55": 2,
    "55-70": 1,
    "70-90": 1,
    "90+": 0
  },
  "opportunities": [
    {
      "id": "opp-001",
      "title": "Local contractor referral service",
      "final_confidence": 0.68,
      "confidence_breakdown": {
        "base": 0.30,
        "evidence_multiplier": 1.75,
        "pattern_multiplier": 1.10
      },
      "lens": "demand_gap",
      "effort_estimate": "medium",
      "upside_estimate": "$3K-10K/month potential"
    }
  ]
}
```

---

## Stage 5: RANK

### What Happens

Opportunities are ordered by priority using a composite ranking formula.

### Ranking Formula

```
Priority_Score = (Confidence × Upside_Value) / Execution_Effort

Where:
- Confidence = 0.0 to 1.0
- Upside_Value = 1 (low) to 5 (high)
- Effort = 1 (low) to 5 (high)
```

### Effort Estimation

| Level | Definition | Examples |
|-------|------------|----------|
| 1 - Minimal | Can do in <1 hour | Send an email introduction |
| 2 - Low | Can do in <1 day | Create simple landing page |
| 3 - Medium | Can do in 1-4 weeks | Build MVP, run small campaign |
| 4 - High | Can do in 1-3 months | Build full product, hire team |
| 5 - Very High | Requires significant resources | Raise funding, build company |

### Upside Estimation

| Level | Definition | Examples |
|-------|------------|----------|
| 1 - Low | Side income potential | $500-2K/month |
| 2 - Moderate | Part-time income | $2K-5K/month |
| 3 - Good | Full-time replacement | $5K-15K/month |
| 4 - High | Significant business | $15K-50K/month |
| 5 - Very High | Company-scale potential | $50K+/month |

### Output

```json
{
  "rank_timestamp": "2026-04-09T10:40:00Z",
  "ranked_opportunities": [
    {
      "rank": 1,
      "id": "opp-001",
      "title": "Local contractor referral service",
      "priority_score": 2.72,
      "confidence": 0.68,
      "upside": 4,
      "effort": 3,
      "recommendation": "HIGH PRIORITY — ACT"
    },
    {
      "rank": 2,
      "id": "opp-002",
      "title": "Internal reporting automation",
      "priority_score": 1.50,
      "confidence": 0.50,
      "upside": 3,
      "effort": 3,
      "recommendation": "MODERATE — Test small"
    }
  ]
}
```

---

## Stage 6: RECOMMEND

### What Happens

Midas generates actionable output with specific next steps for the highest-priority opportunities.

### Output Format

```
[MIDAS SIGNAL REPORT]

Input type: Slack messages
Input size: 47 messages, 5 days
Scan date: 2026-04-09

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HIGHEST PRIORITY: Local contractor referral service
Confidence: 68% | Priority Score: 2.72 | Status: ACT NOW

Evidence Chain (3 converging signals):
  1. Dave (2026-04-01): "contractor costs are killing us"
  2. Photo (2026-04-02): Active construction on Oak Street
  3. Sarah (2026-04-03): "has anyone used contractor referral sites?"

Pattern Match: Thiel's playbook — small monopoly in ignored niche

Estimated Upside: $3K-10K/month
Estimated Effort: Medium (3-4 weeks to MVP)

IMMEDIATE NEXT ACTIONS:
  1. Text Dave: "Hey, can you send me 3 contractor names you've used?"
  2. Drive by Oak Street construction, note company signage
  3. Research existing contractor referral services in your area

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SECOND PRIORITY: Internal reporting automation
Confidence: 50% | Priority Score: 1.50 | Status: TEST SMALL

[Similar detailed output]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SIGNALS EXTRACTED: 8 total
  - Demand gaps: 3
  - Money signals: 2
  - Arbitrage: 1
  - Skill bridges: 1
  - Behavioral leverage: 1

NOISE DISCARDED: 39 items
  - Personal chat: 28
  - Unrelated work: 11

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Action Language Requirements

Every recommendation MUST include:
1. **Specific verb** — What exactly to do
2. **Specific noun** — The exact target
3. **Timeline** — When to do it by
4. **Success metric** — How to know it worked

### Failure Modes

| Failure | Cause | Solution |
|---------|-------|----------|
| Vague recommendations | Over-generalized analysis | Force specificity: "Text X about Y" |
| Too many recommendations | Low filtering threshold | Limit to top 3 per session |
| No prioritization | Equal weighting | Apply ranking formula strictly |

---

## Stage 7: EVOLVE

### What Happens

All session data is logged to the evolution file for cumulative learning.

### Evolution Log Format

```json
{
  "timestamp": "2026-04-09T10:45:00Z",
  "input_type": "slack_messages",
  "input_summary": "47 messages from #engineering, 5 days",
  "session_metrics": {
    "items_ingested": 47,
    "signals_extracted": 8,
    "signals_discarded": 39,
    "cross_references_found": 3,
    "new_opportunities": 2,
    "updated_opportunities": 1,
    "opportunities_closed": 0
  },
  "opportunities": [
    {
      "id": "opp-001",
      "title": "Local contractor referral service",
      "confidence_before": 0.35,
      "confidence_after": 0.68,
      "confidence_delta": "+0.33",
      "evidence_chain": ["sig-001", "sig-004", "sig-007"],
      "lens": "demand_gap",
      "effort": "medium",
      "upside": "$3K-10K/month",
      "next_actions": ["Text Dave for contractor names", "Drive by Oak Street", "Research local services"],
      "pattern_match": "thiel_small_monopoly"
    }
  ],
  "cross_references": [
    {
      "type": "convergence",
      "signals": ["sig-001", "sig-004", "sig-007"],
      "opportunity": "opp-001"
    }
  ]
}
```

### Evolution Purposes

1. **Memory:** Track what you've learned across sessions
2. **Conviction building:** Show confidence growth over time
3. **Pattern recognition:** Identify recurring opportunity types
4. **Audit trail:** Understand why you made past decisions
5. **Compounding:** Enable increasingly sophisticated analysis

### Long-term Evolution Analysis

Periodically, Midas should analyze the evolution log to identify:

- **Recurring opportunity types:** What categories keep appearing?
- **Success patterns:** Which opportunities actually led to action and results?
- **Failure patterns:** Which high-confidence opportunities never materialized?
- **Learning velocity:** How fast is conviction building for different opportunity types?

---

## Pipeline Best Practices

### Input Quality

- Feed Midas varied input types for better cross-referencing
- Include timestamps when possible for sequence analysis
- Don't filter "noise" — let Midas decide what's signal
- Feed regularly — weekly minimum for active users

### Signal Confidence

- Trust the stacking formula — single signals are weak
- Be patient — conviction builds over multiple inputs
- Act at 70%+ confidence — waiting for 100% means never acting

### Action Orientation

- Every recommendation needs a specific next action
- Execute before perfect — small tests are better than no tests
- Log results — what worked and what didn't makes Midas smarter

### Honest Boundaries

- Midas finds gold — you have to pick it up
- No predictions — only pattern recognition
- No guarantees — confidence isn't certainty
- Human judgment required — Midas advises, you decide
