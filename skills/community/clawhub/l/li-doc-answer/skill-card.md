## Description:

Processes Word and Markdown documents locally, detects common question formats, and generates formatted reference-answer documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and office users use this skill to batch process local Word documents, add answer sections, convert Markdown to DOCX, and create template-style reference answers for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated answers may be incomplete or inaccurate because the artifact produces template-style reference answers rather than authoritative solutions.

Mitigation: Review generated answers against textbooks, instructor guidance, or other authoritative materials before use.

Risk: Batch processing and default output filenames can create or overwrite derived local documents.

Mitigation: Run scripts in a working copy, inspect output paths before batch runs, and keep backups of source documents.

Risk: Unpinned dependencies or system tools may behave differently across environments.

Mitigation: Install dependencies in a virtual environment, prefer pinned package versions, and verify legacy .doc handling where antiword is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/43622283/skills/li-doc-answer)
- [SKILL.md](artifact/SKILL.md)
- [README_EN.md](artifact/README_EN.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands; generated artifacts are DOCX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs on local document inputs and writes derived DOCX files; generated answers are templates for human review.]

## Skill Version(s):

3.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
