## Description:

Pocket lets an agent search, list, and read a user's Pocket recordings, including transcripts and AI summaries, create audio download links, save recording audio to file storage, upload new audio recordings, and list tags through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent retrieve Pocket recording metadata, transcripts, summaries, tags, and temporary audio links, or upload audio files for transcription. It is suited to workflows such as meeting follow-up, searchable conversation review, CRM notes, task extraction, and document generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pocket recordings, transcripts, summaries, and audio links can expose sensitive conversation content.

Mitigation: Confirm the user is authorized before retrieving recordings, transcripts, summaries, download links, or saved audio copies, and keep requests scoped to the minimum needed recording data.

Risk: Audio upload and save workflows can move sensitive files between Pocket and AgentPMT File Manager.

Mitigation: Verify file ownership and user intent before uploading File Manager audio for transcription or saving recording audio, and observe the documented 100 MiB limit.

Risk: Setup commands and connected AgentPMT routes may run in environments that contain secrets.

Mitigation: Use the setup skills for credential handling and avoid running unpinned npx setup commands in environments with unnecessary secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/pocket-recordings-transcripts)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/pocket-recordings-transcripts)
- [Pocket action schema](artifact/schema.md)
- [AgentPMT account setup skill](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [File Management related skill](https://clawhub.ai/agentpmt/file-management)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON call examples and action schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defines seven AgentPMT Pocket actions, including recording search, retrieval, download-link creation, audio save, upload, and tag listing.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
