## Description:

Memory Store lets agents store, retrieve, and maintain user-enabled structured memories across sessions and agents with policy-controlled local storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[revolves](https://clawhub.ai/user/revolves)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to let supported coding and AI agents recall durable decisions, fixes, preferences, workflows, and handoff state across sessions. It is intended for explicit or opt-in policy-controlled memory, not automatic background transcript capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local memory stores are plaintext, so secrets, credentials, tokens, and sensitive personal data could be exposed to users or processes with filesystem access.

Mitigation: Do not store secrets or sensitive personal data; review memory-store directory permissions before installation and use an appropriate secret manager for confidential data.

Risk: Private visibility is a cooperation filter rather than a confidentiality boundary, and private-memory records can be copied into shared summary or index files.

Mitigation: Treat private records as convenience filtering only, avoid confidential content, and review shared summaries and indexes when handling sensitive workflows.

Risk: Operational installs can drift if package versions are not pinned.

Mitigation: Pin npm package versions for reviewed deployments and re-run security and functional review before upgrading.

## Reference(s):

- [CLI Reference](references/cli.md)
- [Operations and Safety](references/operations.md)
- [Memory Schema](references/memory_schema.json)
- [Security Model](SECURITY.md)
- [Memory Store on ClawHub](https://clawhub.ai/revolves/skills/memory-store-skill)
- [memory-store-skill on npm](https://www.npmjs.com/package/memory-store-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read and write local JSON memory stores according to the selected profile, scope, and visibility.]

## Skill Version(s):

1.1.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
