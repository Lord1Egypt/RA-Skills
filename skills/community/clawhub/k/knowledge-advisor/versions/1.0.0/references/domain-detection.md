# Domain Detection Guide

How to auto-detect domain tags for ingested materials.

## Process

1. Read the source material
2. Identify the primary subject area(s)
3. Suggest 2-4 domain tags
4. Present to user for confirmation

## Common Domain Tags

| Domain Tag | Typical Content | Example Books |
|-----------|----------------|---------------|
| `leadership` | Leading teams, organizational behavior, executive skills | Good to Great, Leaders Eat Last |
| `management` | Day-to-day people management, delegation, 1:1s | The Manager's Path, High Output Management |
| `communication` | Difficult conversations, persuasion, public speaking | Crucial Conversations, Never Split the Difference |
| `strategy` | Business strategy, competitive advantage, planning | Good Strategy Bad Strategy, Blue Ocean Strategy |
| `entrepreneurship` | Startups, product-market fit, fundraising | The Lean Startup, Zero to One |
| `psychology` | Behavioral science, cognitive biases, decision-making | Thinking Fast and Slow, Influence |
| `personal-development` | Habits, productivity, self-improvement | Atomic Habits, Deep Work |
| `product` | Product management, user research, design | Inspired, The Mom Test |
| `engineering` | Software engineering practices, architecture | Clean Code, Designing Data-Intensive Applications |
| `finance` | Personal finance, investing, economics | The Intelligent Investor, Rich Dad Poor Dad |
| `hr` | Hiring, performance reviews, people operations | Who, Work Rules! |
| `sales` | Sales methodology, negotiation, closing | SPIN Selling, The Challenger Sale |

## Detection Signals

Look for these signals in the material to determine domain:

- **Chapter titles** often directly indicate domain
- **Author background** (stated in intro/bio) suggests domain
- **Case studies** from specific industries narrow the domain
- **Terminology** — "sprint", "standup" → engineering; "P&L", "revenue" → finance
- **Target audience** — "for managers", "for entrepreneurs" usually stated explicitly

## Rules

1. Suggest 2-4 tags, not 1 (most books span multiple domains)
2. Put the most specific tag first
3. Always ask user to confirm — never auto-commit tags
4. Accept custom tags from the user (not limited to the common list)
5. Store tags in lowercase, hyphenated format
6. Tags are stored in `meta.json` and used for filtering in `_index.md`
