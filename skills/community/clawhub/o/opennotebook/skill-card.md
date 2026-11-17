## Description:

OpenNotebook is a knowledge management client for notebooks, sources, notes, AI search, transformation pipelines, models, embeddings, chat, podcasts, and credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iazrael](https://clawhub.ai/user/iazrael)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage OpenNotebook resources through a command-line client or Python API client. It supports creating and updating notebooks, uploading and organizing sources, creating notes, searching or asking questions over the knowledge base, and managing OpenNotebook models and processing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform broad administrative and destructive OpenNotebook actions, including uploads, deletes, credential changes, settings changes, model changes, and migrations.

Mitigation: Require explicit confirmation before those operations and review proposed commands before execution.

Risk: The skill uses an OpenNotebook API key and may expose it if passed directly on the command line or stored carelessly.

Mitigation: Use only an API key whose permissions are acceptable for agent use, avoid passing keys with --api-key, and protect ~/.openclaw/opennotebook.env.

Risk: Server security evidence rates the release as suspicious because disclosure and credential-safety gaps accompany real administrative functionality.

Mitigation: Review the skill carefully before installation and deploy it only in environments where its OpenNotebook permissions are understood.

## Reference(s):

- [OpenNotebook API Reference](artifact/api_reference.md)
- [OpenNotebook Skill Page](https://clawhub.ai/iazrael/skills/opennotebook)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python usage examples, and API response data from OpenNotebook.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, OPENNOTEBOOK_BASE_URL, and OPENNOTEBOOK_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
