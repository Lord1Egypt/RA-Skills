# Standard Section Headings Checklist

Every skill in the library should have these standard headings. During every 10khr pass, check for and fix non-standard equivalents.

## Required Headings

| Required Heading | Common Non-Standard Equivalent | Fix |
|---|---|---|
| `## When to Use` | `## When to use` (lowercase), `## Trigger conditions`, `## Use when` | Rename heading, extract content from existing section |
| `## When NOT to Use` | `## When not to use` (lowercase), "Do not use" embedded in Responsibility boundary | Add dedicated heading, extract content from existing section |

**Cron-only exception:** Skills that run exclusively as cron jobs (no interactive invocation, no `triggers:` field) do not require `## When to Use` or `## When NOT to Use`. The Schedule section is sufficient. Forcing these headings onto cron-only skills adds noise for zero benefit.
| `## Gotchas` | `## ⚠️ Critical Pitfalls`, `## Known issues`, `## Common mistakes` | Rename to `## Gotchas` |
| `## Support file map` | `## References`, `## Reference files` | Rename to `## Support file map` |

## Trigger Phrases That Need Fixing

When you see these in a SKILL.md, convert them:
- "Use X when:" → `## When to Use`
- "Do not use X when:" → `## When NOT to Use`
- "Trigger conditions" → `## When to Use` (move the "when" bullets) + `## When NOT to Use` (move the "do not" bullets)
- "Trigger:" in frontmatter description is fine; this is about body headings

## Impact

Standard headings improve D10 by 1-2 points per skill and make the library consistent for agent activation.