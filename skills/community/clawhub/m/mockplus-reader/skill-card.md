## Description:

Reads and analyzes MockPlus online design pages, including page structure, design information, component trees, interaction notes, and comments from MockPlus links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a-din](https://clawhub.ai/user/a-din)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product or design teams use this skill to inspect MockPlus prototype links and turn design-page details into structured project, page, component, interaction, and note summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes local project run commands that can install and execute npm tooling outside the stated MockPlus reader purpose.

Mitigation: Review the target project and package files before running commands; use a disposable environment for npm install or dev-server execution.

Risk: Restricted MockPlus pages may require login or project permissions, limiting retrieved design details.

Mitigation: Use authorized MockPlus accounts and record access limitations in the generated analysis.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/a-din/skills/mockplus-reader)
- [MockPlus](https://www.mockplus.com/)
- [MockPlus RP](https://rp.mockplus.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary with bullet lists and optional shell-command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require authenticated access to restricted MockPlus pages.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
