# Objection Handling

## Purpose
Prepare for the hardest questions your pitch will face and develop honest, effective responses.

## When to Use
- "What questions will investors ask?"
- "How do I handle objection X?"
- "What are my weak points?"

## Common Objection Categories

### Market & Competition
- "Isn't this market crowded?"
- "What if Google/Facebook builds this?"
- "How big is this market really?"
- "Why hasn't this been done before?"

### Team & Execution
- "Do you have relevant experience?"
- "Can you actually build this?"
- "What if you can't hire the team?"
- "Why is your team the right one?"

### Business Model
- "How do you make money?"
- "Why would customers pay for this?"
- "What are your unit economics?"
- "How do you get to profitability?"

### Product & Technology
- "Does this actually work?"
- "What's your technical moat?"
- "How scalable is this?"
- "What if the tech doesn't work?"

### Traction & Risk
- "You don't have enough traction"
- "What if growth stalls?"
- "How do you know customers will stay?"
- "What's your biggest risk?"

## Response Framework

### 1. Acknowledge Directly
Don't deflect. Show you understand the concern.

```
❌ "Actually, there aren't that many competitors"
✅ "Yes, there are 10+ competitors in this space"
```

### 2. Provide Context
Give the information that reframes the concern.

```
"The existing solutions require manual data entry. 
We're the only one that automates the entire workflow."
```

### 3. Show Evidence
Back up your claim with data or traction.

```
"That's why 3 customers switched from Competitor X to us 
in the last 6 months, citing exactly this pain point."
```

### 4. Bridge Forward
Move the conversation to the next point.

```
"The key question is whether we can execute on the 
automation, which brings us to our technical team..."
```

## Data Structure

```json
{
  "objections": [
    {
      "id": "OBJ-456",
      "category": "competition",
      "objection": "What if Google builds this?",
      "severity": "high",
      
      "response": {
        "acknowledge": "Google could theoretically build anything",
        "context": "But they've tried and failed in this specific workflow 3 times",
        "evidence": "Their solutions don't integrate with the tools customers actually use",
        "bridge": "The question is whether we can build a better integrated solution, which we are doing"
      },
      
      "follow_up_questions": [
        "How do you plan to stay ahead if a big company enters?"
      ],
      
      "prepared_talking_points": [
        "Google's previous attempts: Google Wave, Google+, internal tools",
        "Integration moat: 50+ integrations we've built",
        "Customer lock-in: 6-month average setup time"
      ]
    }
  ]
}
```

## Script Usage

```bash
# Generate likely objections
python scripts/prep_objections.py \
  --foundation-id "FOUND-123" \
  --audience investor \
  --stage seed

# Add custom objection
python scripts/add_objection.py \
  --foundation-id "FOUND-123" \
  --objection "What about regulatory risk?" \
  --category risk

# View objection prep
python scripts/view_objections.py --foundation-id "FOUND-123"

# Practice response
python scripts/practice_objection.py --objection-id "OBJ-456"
```

## Output Format

```
OBJECTION PREPARATION
Company: MyCo | Audience: Seed Investors
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HIGH-SEVERITY OBJECTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. "What if Google builds this?" (Competition)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your Response:
"Google could theoretically build anything. They've actually 
tried to solve this problem three times with internal tools 
and each time failed because they don't understand the workflow 
nuances. We're integrated with 50+ tools that customers already 
use, creating a moat that would take them 18+ months to replicate. 

The real question is whether we can build the best solution for 
our target market, which is mid-sized companies that Google 
ignores. That's why 3 companies have switched from Google 
Sheets to us in the last 6 months."

Key Talking Points:
• Google's failed attempts (Wave, internal tools)
• Integration moat (50+ integrations)
• Different target market (mid-market vs. enterprise)
• Customer evidence (3 recent switches)

Follow-up They Might Ask:
"How do you stay ahead if Google targets your segment?"
Your Answer: "We'd partner with Microsoft/Slack who compete 
with Google and would promote us."

---

2. "Your team doesn't have sales experience" (Team)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your Response:
"You're right, neither of us has sold enterprise software before. 
That's exactly why we hired Sarah as our advisor—she was VP Sales 
at Box and helped them scale from $1M to $100M. She's already 
introduced us to 3 prospects.

We're also taking a product-led approach where the product sells 
itself, which is why we have 12 customers with zero sales team. 
Our next hire is a sales leader, and we've budgeted for a VP Sales 
at $200K+ equity."

Key Talking Points:
• Advisor with relevant experience (Sarah/Box)
• Product-led growth working (12 customers, $0 CAC)
• Plan to hire VP Sales
• Budget allocated

---

MEDIUM-SEVERITY OBJECTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3. "Is the market big enough?" (Market)
4. "How do you know customers will pay?" (Business Model)
5. "What if the AI doesn't work well?" (Technology)

[Additional objections prepared...]

PRACTICE NOTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Most likely objections for this audience:
1. Competition (Google threat)
2. Team gaps (sales experience)
3. Market size (TAM questions)

Practice these three until responses are automatic.

⚠️  Remember: Don't get defensive. Acknowledge concerns 
    honestly and move forward with evidence.
```

## Difficult Objection Responses

### "You don't have enough traction"
Response: "You're right, we're early. That's why we're raising now—to get to $30K MRR which would put us in the top 10% of seed companies. The question is whether you believe in the market and our ability to execute."

### "This seems like a feature, not a product"
Response: "That's what we thought 6 months ago. Then we discovered customers are paying $50K+ annually and integrating us into 10+ workflows. We've become system of record, not just a feature."

### "Why you and not the other 10 companies doing this?"
Response: "Most competitors are doing X. We're the only ones doing Y, which is why our customers say Z. The market has room for 2-3 winners and we believe we'll be one based on [evidence]."
