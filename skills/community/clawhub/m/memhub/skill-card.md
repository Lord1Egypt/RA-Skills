## Description:

MemHub lets an agent manage a user-designated cross-agent memory repository with MemHub Protocol v0.1, including remembering, retrieving, forgetting, exporting context, and configuring Git sync with explicit user consent for persistent writes and remote changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutd](https://clawhub.ai/user/cutd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use MemHub when they want an agent to maintain, retrieve, archive, export, and optionally Git-sync a dedicated long-term memory repository across agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-term memory may retain sensitive, stale, or unwanted personal context.

Mitigation: Use a dedicated MEMHUB_REPO, review what gets remembered, and use the skill's forget, inbox, and promote workflows to keep retained context intentional.

Risk: After sync setup or onboard, memory reads may pull and memory writes may push repository content on a throttle.

Mitigation: Configure sync only when the user explicitly asks for it, and choose manual sync or no-sync options when automatic pull or push is not desired.

Risk: OAuth codes, client secrets, or access tokens could be exposed if shared in chat.

Mitigation: Do not paste tokens or OAuth codes into chat; use the supported authorization flow and local credential storage instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cutd/skills/memhub)
- [README](artifact/README.md)
- [Permission boundary](artifact/permissions.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated memory context text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for agent use with explicit user consent for persistent writes, remote sync setup, OAuth, repository creation, and apply-mode mutations.]

## Skill Version(s):

0.4.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
