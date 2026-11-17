## Description:

OOMOL RAG (knowledge-base.oomol.com). Use this skill for ANY OOMOL RAG request — reading, creating, updating, and deleting data. Whenever a task involves OOMOL RAG, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other OOMOL RAG users can retrieve knowledge-base content, add and manage files, and check ingestion or deletion status through the OOMOL-connected oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI setup path runs downloaded code that has not been verified, and installation may add or synchronize agent skills.

Mitigation: Review and approve CLI installation separately, check which agent skills it installs or synchronizes, and disable startup synchronization if unwanted.

Risk: File exports return temporary public URLs.

Mitigation: Protect export links and share them only with intended recipients.

## Reference(s):

- [OOMOL RAG release on ClawHub](https://clawhub.ai/oomol/skills/oo-oomol-rag)
- [OOMOL RAG homepage](https://knowledge-base.oomol.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON payloads, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
