## Description:

Installs HeyCube profile-memory support for OpenClaw, including pre- and post-conversation hook skills, local SQLite profile storage, and configuration updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmmmmmtl](https://clawhub.ai/user/mmmmmmtl)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to set up HeyCube profile memory so an agent can load relevant local profile context before a conversation and update local profile records after substantive conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent hooks can process future conversations and send sanitized summaries to an external HeyCube service.

Mitigation: Install only with informed user consent, configure the API key intentionally, and disable the hooks with .heycube-off or by removing the AGENTS.md hook block and copied hook skills.

Risk: The setup stores an API key and inferred profile data in local workspace files.

Mitigation: Keep the workspace protected, avoid storing unnecessary sensitive profile details, and remove the API key and local SQLite database when uninstalling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mmmmmmtl/skills/heycube-setup)
- [HeyCube service website](https://heifangti.com)
- [HeyCube API base URL](https://heifangti.com/api/api/v1/heifangti)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands, configuration snippets, and code file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance for installing hook skills and a local SQLite helper.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
