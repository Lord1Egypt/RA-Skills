## Description:

Detects local file content types using the Google Magika deep learning model and magika CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to identify single files, MIME types, batch uploads, or directories by content using local Magika inference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install instructions include a command that downloads a remote script and runs it immediately.

Mitigation: Prefer an isolated package-manager install such as pipx install magika from a trusted source, and review commands before execution.

Risk: Recursive scans may classify more files than intended.

Mitigation: Run recursive Magika scans only on directories selected for classification.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include labels, MIME types, JSON output, JSONL output, and confidence scores from Magika.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
