# Query Patterns

Use this file for common answer shapes and decisions about when to file results back into the wiki.

## Answer structure

A good default answer shape is:

```markdown
## Answer
Short answer first.

## Why
- point supported by [[Page A]]
- point supported by [[Page B]]

## Uncertainty
- ambiguity or missing evidence

## Related pages
- [[Analysis X]]
- [[Topic Y]]
```
```

## Analysis page template

Use this when a query result should become a durable page.

```markdown
# Analysis: <short title>

## Question
What was being asked.

## Short answer
2-4 sentence synthesis.

## Key findings
- finding one
- finding two

## Evidence and reasoning
Longer synthesis grounded in relevant wiki pages.

## Uncertainty
Open questions, weak evidence, or conflicting claims.

## Related
- [[Topic A]]
- [[Entity B]]

## Sources
- [[Source: Example]]
- [[Source: Example 2]]
```
```

## Filing heuristic

File the result back into the wiki when:
- it combines information from multiple pages
- it creates a reusable comparison or recommendation
- it resolves or clarifies a recurring question
- it would be annoying or expensive to reconstruct later

Do not file it when:
- the answer is obvious from one page
- the answer is ephemeral or conversational only
- the result adds clutter without improving retrieval

## Log entry pattern

```markdown
## [YYYY-MM-DD] query | <question>
- Read: [[Topic A]], [[Analysis B]]
- Created: [[Analysis: <short title>]]
```
```

## Citation habit

Prefer citing wiki pages first. Add source-page citations when the user needs tighter traceability or when the claim is likely to be questioned.
