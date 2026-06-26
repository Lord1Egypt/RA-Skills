---
name: Gmail Search Emails
description: Atomic node skill to search for emails in Gmail using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the search fails.

# Gmail Search Emails

This skill allows the agent to search for emails in Gmail using specific queries with the native CLI.

## Cognitive Directives
WHEN [Requested to search for an email or find specific communications]
THEN [Invoke the `gog` tool with the argument `gmail search "query" --json`]

## Schema Example
```json
{
  "args": "gmail search \"from:example@gmail.com subject:invoice\" --json"
}
```

## Expected Output
A JSON array containing email headers (id, threadId, snippet) or a "no results found" message.
