## Description:

This ClawHub Plug bundles four operations skills for Linear, AWS-related workflows, article-writing support, and ping monitoring into a coordinated operations toolkit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Operations users and developers use this bundle to combine read, command execution, and file-writing workflows across the included skills, then consolidate their outputs into a single operational result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundle combines command execution, file writing, API credentials, and AWS-related automation without tight task boundaries or approval controls.

Mitigation: Review the bundle before production or cloud-connected use, apply least-privilege credentials, keep secrets in environment variables, and require explicit human approval before commands, writes, AWS changes, or bulk processing.

Risk: The security verdict is suspicious for normal installation because the bundle can affect local files and external services.

Mitigation: Start with read-only or dry-run workflows, inspect generated commands and file changes before execution, and deploy only in a controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/plug-bundle-linear-toolkit-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and text with inline code, shell command examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file-oriented workflow guidance and command/API examples depending on the selected member skills.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
