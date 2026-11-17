## Description:

Provides bilingual anti-hallucination guardrails for summary tasks so agents report empty or sparse source logs honestly instead of fabricating dated activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mowenqwq](https://clawhub.ai/user/mowenqwq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to harden automated or scheduled summary workflows against blank-day hallucinations, profile contamination, and unsupported dated claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Empty or sparse logs can lead an agent to fill required summary sections with plausible but unsupported activity.

Mitigation: Require every dated claim to trace to current-session dialogue or tool results, and emit "no records" when the source data is empty.

Risk: User profiles, long-term memory, or knowledge archives can contaminate a summary by being treated as evidence of what happened on a specific day.

Mitigation: Treat profile and memory material as context only, not as evidence for dated facts in a summary.

Risk: Persisting unsupported summary content can turn fabricated entries into future false evidence.

Mitigation: Gate archival writes on per-item source checks and avoid persisting summary content that lacks current-session provenance.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mowenqwq/skills/grounded-summaries)

## Skill Output:

**Output Type(s):** [markdown, guidance]

**Output Format:** [Markdown prose with bilingual rules, checklists, and examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no tools, API calls, credential variables, or MCP references detected.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
