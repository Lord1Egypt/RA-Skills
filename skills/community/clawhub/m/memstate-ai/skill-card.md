## Description:

Versioned, structured memory for AI agents that stores current facts and preserves change history using the Memstate API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yepthatsjason](https://clawhub.ai/user/yepthatsjason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to recall, store, search, update, inspect, and soft-delete structured project memory through Memstate AI. It is useful when an agent needs persistent versioned context across tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent external memory may expose sensitive project details if agents store secrets, regulated data, customer data, or private information.

Mitigation: Use the skill only for approved Memstate data and avoid storing secrets, regulated data, customer data, or private project details unless explicitly approved.

Risk: Recalled memories may be stale, incomplete, or untrusted reference material.

Mitigation: Treat retrieved memory as context to review, and verify important facts before using them for decisions or code changes.

Risk: Delete, recursive delete, and project delete commands can remove active memory entries or whole projects.

Mitigation: Require explicit human review before running destructive memory commands, especially recursive or project-level deletes.

## Reference(s):

- [Memstate AI](https://memstate.ai)
- [Memstate Documentation](https://memstate.ai/docs)
- [ClawHub Skill Page](https://clawhub.ai/yepthatsjason/skills/memstate-ai)
- [Publisher Profile](https://clawhub.ai/user/yepthatsjason)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and MEMSTATE_API_KEY; helper scripts communicate with the Memstate AI API.]

## Skill Version(s):

1.2.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
