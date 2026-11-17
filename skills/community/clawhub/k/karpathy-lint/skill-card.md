## Description:

Karpathy Lint checks Karpathy LLM knowledge points for duplicates, incomplete entries, tag quality, and overall knowledge base health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sora-mury](https://clawhub.ai/user/sora-mury)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base maintainers use this skill to audit Karpathy LLM knowledge point files, detect duplicate or incomplete entries, and generate a health report with repair suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parser and save helpers may read or overwrite files outside the intended knowledge directory if passed an unsafe filename.

Mitigation: Use the skill only in a controlled workspace, do not pass user-supplied paths or filenames, and add filename validation before enabling repair or write behavior.

Risk: Security evidence marks the release as suspicious pending review.

Mitigation: Review the source before installing and run it with least-privilege file access limited to the target knowledge base.

## Reference(s):

- [Karpathy Lint on ClawHub](https://clawhub.ai/sora-mury/skills/karpathy-lint)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports and terminal output from Python lint helpers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output is primarily Chinese-language diagnostics, statistics, and repair suggestions for knowledge point files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
