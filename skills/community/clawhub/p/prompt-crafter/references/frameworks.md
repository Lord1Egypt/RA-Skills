# Prompt Frameworks — Extended Examples

## RACE Examples

### Email copywriting
```
Role: Email copywriter for a bootstrapped SaaS (not VC-funded, no marketing team)
Action: Write a launch announcement email for a new feature — automatic invoice reminders
Context: 2,400 subscribers, mostly freelancers and small agencies. Open rate is 34%. 
They've been asking for this feature for months. Subject line + body. Max 150 words.
Example tone: "We built the thing you kept asking for. Here's how it works."
```

### Technical documentation
```
Role: Senior developer who writes docs that junior devs actually read
Action: Write setup instructions for a Python CLI tool that connects to a Postgres database
Context: Users are developers but may not know Postgres. Assume Mac or Linux. 
Must include: prerequisites, install command, config file example, first run test.
Example format:
## Prerequisites
- Python 3.9+
- A running Postgres instance (local or remote)
```

### Job description
```
Role: Startup founder who's hired 20+ people and hates corporate job postings
Action: Write a job post for a full-stack developer (React + Python)
Context: 8-person remote team, $120-150K range, must mention equity. 
No "rock star" or "ninja." Be specific about what they'll build in the first 90 days.
Example: "You'll own the billing system rewrite. Not 'contribute to' — own it."
```

## Chain-of-Thought Examples

### Pricing analysis
```
I'm pricing a digital course about prompt engineering at $49. 
Think through this systematically:
1. Who exactly would pay $49 for this vs finding free resources?
2. What do the top 5 competing courses charge? (Estimate based on the market)
3. What must the course include to justify $49?
4. What's the refund risk at this price point?
5. Would $29 or $79 convert better? For each, explain why.
6. Final recommendation with specific reasoning.
```

### Architecture decision
```
We need to choose between SQLite and Postgres for a new SaaS product.
Expected: <1000 users in year 1, growing to maybe 10K.
Walk through this decision:
1. What are the actual performance differences at our expected scale?
2. What features does Postgres have that we'd miss with SQLite?
3. What's the operational cost difference (hosting, backups, maintenance)?
4. At what specific scale does SQLite become a problem?
5. What's the migration cost if we start with SQLite and move later?
6. Recommendation: which one, and what trigger point should make us switch?
```

## Constraint-Stacking Examples

### LinkedIn post
```
Write a LinkedIn post about why most AI tools fail in enterprise.

CONSTRAINTS:
- 150-200 words (the sweet spot for LinkedIn engagement)
- Open with a surprising statistic or contrarian claim
- Include exactly one specific example (company name or scenario)
- End with a question that CTOs would want to answer
- No emojis except a single one at the very end
- Do NOT use: "leverage", "synergy", "game-changer", "at the end of the day"
- Write as a practitioner, not a thought leader
```

### API error message
```
Write an error message for when a user's payment fails.

CONSTRAINTS:
- Max 2 sentences
- Must tell the user what happened AND what to do next
- No technical jargon (no "transaction declined", "gateway timeout")
- Tone: helpful, not apologetic (no "We're sorry")
- Must not reveal internal system details
- Example format: "[What happened]. [What to do]."
```

## Few-Shot Examples

### Data extraction
```
Extract structured data from these product reviews. Follow this exact format:

Review: "Bought these headphones for my commute. Sound is great but they 
hurt my ears after about 45 minutes. Battery lasted 3 days on a single charge."
→ {"sentiment": "mixed", "pros": ["sound quality", "battery life"], 
   "cons": ["comfort"], "use_case": "commuting", "duration_mentioned": "45min"}

Review: "Absolute garbage. Stopped working after 2 weeks. Don't waste your money."
→ {"sentiment": "negative", "pros": [], "cons": ["durability"], 
   "use_case": "unknown", "duration_mentioned": "2 weeks"}

Now extract from this review:
Review: "Perfect for the gym. They stay in place during heavy workouts and 
the bass is incredible. A bit pricey at $200 but worth it."
```

### Tone matching for brand voice
```
Rewrite formal sentences in a casual SaaS brand voice. Examples:

Formal: "We are pleased to announce the availability of our new dashboard feature."
Casual: "New dashboard just dropped. It's the one you've been bugging us about."

Formal: "Please ensure that all required fields are completed prior to submission."
Casual: "Fill in the highlighted fields and hit submit. That's it."

Formal: "Our team is currently investigating the reported service disruption."
Casual: "Something broke. We're on it. Updates in #status."

Now rewrite:
Formal: "We regret to inform you that your subscription will be discontinued 
effective at the end of your current billing period."
```
