## Description:

Guides OpenClaw users through installing HeyCube personal profile memory by setting an API key, deploying a local SQLite helper, and installing trigger skills for profile retrieval and updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmmmmmtl](https://clawhub.ai/user/mmmmmmtl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure HeyCube as a personal memory service for OpenClaw. After setup, explicit trigger phrases can load relevant local profile context or save sanitized conversation-derived updates to a local SQLite profile store.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sanitized conversation summaries are sent to a third-party API.

Mitigation: Use explicit trigger phrases, review outbound summaries before sending, and avoid including sensitive personal details.

Risk: Structured personal profile data persists locally in SQLite.

Mitigation: Keep the database in a controlled workspace, avoid storing sensitive data, and add clear delete and export controls before regular use.

Risk: Remote API responses can steer later extraction and local profile updates.

Mitigation: Review returned dimensions and extraction prompts before writing local profile data, and skip updates when responses are unexpected.

Risk: The Node dependency is declared without a lockfile.

Mitigation: Pin dependencies with a lockfile before installation in a regular-use environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mmmmmmtl/skills/heycube)
- [HeyCube Service](https://heifangti.com)
- [HeyCube API Base URL](https://heifangti.com/api/api/v1/heifangti)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown setup guidance with inline shell commands, JSON examples, and file-copy instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces stepwise installation and operation guidance for a local SQLite profile helper and HeyCube trigger skills.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
