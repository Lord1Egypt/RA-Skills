## Description:

Project Code Standard helps agents check, enforce, and repair project coding standards for Python, JavaScript/TypeScript, and general repository conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forestxiecode](https://clawhub.ai/user/forestxiecode)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to assess code style, configure linting or formatting standards, summarize quality findings, and optionally apply approved fixes before review or CI integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest local linting, formatting, or helper-script commands, while referenced helper scripts and assets are not included in the artifact.

Mitigation: Review each suggested command and confirm the required tools or scripts exist in the target project before running them.

Risk: Automatic fixes can modify project files.

Mitigation: Require explicit user approval before applying fixes, then rerun checks and review the resulting file changes.

Risk: The skill content is primarily Chinese-language, which may be less accessible to some reviewers or operators.

Mitigation: Confirm that the installing team is comfortable reviewing and operating Chinese-language skill guidance before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/forestxiecode/skills/project-code-standard)
- [Publisher profile](https://clawhub.ai/user/forestxiecode)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optional fix commands or starter configuration recommendations that require user confirmation before file changes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
