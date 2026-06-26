# PRISM Evidence Rules

**Mandatory for all PRISM reviewers. Copy this block into every reviewer prompt.**

```
EVIDENCE RULES (mandatory for all PRISM reviewers):
1. Before analyzing, read at least 3 specific files relevant to your focus.
2. Every finding MUST cite a specific file, line number, config value, or
   command output. Quote directly from what you read.
3. Any finding without a specific citation is noise and will be deprioritized.
4. Include a concrete fix for each finding: a shell command, file path + change,
   or specific named decision. "Consider improving" is not acceptable.
```

## Why These Rules Exist

- **Citations prevent hallucination.** Reviewers without citation requirements produce vague findings that can't be verified or actioned.
- **Concrete fixes prevent analysis paralysis.** "Consider improving X" is not a finding — it's a suggestion that will sit unresolved.
- **File reads before analysis prevent anchoring.** Reviewers who analyze from memory rather than fresh reads reproduce prior assumptions.

## Enforcement

The orchestrator is responsible for including this block verbatim in every reviewer prompt. Do not summarize or abbreviate. The repetition is intentional — each reviewer sees it fresh.
