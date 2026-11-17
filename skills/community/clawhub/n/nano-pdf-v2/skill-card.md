## Description:

Edit PDFs with natural-language instructions using the nano-pdf CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[15914355527](https://clawhub.ai/user/15914355527)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document editors use this skill to ask an agent to apply page-specific PDF edits through the nano-pdf command-line tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned third-party nano-pdf package.

Mitigation: Install a pinned, reviewed package version in a sandboxed environment before using it on sensitive documents.

Risk: PDF edits may target the wrong page when page numbering differs by tool version or configuration.

Mitigation: Verify the output PDF after each edit and retry with the alternate page index convention when results are off by one.

Risk: Generated PDFs may contain incorrect or unintended edits.

Mitigation: Review generated PDFs before sending or publishing them.

## Reference(s):

- [nano-pdf package](https://pypi.org/project/nano-pdf/)
- [Nano PDF V2 ClawHub listing](https://clawhub.ai/15914355527/skills/nano-pdf-v2)

## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the nano-pdf CLI and manual review of generated PDFs before sharing.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
