# Pitch Foundation Building

## Purpose
Develop the core value proposition and narrative foundation before building any presentation.

## When to Use
- "Help me build my pitch foundation"
- "What's our core value proposition?"
- "Why should anyone care about our product?"

## Core Questions to Answer

### 1. What Problem Exists?
**The question:** What pain exists in the world without your solution?

**Good answers:**
- Specific and concrete
- Quantified when possible
- Experienced by real people you've talked to
- Not solved well by current alternatives

**Example:**
```
❌ "People need better project management tools"
✅ "Engineering teams spend 8+ hours/week in status 
    meetings because there's no single source of truth 
    for project status. We interviewed 50 eng managers 
    and this was their #1 complaint."
```

### 2. Who Has This Problem?
**The question:** Who specifically experiences this pain, and how do you know?

**Good answers:**
- Specific persona, not "everyone"
- Direct evidence (interviews, surveys, usage data)
- Willing to pay for solution
- Accessible to reach

### 3. Why Your Solution?
**The question:** Why does your solution work better than alternatives?

**Good answers:**
- 10x better, not 10% better
- Defensible advantage
- Explains why others haven't done it
- Can be delivered at reasonable cost

### 4. What's the Business Model?
**The question:** How do you make money, and why does it work?

**Key elements:**
- Revenue model clear
- Unit economics make sense
- Path to profitability visible
- Market size justifies investment

### 5. What Traction Exists?
**The question:** What evidence proves the theory works?

**Traction types:**
- Revenue/customers
- Usage metrics
- Letters of intent
- Pilot results
- Waitlist size

### 6. Why You, Why Now?
**The question:** Why are you the right team, and why is timing right?

**Team credibility:**
- Domain expertise
- Previous relevant experience
- Technical capability
- Network in the space

**Timing factors:**
- Market readiness
- Technology enabling
- Regulatory changes
- Competitive landscape

## Data Structure

```json
{
  "foundations": [
    {
      "id": "FOUND-123",
      "company_name": "MyCo",
      "created_at": "2024-03-01",
      
      "problem": {
        "statement": "Engineering teams spend 8+ hours/week in status meetings",
        "evidence": "50 customer interviews, survey of 200 teams",
        "pain_level": "High - wasting 20% of engineering time",
        "current_solutions": "Spreadsheets, Slack, ad-hoc updates"
      },
      
      "target_customer": {
        "primary": "Engineering managers at 50-500 person tech companies",
        "size": "10,000 companies in US",
        "willingness_to_pay": "$50-200/seat/month"
      },
      
      "solution": {
        "description": "Auto-generated project status from code/commits",
        "key_differentiator": "Zero manual input required",
        "why_now": "AI/ML now capable of understanding code context"
      },
      
      "business_model": {
        "revenue_model": "SaaS subscription",
        "pricing": "$50/seat/month",
        "unit_economics": "CAC $500, LTV $3,000",
        "market_size": "$2B addressable market"
      },
      
      "traction": {
        "metrics": [
          {"name": "MRR", "value": "$15,000", "trend": "growing 20% MoM"},
          {"name": "Customers", "value": "12", "trend": "6 new this quarter"},
          {"name": "NPS", "value": "58", "trend": "improving"}
        ]
      },
      
      "team": {
        "founders": [
          {"name": "Jane Doe", "background": "Ex-Eng Director at Stripe", "role": "CEO"},
          {"name": "John Smith", "background": "Tech Lead at Google", "role": "CTO"}
        ],
        "why_now": "Remote work has made status visibility critical"
      }
    }
  ]
}
```

## Script Usage

```bash
# Build foundation
python scripts/build_foundation.py \
  --company "MyCo" \
  --problem "Engineering status visibility" \
  --solution "Auto-generated status from code"

# View foundation
python scripts/view_foundation.py --foundation-id "FOUND-123"

# Update traction metrics
python scripts/update_foundation.py \
  --foundation-id "FOUND-123" \
  --field "traction.mrr" \
  --value "20000"

# Analyze gaps
python scripts/analyze_foundation.py --foundation-id "FOUND-123"
```

## Output Format

```
PITCH FOUNDATION ANALYSIS
Company: MyCo
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROBLEM STATEMENT ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Statement: Engineering teams spend 8+ hours/week in status meetings
Evidence: 50 customer interviews, survey of 200 teams
Pain level: High (20% of engineering time wasted)
Current alternatives: Spreadsheets, Slack, ad-hoc

Strength: Strong quantitative evidence
Gap: Could use one customer quote/testimonial

TARGET CUSTOMER ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Primary: Engineering managers at 50-500 person tech companies
Market size: 10,000 companies in US
Willingness to pay: $50-200/seat/month confirmed

Strength: Specific and testable
Gap: Consider defining secondary personas

SOLUTION ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Description: Auto-generated project status from code/commits
Key differentiator: Zero manual input required
Why now: AI/ML now capable of understanding code context

Strength: Clear 10x improvement over status quo
Gap: Need to explain technical feasibility more

BUSINESS MODEL ⚠️
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Revenue: SaaS at $50/seat/month
Unit economics: CAC $500, LTV $3,000 (6:1 ratio ✅)
Market size: $2B addressable

Strength: Healthy unit economics
Gap: CAC seems low - verify with actual data

TRACTION ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MRR: $15,000 (growing 20% MoM)
Customers: 12 (6 new this quarter)
NPS: 58

Strength: Real revenue, growth trending up
Gap: Need retention/cohort data

TEAM ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Jane Doe - CEO: Ex-Eng Director at Stripe
John Smith - CTO: Tech Lead at Google

Strength: Deep domain expertise
Gap: Consider adding advisor with go-to-market experience

WHY NOW ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Remote work has made status visibility critical
Market timing: 2020-2024 shift to distributed teams

FOUNDATION STRENGTH: 8.5/10
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Strong foundation with good evidence.
Recommended focus: Get CAC data, add testimonials.

Ready for: Seed stage investor conversations
Next milestone: $30K MRR for Series A prep
```

## Common Weaknesses to Fix

### Vague Problem
❌ "People struggle with productivity"
✅ "Engineering managers waste 8 hours/week in status meetings"

### Weak Differentiation
❌ "We're better than competitors"
✅ "We require zero manual input vs. 2 hours/day for alternatives"

### No Evidence
❌ "We think customers want this"
✅ "50 interviews confirm this is their #1 problem"

### Bad Unit Economics
❌ "We'll make money at scale"
✅ "CAC $500, LTV $3,000, payback in 6 months"

### Unrealistic Market Size
❌ "$100B market"
✅ "10,000 target companies × $50K ACV = $500M SAM"
