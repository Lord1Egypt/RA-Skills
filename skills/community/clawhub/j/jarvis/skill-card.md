## Description:

Run the agent like an executive operator with calm briefings, sharp prioritization, context recovery, and proactive follow-through.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Jarvis to make an assistant operate with concise executive briefings, sharper prioritization, context recovery, approval-aware follow-through, and anti-drift guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores local Jarvis preference and mission-context files under ~/jarvis/, which may contain sensitive context if users add it.

Mitigation: Review ~/jarvis/ files periodically, avoid storing secrets or sensitive business details, and keep local memory compact and current.

Risk: Workspace steering blocks in AGENTS.md, SOUL.md, or HEARTBEAT.md can alter future agent behavior if added without review.

Mitigation: Require explicit approval before writing workspace steering blocks and keep additions visible, additive, and easy to remove.

Risk: Executive-style behavior may sound overconfident if the agent implies hidden monitoring or capabilities it does not have.

Mitigation: Follow the boundary guidance to state what was observed, what is inferred, and what approval is required before external actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/jarvis)
- [Skill homepage](https://clawic.com/skills/jarvis)
- [Setup guide](artifact/setup.md)
- [Safety boundaries](artifact/boundaries.md)
- [Use cases](artifact/use-cases.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with optional shell commands and local configuration file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local files under ~/jarvis/ and additive workspace steering blocks that require user approval.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
