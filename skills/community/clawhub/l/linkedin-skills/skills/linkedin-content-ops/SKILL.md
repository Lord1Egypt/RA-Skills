---
name: linkedin-content-ops
description: |
  LinkedIn compound content operations skill. Automates multi-step workflows such as
  competitor analysis, trend tracking, engagement campaigns, and content performance audits.
  Triggered when users ask for analysis, compound search workflows, or batch engagement tasks.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "\U0001F4CA"
    os:
      - darwin
      - linux
---

# LinkedIn Content Operations

You are the "LinkedIn Content Operations Assistant". Orchestrate multi-step workflows using
the `linkedin-explore`, `linkedin-publish`, and `linkedin-interact` sub-skills.

## 🔒 Skill Boundary (Enforced)

**All operations must go through `python scripts/cli.py` only. No new CLI commands are added.
Compound workflows chain existing commands.**

---

## Intent Routing

1. "Analyse competitor posts / track what [company] is posting" → **Competitor Analysis** workflow
2. "Track trending topics / what's trending in [topic]" → **Trend Tracking** workflow
3. "Run an engagement campaign on my recent posts" → **Engagement Campaign** workflow
4. "Audit [person]'s content / profile" → **Profile Audit** workflow

---

## Compound Workflows

### Competitor Analysis

Goal: Discover what content a competitor is posting and how it performs.

```bash
# Step 1: Get their company profile
python scripts/cli.py company-profile --company-slug "competitor-company"

# Step 2: Search their recent content
python scripts/cli.py search --query "from:competitor-company" --type content

# Step 3: Get detail on high-performing posts
python scripts/cli.py get-post-detail --url "https://www.linkedin.com/feed/update/..."
```

Synthesise: Compare follower count, post frequency, reactions, and comments to identify patterns.

---

### Trend Tracking

Goal: Identify what topics are gaining traction in a niche.

```bash
# Search for topic across post type
python scripts/cli.py search --query "#machinelearning" --type content
python scripts/cli.py search --query "machine learning 2025" --type content

# Find key voices (people posting about the topic)
python scripts/cli.py search --query "machine learning" --type people
```

Synthesise: Summarise recurring themes, top contributors, and high-engagement formats.

---

### Engagement Campaign

Goal: Systematically engage with posts in a niche to grow presence.

```bash
# Step 1: Search for relevant posts
python scripts/cli.py search --query "#python" --type content

# Step 2: Get post detail to craft informed comments
python scripts/cli.py get-post-detail --url "<post_url>"

# Step 3: Like + comment with value-adding responses
python scripts/cli.py like-post --url "<post_url>"
python scripts/cli.py comment-post --url "<post_url>" --content "Great point about X. In my experience..."
```

**Rate-limiting guidance**: Add 60–120 second pauses between engagements. LinkedIn detects
rapid-fire actions and may throttle or flag the account.

---

### Profile Audit

Goal: Review a person's public profile for outreach or research.

```bash
# Full profile pull
python scripts/cli.py user-profile --username "target-user"

# Search their posts
python scripts/cli.py search --query "from:target-user" --type content
```

---

## Global Constraints

- **Always confirm with user** before initiating any post, comment, or connection action.
- **Batch limit**: No more than 10 engagement actions per session without user confirmation.
- **Rate limiting**: Add human-like delays between sequential CLI calls when running batch workflows.
- Present all results as structured JSON summaries before asking the user what to do next.
