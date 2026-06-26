---
name: prospect-analyzer
description: "Analyze any company's website to find content marketing gaps and qualify them as a potential client. Visits their site, audits their blog, checks competitors, scores the opportunity, and generates a personalized outreach angle. Use when you need to 'analyze a prospect', 'qualify a lead', 'audit their content', 'check their blog', 'find content gaps for [domain]', 'research a company for outreach', or 'score this lead'."
version: 1.0.0
metadata:
  openclaw:
    emoji: "🔍"
    homepage: "https://driftmango.com/sdr-kit"
---

# Prospect Analyzer

Analyze a company's website to determine if they need content marketing help. Produces a scored qualification report with specific content gaps, competitive positioning, and a personalized outreach angle you can use immediately.

**Part of the DriftMango SDR Kit** — an autonomous prospecting pipeline for service businesses. This is the free standalone skill. The full pipeline (automated scanning, outreach email composer, content writer, editor) is available at driftmango.com/sdr-kit.

## When to Use

- Given a company domain: "analyze example.com" or "qualify acme.io as a prospect"
- Processing prospects from a queue file (see Queue Integration below)
- Evaluating whether a company is worth reaching out to before writing a cold email

## What You Need

- Browser tool enabled in OpenClaw (for visiting websites)
- A clear idea of what service you sell (so the outreach angle is relevant)

If you sell content marketing, SEO, web design, paid ads, or any service where you can spot weaknesses on a company's website, this skill works for you.

## Configuration

Create a file called `PROSPECT_CONFIG.md` in your workspace root with your business context:

```markdown
# My Business

## What I Sell
[Describe your service in 1-2 sentences]

## Target Clients
[Who is your ideal customer? Industry, size, stage]

## Avoid
[Any industries or company types you don't work with]

## Price Range
[Your typical engagement price, so outreach angles are realistic]
```

If no PROSPECT_CONFIG.md exists, the skill still works — it just produces a generic content gap analysis without a tailored outreach angle.

## Analysis Process

### Step 1: Initial Reconnaissance

Visit the prospect's homepage using the browser. Note:
- What does the company do? (SaaS, e-commerce, services, etc.)
- What is their product/service?
- Who is their target audience?
- What stage are they at? (startup, growth, enterprise — look for signals like team size on About page, funding announcements, pricing page sophistication)

### Step 2: Blog and Content Audit

Navigate to common blog locations in this order until you find one:
- /blog
- /resources
- /articles
- /news
- /insights
- /learn
- /content

If NO blog exists, that is a strong qualification signal — note "No blog found" and skip to Step 4.

If a blog exists, analyze:

**Publishing frequency:**
- Look at the dates of the 10 most recent posts
- Calculate average posting frequency
- Note the date of the most recent post
- If last post is >60 days old, flag as "dormant blog"

**Content quality (sample the 3 most recent posts):**
For each post, visit it and evaluate:
- Estimated word count (look at content length)
- Does the title contain a target keyword? (search-intent phrasing like "how to...", "best...", "guide to...", "[year] ...")
- Heading structure: does it use H2/H3 subheadings logically?
- Does it have internal links to other content or product pages?
- Does it have a clear call-to-action?
- Overall quality impression: thin / generic / decent / strong

### Step 3: Competitive Quick-Check

From the homepage, identify what space/niche the company is in. Then:
- Use the browser to Google: "[their main keyword] blog" or "[their product category] guide"
- Check if any of their content appears on the first page
- Note 1-2 competitors who DO appear and are clearly investing in content

### Step 4: Scoring and Qualification

Score the prospect on a 1-10 scale based on these weighted factors:

| Factor | Weight | Scoring |
|--------|--------|---------|
| Blog exists but is weak/dormant | 3x | No blog=10, dormant=8, irregular=6, active but thin=4, strong=1 |
| Company is a fit for your services | 2x | Perfect fit=10, adjacent=6, outside target=2 |
| Evidence they can pay | 2x | Funded/revenue signals=10, unclear=5, likely tiny=3 |
| Competitor content is strong | 2x | Competitors crushing it while they're not=10, similar level=3 |
| Contact person findable | 1x | Founder/CMO name visible=10, team page exists=6, no info=2 |

Total = weighted sum / 100, normalized to 1-10 scale.

**Qualification thresholds:**
- 8-10: HOT LEAD — prioritize outreach
- 6-7: Warm lead — worth pursuing
- 4-5: Cool lead — low priority
- 1-3: Skip — not a fit

### Step 5: Generate Outreach Angle

Based on the analysis, write a specific outreach angle. This is NOT a full email — it's the core insight that makes an email personalized. Format:

```
OUTREACH ANGLE:
Hook: [One sentence describing their specific content problem]
Evidence: [The concrete data point you found]
Value prop: [What you would specifically do for them]
```

If PROSPECT_CONFIG.md exists, tailor the value prop to your actual services and pricing.

### Step 6: Output

Save the report to your workspace:

```
prospects/[company-name]-analysis.md
```

Create the prospects directory if it doesn't exist:
```bash
mkdir -p prospects
```

Use this format:

```markdown
## Prospect Report: [Company Name]
**Domain:** [domain]
**Analyzed:** [date]
**Score:** [X/10] — [Hot/Warm/Cool/Skip]

### Company Overview
- **What they do:** [1-2 sentences]
- **Stage:** [startup/growth/enterprise]
- **Can they pay:** [yes/likely/unclear]

### Content Audit
- **Blog URL:** [url or "none found"]
- **Total posts found:** [N]
- **Last published:** [date or "N/A"]
- **Publishing frequency:** [X posts/month or "dormant" or "none"]
- **Average quality:** [thin/generic/decent/strong]
- **Key weaknesses:**
  - [specific weakness 1]
  - [specific weakness 2]
  - [specific weakness 3]

### Competitive Position
- **Key competitor:** [name + domain]
- **Competitor content strength:** [description]
- **Gap:** [what the competitor does that this prospect doesn't]

### Outreach Angle
- **Hook:** [one sentence]
- **Evidence:** [concrete data]
- **Value prop:** [specific offer]

### Raw Notes
[Any additional observations worth remembering]
```

After generating the report, tell the user the score and a 2-sentence summary.

## Queue Integration (Optional)

If you maintain a prospect queue at `prospects/queue.md`, this skill can process it:

1. Read the top entry from "Pending Analysis"
2. Move it to "In Progress"
3. Run the full analysis
4. Save the report to `prospects/[company-name]-analysis.md`
5. Move the entry to "Analyzed" with the score
6. If score is 8+: notify immediately (hot lead)
7. If score is 6-7: note for batch notification

Queue format:
```markdown
# Prospect Queue

## Pending Analysis
- **[Company Name]** — [domain.com]
  - Source: [where you found them]
  - Found: [date]

## Analyzed
- **[Company Name]** — [domain.com] — Score: X/10 — [Hot/Warm/Cool/Skip]
```

## Tips for Best Results

- **Run on a capable model.** Claude Haiku 4.5 is the minimum for decent analysis. Sonnet produces noticeably better outreach angles.
- **Be specific in PROSPECT_CONFIG.md.** The more the skill knows about what you sell, the better the outreach angle.
- **Batch your analyses.** Run 3-5 per day to build a pipeline without burning through tokens.
- **Trust the scores.** If a prospect scores below 6, don't waste time on outreach. Move on.

## What's Next

This skill tells you WHO to reach out to and WHY. To complete the pipeline:

- **market-scanner** finds prospects automatically from Product Hunt, Google, and IndieHackers
- **outreach-composer** turns this analysis into a ready-to-send 3-email cold sequence
- **content-writer + editor** produce the content you'll deliver when they say yes

Full pipeline available at **driftmango.com/sdr-kit** →

## Important Rules

- NEVER fabricate data. If you can't find a blog, say so. If you can't determine posting frequency, say "unclear."
- NEVER guess at traffic numbers — just note what you observe.
- If the browser can't load a page, try curl as a fallback.
- Keep the analysis factual. The outreach angle should feel like it came from a human who spent 10 minutes researching the company.
- If a prospect is clearly outside the user's target, score them low and explain why.
