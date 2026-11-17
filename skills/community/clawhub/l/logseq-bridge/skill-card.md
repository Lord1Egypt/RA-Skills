## Description:

Pure file-based interaction with a local Logseq graph. Read, write, search, and manage Logseq journals and pages via direct `.md` file operations. No plugins or HTTP APIs needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ham-5on](https://clawhub.ai/user/ham-5on)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, external agents, and CLI users use this skill to read, write, search, and manage local Logseq journals and pages through direct Markdown file operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write examples can modify local Logseq Markdown files.

Mitigation: Verify the graph path before running write commands, and keep backups or version control for important notes.

Risk: Optional transit-index search can inspect Logseq index files under ~/.logseq.

Mitigation: Use transit-index search only when broader local index inspection is acceptable; otherwise search within the selected graph folder.

## Reference(s):

- [Logseq](https://logseq.com)
- [Logseq Markdown Guide](https://docs.logseq.com)
- [ClawHub Skill Page](https://clawhub.ai/ham-5on/skills/logseq-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Logseq-compatible Markdown examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires filesystem access to the user's local Logseq graph directory.]

## Skill Version(s):

2.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
