## Description:

Show journal impact factor and quartile trends over 5 years.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to generate bounded journal impact factor and quartile trend summaries for supported journals. It is best suited for demonstrations or scoped evidence-insight workflows where built-in mock data is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses limited built-in mock journal data, so reported impact factors may be mistaken for authoritative Journal Citation Reports data.

Mitigation: Use results only for bounded demonstrations or scoped evidence workflows, and verify any real impact-factor claims against authoritative sources before relying on them.

Risk: The batch mode reads journal names from a local file path supplied to the script.

Mitigation: Use trusted workspace files, keep input paths scoped to the workspace, and review input contents before execution.

Risk: Audit evidence preserved one stress-case boundary weakness around staying within declared scope.

Mitigation: Keep requests within the documented journal-trend workflow and use the fallback path when required inputs or authoritative evidence are missing.

## Reference(s):

- [Audit Reference](references/audit-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/journal-impact-factor-trend)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain-text reports with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 5-year impact factor trend summaries, quartile status, trend labels, assumptions, limits, and next checks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
