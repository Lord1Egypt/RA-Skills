# Recommendation Engine — Full Procedure

## Overview

The recommendation engine takes the Workflow Profile from Phase 1 and produces a ranked list of skill suggestions. It works by matching gaps to catalogue entries, scoring candidates, and filtering for quality.

## Step 1: Load the Skills Catalogue

Read `data/skills-catalogue.json`. This contains a curated index of quality ClawHub skills organized by category. Each entry includes: name, slug, description, author, downloads, stars, permissions, tags, trust score, and install command.

## Step 2: Identify Gaps

From the Workflow Profile, extract two types of gaps:

### Priority 1: Explicit Gaps (Integration Mismatches)
The user actively uses a tool/service but has no corresponding skill. Examples:
- Mentions "Notion" but has no Notion skill
- Uses GitHub daily but has no GitHub skill
- Sends emails but has no email skill

These are the strongest recommendations because the user is already doing the work manually.

### Priority 2: Category Gaps
The user works in a domain but has no skills covering common needs in that domain. Examples:
- Codes daily but has no testing or linting skill
- Writes content but has no SEO skill
- Does devops but has no monitoring skill

### Priority 3: Enhancement Opportunities
The user has basic coverage but could benefit from specialized tools. Examples:
- Has a generic GitHub skill but could use a PR review skill
- Has web search but could use a domain-specific research tool
- Has basic automation but could use a workflow orchestration skill

## Step 3: Match Gaps to Catalogue

For each gap:
1. Identify the relevant category in the catalogue
2. Pull all skills from that category
3. Filter out skills already installed in ANY location (user skills at `~/.openclaw/skills/`, system skills at `/opt/homebrew/lib/node_modules/openclaw/skills/` or equivalent, workspace skills). Match by name, case-insensitive.
4. Filter out skills whose functionality is already covered by existing config (e.g. memoryFlush covers session wrap-up, gog system skill covers Gmail, HEARTBEAT.md automations cover scheduled tasks). Don't recommend what already works.
5. Score remaining candidates (see scoring.md)

## Step 4: Deduplicate and Prioritize

### Overlap Detection
Don't recommend multiple skills that do the same thing. If three email skills match:
- Pick the highest-scored one
- Mention alternatives briefly: "Also consider: [skill-b], [skill-c]"

### Prioritization Order
1. Explicit gaps with high-confidence domains (user definitely needs this)
2. Category gaps in high-confidence domains
3. Explicit gaps in medium-confidence domains
4. Enhancement opportunities
5. Speculative recommendations (low confidence domains)

## Step 5: Limit to Top 5

Only present 5 recommendations maximum. Rationale:
- More than 5 overwhelms the user
- Forces the engine to pick only the best matches
- User can run /kungfu-gaps to see ALL gaps without recommendations

If fewer than 5 quality matches exist, show fewer. Never pad with weak recommendations.

## Step 6: Generate Recommendation Output

For each recommendation, include:
- **Skill name and trust score** (stars out of 5)
- **Category** it belongs to
- **Why**: 1-2 sentences explaining why THIS user needs it, referencing specific findings from their Workflow Profile
- **Author and stats**: downloads, stars
- **Install command**: ready to copy-paste

The "Why" is the most important field. Generic reasons like "this is a popular skill" are useless. Tie it to the user's actual workflow: "You mention Slack in 4 of your last 7 daily logs but have no Slack integration skill."

## Step 7: Handle No-Match Scenarios

If a gap has no matching skill in the catalogue:
- Say "No trusted skill found for [category] yet"
- Don't recommend a vaguely related skill just to fill the slot

If the user's workflow is very niche:
- Acknowledge it: "Your workflow is specialized. The catalogue may not cover [niche] well yet."
- Suggest contributing: "Know a good skill for this? Open an issue on GitHub."

## Step 8: Confidence Labels

Tag each recommendation with a confidence level:
- **High**: Direct match to an explicit gap in a high-confidence domain
- **Medium**: Category match or medium-confidence domain
- **Speculative**: Low-confidence domain or enhancement opportunity

Show confidence in the output so users can prioritize what to install first.
