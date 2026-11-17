## Description:

Merges invoice PDFs and images into printable PDF sheets with consistent crop lines, safe margins, dated output folders, and automatic skipping of previously generated merged files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cdk1025](https://clawhub.ai/user/cdk1025)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill in OpenClaw or from the command line to batch-layout invoice PDFs and JPG/JPEG/PNG images into printable PDF output. It is intended for directories the user explicitly selects and produces merged invoice or bill PDFs in a dated output folder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation uses mutable remote package resolution for pypdf and Pillow.

Mitigation: Install only a reviewed or pinned release, preferably inside a virtual environment or sandbox.

Risk: The skill reads files from a user-provided directory and writes generated PDFs into that directory tree.

Mitigation: Run it only on directories the user explicitly chooses and review outputs before sharing or uploading them.

Risk: Generated PDFs are automatically opened with the system default application.

Mitigation: Use in an environment where opening local PDFs is acceptable, or review/disable auto-open behavior before deployment in sensitive accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cdk1025/skills/invoice-merger)
- [CLAWHUB.md](artifact/CLAWHUB.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [PDF files plus Markdown and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a dated output directory, writes merged PDF files, prints progress messages, and may open generated PDFs with the system default application.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
