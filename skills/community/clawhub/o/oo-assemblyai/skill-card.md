## Description:

AssemblyAI (assemblyai.com). Use this skill for ANY AssemblyAI request — reading, creating, updating, and deleting data. Whenever a task involves AssemblyAI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill with an OOMOL-connected AssemblyAI account to create, list, read, and delete transcripts, including retrieving paragraph and sentence views. Creation and deletion actions require confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs remote installer code whose contents have not been verified.

Mitigation: Review the installer and CLI bundled-skill behavior, check installer integrity, and approve installation separately.

Risk: External credential handling has not been verified.

Mitigation: Review credential handling before connecting an account; use the OOMOL-mediated connection and do not handle raw tokens.

## Reference(s):

- [AssemblyAI](https://www.assemblyai.com/)
- [AssemblyAI API documentation](https://www.assemblyai.com/docs)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses from the oo CLI and Markdown command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-dependent transcript data; write and destructive actions require confirmation.]

## Skill Version(s):

1.0.4 (source: server-resolved release, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
