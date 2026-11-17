---
name: Classify Customer Intents with AI — Route to Slack & CRM
description: "Classify customer micro-moments into Buy Now, Research, Frustration, Advocacy, or Churn Risk with confidence scores. Use when the user needs real-time intent detection, personalized next actions, or audience segmentation from support tickets, DMs, and comments."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🎯"
    }
  }
---

## Overview

The **Micro-Moment Intent Classifier** is a real-time AI skill that analyzes customer interactions—support tickets, Slack DMs, form submissions, comments, and emails—to instantly classify intent into 5 actionable buckets with confidence scores and recommended next actions.

**Why This Matters:**
Customer intent shifts moment-to-moment. A frustrated user in a support ticket isn't ready for upselling; a research-phase prospect needs education, not a sales call. This skill bridges the gap between raw customer data and intelligent routing, enabling personalized workflows that convert, retain, and delight.

**Primary Use Cases:**
- Real-time support ticket triage → route to retention specialists vs. sales
- Customer success sentiment tracking → identify churn risk before they leave
- Product feedback analysis → separate feature requests (advocacy) from bugs (frustration)
- Sales pipeline enrichment → automate nurture sequences based on research vs. buy-ready signals
- Multi-channel monitoring → unify intent detection across Slack, email, comments, forms

**Integrations & Platforms:**
Works seamlessly with Slack, WordPress, HubSpot, Zendesk, Intercom, Email inboxes, Google Sheets, n8n, Make, Zapier, and custom APIs.

---

## Quick Start

### Example 1: Analyze a Support Ticket

```
Analyze this support ticket and classify the customer's micro-moment intent:

Ticket: "Your product is missing the bulk export feature I need. 
I've been looking for solutions for 3 weeks and I'm considering 
switching to your competitor if this isn't added by month-end."

Return: intent classification with confidence scores and recommended action.
```

**Expected Output:**
- **Primary Intent:** Research (72% confidence)
- **Secondary Intent:** Churn Risk (68% confidence)
- **Recommended Action:** Schedule product roadmap call + create feature tracking ticket
- **Reasoning:** Customer is evaluating alternatives; educational content won't help—they need commitment/timeline.

---

### Example 2: Classify Multiple Social Comments

```
Batch classify these 3 Twitter replies to our latest product announcement:

1. "Just launched! Excited to try this. Quick Q—does it integrate with Salesforce?"
2. "Another feature nobody asked for. Still waiting for you to fix the API docs."
3. "This is amazing! I'm definitely buying an enterprise plan for my team."

Provide intent scores, segments, and nurture recommendations for each.
```

**Expected Output:**
| Comment | Primary Intent | Confidence | Recommended Action |
|---------|----------------|------------|--------------------|
| Comment 1 | Research | 81% | Send integration guide + demo video |
| Comment 2 | Frustration | 88% | Route to Support Lead + bug tracker |
| Comment 3 | Buy Now | 94% | Trigger sales team notification + enterprise onboarding |

---

### Example 3: Real-Time Slack DM Monitoring

```
Monitor this Slack DM from a key customer and classify intent:

"Hey! We're rolling out to 50 new teams next quarter and need 
custom SSO + audit logs. What's the fastest path to get this set up?"

Include: intent bucket, urgency level, deal size indicator, and 
suggested response playbook.
```

**Expected Output:**
- **Intent:** Buy Now (92% confidence)
- **Urgency:** High (immediate need)
- **Deal Signal:** Enterprise expansion (50 new teams)
- **Playbook:** "Enterprise Sales Fast-Track" → schedule CSM + solution architect

---

## Capabilities

### 1. Five-Bucket Intent Classification

The skill categorizes every customer interaction into one of these micro-moments:

| Intent Bucket | Definition | Confidence Score | Typical Signals |
|---------------|-----------|-------------------|-----------------|
| **Buy Now** | Ready to purchase or upgrade | 0–100% | "pricing," "demo," "buy," urgent language |
| **Research** | Evaluating options, gathering info | 0–100% | "does it support," "vs.", "alternatives," questions |
| **Frustration** | Upset, experiencing friction | 0–100% | "not working," "failed," "disappointed," complaints |
| **Advocacy** | Promoting product, love signaling | 0–100% | "amazing," "recommend," sharing wins, testimonials |
| **Churn Risk** | Considering leaving/switching | 0–100% | "competitor," "canceling," "better options," deadline threats |

**How It Works:**
- Ingests raw text (any length, any format)
- Applies multi-stage NLP + LLM reasoning
- Outputs all 5 confidence scores (not binary)
- Identifies secondary intents (e.g., Frustration + Churn Risk)
- Contextualizes based on customer history (optional)

### 2. Recommended Next Actions

Automatically suggests playbooks tailored to detected intent:

- **Buy Now** → Sales outreach, pricing page, demo scheduling, contract templates
- **Research** → Comparison guides, webinars, feature documentation, use-case videos
- **Frustration** → Support escalation, bug tracking, priority queue, gesture (discount/credit)
- **Advocacy** → Case study request, referral program, community spotlight, VIP engagement
- **Churn Risk** → Retention specialist call, product roadmap transparency, custom solutions review

### 3. Batch & Stream Processing

- **Batch:** Analyze 100+ tickets/comments in one pass
- **Stream:** Connect to Slack, email, form APIs for real-time classification
- **Continuous Learning:** Optionally log classifications for model refinement

### 4. Multi-Channel Input Support

- Support tickets (Zendesk, Freshdesk, Intercom JSON)
- Email (raw text or parsed headers)
- Slack messages + threads
- Social media comments (Twitter, LinkedIn, Reddit)
- Form submissions & feedback
- Custom data sources (CSV, webhook payloads)

### 5. Confidence & Explainability

Each classification includes:
- All 5 intent scores (not just top pick)
- Key phrases that triggered the classification
- Explainability reasoning ("Customer mentioned 3 churn signals")
- Confidence threshold warnings ("Below 65%—manually review recommended")

---

## Configuration

### Environment Variables

```bash
# Required
export OPENAI_API_KEY="sk-..."  # OpenAI GPT-4 Turbo or better

# Optional
export CONFIDENCE_THRESHOLD="0.65"  # Minimum confidence to auto-action
export INCLUDE_REASONING="true"      # Return explanation text
export MAX_BATCH_SIZE="100"          # Batch processing limit
export CONTEXT_LOOKBACK_DAYS="90"    # Historical context window
```

### Setup Instructions

1. **Get API Key:** https://platform.openai.com/account/api-keys
2. **Set Environment:**
   ```bash
   export OPENAI_API_KEY="your-key-here"
   ```
3. **Test Classification:**
   ```
   Classify this: "Love your product! Just referred my entire team."
   ```
4. **Integrate with Workflows:**
   - Connect via Zapier, Make, n8n, or custom API calls
   - Route classifications to Slack channels, Airtable, Salesforce, HubSpot
   - Trigger follow-up automations based on intent buckets

### Optional Configuration

- **Custom Intent Buckets:** Modify the 5 categories to match your business (e.g., swap "Buy Now" for "Feature Request")
- **Industry Presets:** Load templates for SaaS, E-commerce, Support, Community, etc.
- **Language Support:** English, Spanish, French, German, Mandarin (specify in request)
- **PII Handling:** Automatically redact emails, phone numbers, customer IDs before processing

---

## Example Outputs

### Output Format 1: Single Classification (JSON)

```json
{
  "input_text": "We need SSO and audit logs by EOQ for compliance. Can we make this happen?",
  "timestamp": "2024-01-15T14:32:00Z",
  "primary_intent": "Buy Now",
  "intent_scores": {
    "buy_now": 0.89,
    "research": 0.34,
    "frustration": 0.08,
    "advocacy": 0.12,
    "churn_risk": 0.15
  },
  "confidence": 0.89,
  "recommended_action": "Enterprise Sales Fast-Track",
  "playbook": "Schedule 15-min call with Solutions Architect within 4 hours",
  "key_signals": ["compliance", "EOQ deadline", "specific features"],
  "reasoning": "Customer specified exact features + hard deadline = purchase intent",
  "secondary_intent": "Research",
  "urgency_level": "High"
}
```

### Output Format 2: Batch Results (CSV)

```
timestamp,channel,customer_id,text_preview,primary_intent,confidence,secondary_intent,recommended_action
2024-01-15T14:15:00Z,slack,cust_001,"Quick question about...",Research,0.78,Buy Now,Send technical docs + demo
2024-01-15T14:22:00Z,email,cust_002,"Your API is broken",Frustration,0.92,,Escalate to support lead
2024-01-15T14:31:00Z,twitter,cust_003,"Amazing product! Just told...",Advocacy,0.95,,Feature in case study
```

### Output Format 3: Dashboard Summary

```
Today's Micro-Moment Breakdown (47 interactions):

Buy Now (8 customers) — 17% → Auto-route to sales
Research (18 customers) — 38% → Send nurture drip
Advocacy (7 customers) — 15% → Launch referral outreach
Frustration (9 customers) — 19% → Support escalation
Churn Risk (5 customers) — 11% → Retention squad alert

Recommended Revenue Impact: +$156K (enterprise deals) + $34K (upsells)
Retention Saves: $78K (5 customers at risk, intervention possible)
```

---

## Tips & Best Practices

### 1. Pair Intent with Customer LTV
Combine classification with customer lifetime value data:
- **High-LTV + Churn Risk** = CEO-level retention call
- **Low-LTV + Frustration** = Self-serve support knowledge base
- **Mid-LTV + Buy Now** = Account manager touch

### 2. Use Secondary Intents
Don't ignore the second-highest score. A customer might be:
- **Frustrated (primary) + Churn Risk (secondary)** = They're upset AND considering leaving
- Act on both: fix the issue + create win-back sequence

### 3. Set Dynamic Thresholds
- **< 65% confidence** → Manual review queue
- **65–80% confidence** → Auto-route with human flag
- **> 80% confidence** → Full automation

### 4. Monitor False Positives
Log misclassifications to a Slack channel daily. Over time, refine prompts or swap to custom fine-tuning model.

### 5. Combine with Sentiment Analysis
Pair intent classification with sentiment (positive/negative/neutral) for richer routing:
- Positive + Buy Now = Hot lead
- Negative + Frustration = VIP support priority
- Neutral + Research = Standard nurture

### 6. A/B Test Playbooks
Once you know intent, test 2–3 response templates:
- **Playbook A:** Educational webinar → nurture sequence
- **Playbook B:** Live demo call → faster conversion
- Track conversion rate by playbook to find your winner

### 7. Real-Time Dashboards
Connect outputs to a live dashboard (Google Sheets, Tableau, Metabase) showing:
- Hourly intent distribution
- Response time by bucket
- Conversion rate per playbook
- Churn risk alerts

### 8. Batch + Stream Hybrid
- **Batch (Weekly):** Analyze all past week's tickets for insights
- **Stream (Real-Time):** Classify new messages as they arrive for immediate action

---

## Safety & Guardrails

### What This Skill WILL Do
✅ Classify intent from text interactions  
✅ Suggest next actions based on detected signals  
✅ Return confidence scores for human review  
✅ Handle multiple languages  
✅ Provide explainability reasoning  

### What This Skill WILL NOT Do
❌ **Make final decisions** → Always flag low-confidence classifications for human review (< 65%)  
❌ **Automatically send emails/messages** → Returns recommendations only; humans control outreach  
❌ **Guarantee perfect accuracy** → Depends on input quality; ambiguous text may score evenly across buckets  
❌ **Access customer data without consent** → Requires explicit permission to analyze; doesn't store or log data (unless configured)  
❌ **Override business logic** → Recommendations are suggestions, not rules; your playbooks take precedence  
❌ **Detect sarcasm 100%** → Sarcasm and irony may be misclassified; review high-confidence satire flagged by human reviewers  

### Limitations & Boundaries

1. **Context Dependency:** Intent classification is strongest with 100+ characters of context. Very short messages ("Yes!" or "When?") may score evenly.

2. **Language Bias:** Model trained primarily on English SaaS interactions. Non-English text or industry-specific jargon may be misclassified.

3. **API Rate Limits:** OpenAI has throttling; batch processing may queue during peak usage.

4. **Cost:** ~$0.01–0.05 per classification depending on text length; budget $500–2000/month for 100K+ classifications.

5. **Freshness:** Model has a knowledge cutoff; very recent product names or memes may not be recognized.

### Data Privacy & Compliance

- **No Data Retention:** By default, skill does not log or store customer text
- **PII Redaction:** Enable flag to auto-remove emails, phone numbers, SSNs before processing
- **GDPR/CCPA:** Compliant; classify without storing personally identifiable information
- **SOC 2:** If using OpenAI's API, ensure you've reviewed OpenAI's data handling policies

---

## Troubleshooting

### Q: My classification returned 5 equal scores (20% each). Why?
**A:** Input text was too ambiguous or contradictory. Add more context:
- Share previous conversation history
- Include customer segment/LTV data
- Clarify if this is a reply or new message

### Q: Confidence is below 65%. Should I still act?
**A:** No. Put it in a manual review queue. Examples of ambiguous cases:
- "Let me think about it" (could be Research or Churn Risk)
- Sarcasm or irony without clear markers
- Multi-intent messages (frustration + interest in upselling)

### Q: The skill classified this as "Research" but I know it's "Buy Now."
**A:** This is common with formal procurement language. Try rephrasing your context or add customer history (e.g., "This customer has been in our sales pipeline for 6 months"). Consider logging this as feedback to improve future classifications.

### Q: I'm getting too many false positives in the "Churn Risk" bucket.
**A:** Tighten the threshold. In configuration, set:
```
CHURN_RISK_THRESHOLD="0.75"  # Require 75%+ confidence vs. default 65%
```
Or review the key signals detected—you may need to exclude common red herrings in your industry.

### Q: Can I use this with non-English languages?
**A:** Yes. Specify in your request:
```
Language: Spanish
Classify this: "Me encanta vuestro producto pero necesitaré SSO para mi empresa."
```
Note: Confidence may be slightly lower (3–5%) for non-English text. German and French perform best; other languages may need custom tuning.

### Q: How do I integrate this with Slack?
**A:** Use a Slack bot + webhook:
1. In Slack app settings, enable incoming webhooks
2. Create an n8n or Zapier workflow