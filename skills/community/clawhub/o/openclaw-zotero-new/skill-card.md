## Description:

Saves paper metadata, paper links, abstracts, tags, and optional AI-generated summaries to a user's Zotero library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[little-cat1](https://clawhub.ai/user/little-cat1)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and developers use this skill to add paper records to a Zotero library from agent-supplied title, author, URL, abstract, tag, and summary data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Zotero credentials could be over-scoped or exposed through logs, shell history, or shared terminal environments.

Mitigation: Use a least-privilege Zotero API key and keep ZOTERO_CREDENTIALS out of logs, shared shells, and committed configuration.

Risk: Shell and PowerShell installer entries introduce installation-time trust in the uv installer source.

Mitigation: Prefer a reviewed package-manager install path where available, or verify the installer source before running it.

Risk: Loose arXiv URL detection may fetch and upload unexpected content to the user's Zotero library.

Mitigation: Run the script only with trusted paper URLs and review created Zotero items and attachments after execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/little-cat1/skills/openclaw-zotero-new)
- [Zotero](https://www.zotero.org)
- [uv installer for Linux](https://astral.sh/uv/install.sh)
- [uv installer for Windows](https://astral.sh/uv/install.ps1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain text execution output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv, Python 3.10 or newer, pyzotero, and a ZOTERO_CREDENTIALS value in userid:apiKey format.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
