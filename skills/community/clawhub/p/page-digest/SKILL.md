---
name: page-digest
description: "Fetch a web page and produce a structured markdown digest: title, key points, entities, action items, and a one-paragraph TL;DR. Use when the user shares a URL and asks for a quick summary, briefing, or extraction of actionable information."
metadata:
  openclaw:
    emoji: "📄"
---

# Page Digest

Turn any URL into a concise, structured markdown digest.

## When to use

- User shares a link and wants "the gist" or "summary"
- Need to extract action items, key facts, or entities from an article
- Quick briefing before a meeting based on a web page

## Prerequisites

- `web_fetch` tool available in the agent runtime
- Target URL must be publicly accessible (no auth-gated pages)

## Steps

1. **Receive URL** — Accept the target URL from the user or upstream process.
2. **Fetch content** — Call `web_fetch` with `extractMode: "markdown"` and `maxChars: 20000`.
3. **Analyze** — Read the fetched markdown and identify:
   - Title (first H1 or page title)
   - TL;DR (≤ 3 sentences)
   - Key points (3-7 bullet points)
   - Entities mentioned (people, orgs, products — max 5)
   - Action items (if any — explicit next steps or recommendations)
4. **Format output** — Produce a markdown digest with the sections above, in that order.
5. **Return** — Deliver the digest to the caller.

## Output format

```markdown
## {Title}

**TL;DR:** {3-sentence summary}

### Key Points
- {point 1}
- {point 2}
- ...

### Entities
- {entity} — {brief role/context}

### Action Items
- {action item 1}
- {action item 2}
```

## Example

**Input:** `https://example.com/article-about-ai-regulation`

**Output:**
```markdown
## AI Regulation Bill Passes Senate

**TL;DR:** The U.S. Senate passed a sweeping AI regulation bill Thursday. The legislation requires companies to audit high-risk AI systems before deployment. The bill now moves to the House for consideration.

### Key Points
- Bipartisan vote of 68-32
- Covers high-risk AI in healthcare, finance, and critical infrastructure
- Penalties for non-compliance up to $10M or 2x profits
- Enforcement begins 18 months after signing

### Entities
- U.S. Senate — Legislative body that voted
- Senate Majority Leader — Sponsored the bill
- FDA — Will enforce medical AI provisions

### Action Items
- Review compliance timeline for affected systems
- Schedule legal review of audit requirements
```

## Error handling

- If URL is unreachable: report the error with the URL, suggest alternatives
- If content is too short (< 200 chars): note it and produce what's available
- If content is too long (> 20000 chars): truncate and warn that the digest may be incomplete
