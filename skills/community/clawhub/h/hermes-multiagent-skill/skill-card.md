## Description:

Hermes provides a Python message router for multi-agent coordination, delivering task, done, and system messages only to agents subscribed to matching topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[briefness](https://clawhub.ai/user/briefness)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to coordinate multiple agents through topic-based publish/subscribe routing, including optional lifecycle integration with sessions_spawn. It is intended for agent workflows that need sparse message delivery instead of broad message broadcasts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Message routing can mix or disrupt messages between agents.

Mitigation: Use the skill only for testing or non-sensitive coordination until routing bugs are fixed, and review routing behavior before production use.

Risk: Mutable or prematurely recycled messages can cause handlers to observe incorrect message contents.

Mitigation: Use immutable or copied messages and recycle message objects only after all handlers finish.

Risk: Duplicate active agent IDs can route messages to the wrong active participant.

Mitigation: Reject duplicate active agent IDs or isolate agents by session.

Risk: User-facing text is Chinese-only in the artifact.

Mitigation: Document the language limitation for users who need localized or English-only operational output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/briefness/skills/hermes-multiagent-skill)
- [Publisher Profile](https://clawhub.ai/user/briefness)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python code examples and API usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs describe in-process Python routing APIs; no external credentials or network services are required by the artifact.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
