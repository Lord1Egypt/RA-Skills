## Description:

Sets up and maintains a governance workspace for AI-assisted long-running projects, including a project protocol, directory index, error log, session handoff, changelog, stable version index, and whitelist/blacklist parameter registries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[century0327](https://clawhub.ai/user/century0327)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to scaffold and maintain durable project governance files for long-running AI-assisted work. It helps agents find authoritative files, preserve handoff state, record lessons, track versions, and avoid repeating known mistakes across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent project-governance files that future AI sessions may read and follow.

Mitigation: Install it only in trusted, version-controlled project directories and review generated AGENTS.md and index.md before relying on them.

Risk: The project index can include data from filenames and index_notes.json content that may not be sufficiently sanitized.

Mitigation: Avoid running the index command on repositories with adversarial filenames or untrusted index_notes.json content until escaping and validation are hardened.

Risk: Automatic skill discovery and loading are documented as primarily tested for Trae Skills.

Mitigation: For other agents, verify that the generated governance files are loaded and followed as intended before depending on the workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/century0327/skills/project-governance)
- [README](artifact/README.md)
- [Example Workflow](artifact/examples/example-workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated governance files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent project governance files and registries in the target project directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
