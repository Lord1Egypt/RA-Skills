## Description:

Notelane helps agents organize local notes as a personal knowledge base with tagging, full-text search, productivity logs, and export workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Notelane to capture, organize, search, review, and export local productivity notes from a Bash command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local note logs and exports are stored in plaintext and may contain sensitive personal or work material.

Mitigation: Avoid storing passwords, tokens, regulated data, or highly sensitive material, and restrict permissions on ~/.local/share/notelane on shared machines.

Risk: CSV exports may carry privacy or spreadsheet-opening risks if note content is copied directly into spreadsheet software.

Mitigation: Review and sanitize exported CSV content before opening it in spreadsheet tools or sharing it outside the local environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and concise CLI output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local plain-text log files and JSON, CSV, or text exports under ~/.local/share/notelane when commands are run.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
