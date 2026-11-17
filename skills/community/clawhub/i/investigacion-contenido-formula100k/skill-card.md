## Description:

Researches viral content trends and converts verified public web, Apify, and optional vidIQ findings into content ideas using the FORMULA 100K methodology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and content strategists use this skill to research trends, competitor content, audience questions, and YouTube outliers, then turn verified findings into 3 to 5 content ideas with hooks and viral triggers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conflicting logged-in browser instructions could lead an agent to inspect private social account areas.

Mitigation: Use OpenClaw public-data mode for ordinary research and do not inspect DMs, saved messages, private messages, or other private account areas unless the operator explicitly wants authenticated account analysis.

Risk: Reports or social-platform sessions may be stored or reused without clear operator awareness.

Mitigation: Confirm where reports are stored and whether any session files are created or reused before running the workflow.

Risk: Social metrics and URLs can be misleading when a scrape or connected tool did not actually run.

Mitigation: Require live evidence from the configured research tools for metrics and URLs, and mark missing scrape results as unverified instead of filling gaps from memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/investigacion-contenido-formula100k)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with tables, links, verification notes, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Metrics and social URLs must be backed by live tool evidence or clearly marked unverified.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
