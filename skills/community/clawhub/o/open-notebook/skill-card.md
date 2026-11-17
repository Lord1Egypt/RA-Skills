## Description:

Access and manage a self-hosted Open Notebook research system for creating notebooks, adding text, URL, or file sources, searching across notebooks, and RAG chat with stored research notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crabsticksalad](https://clawhub.ai/user/crabsticksalad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to connect agents to a self-hosted Open Notebook deployment, create and manage research notebooks, add sources, search saved material, and ask RAG questions over notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restricted agent keys may receive broader search or mutation access than expected.

Mitigation: Use only with a trusted local bridge, restrict access to agents.json and audit logs, and fix bridge authorization checks before relying on per-agent notebook isolation.

Risk: The skill can add sources and irreversibly delete notebook sources or notebooks.

Mitigation: Review requested write and delete operations before execution, confirm target notebook and source IDs, and keep backups for important notebook data.

Risk: Notebook data is stored unencrypted at rest in the upstream Open Notebook stack.

Mitigation: Do not store secrets, credentials, or sensitive PII in notebooks; use trusted deployments and review storage controls before use.

## Reference(s):

- [Open Notebook skill page](https://clawhub.ai/crabsticksalad/skills/open-notebook)
- [Open Notebook upstream project](https://github.com/lfnovo/open-notebook)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command invocations and JSON bridge responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Open Notebook bridge, OPEN_NOTEBOOK_BRIDGE_URL, and OPEN_NOTEBOOK_API_KEY.]

## Skill Version(s):

1.3.2 (source: frontmatter, server release, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
