## Description:

Lossless Claw distills conversations or session logs into local memory by extracting identity details, preferences, tasks, and durable knowledge while preserving traceable short-term logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingmoon96-dev](https://clawhub.ai/user/lingmoon96-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert conversation or session records into structured local memory, including preferences, tasks, durable knowledge, and traceable summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages permanent retention of conversation logs and personal details without documented privacy controls.

Mitigation: Use it only with inputs approved for retention, and require a clear storage location, review step, redaction process, and deletion path before applying long-term memory changes.

Risk: Sensitive personal, credential, or business data from session logs could be promoted into long-term memory.

Mitigation: Review and redact proposed memory updates before applying them, especially when using commands that persist distilled content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lingmoon96-dev/skills/lossless-claw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces traceable summaries and memory-update guidance; long-term retention should be reviewed before applying changes.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
