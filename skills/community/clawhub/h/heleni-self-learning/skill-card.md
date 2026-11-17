## Description:

Continuous self-improvement through systematic logging, pattern detection, and behavioral updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users use this skill to log corrections, failures, feature requests, and recurring behavior patterns, then turn repeated learnings into durable configuration updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs and configuration updates can change future agent behavior in ways the user did not intend.

Mitigation: Require explicit review and per-file approval before changing memory, identity, skills, configuration, scheduled tasks, or commits.

Risk: Learning files could capture secrets or sensitive personal data.

Mitigation: Do not store passwords, tokens, API keys, private keys, recovery codes, or sensitive personal data in Markdown learning files.

Risk: Broad reads of personal memory and configuration can expose private context during reflection.

Mitigation: Scope reflection reads to the files needed for the requested behavior change and review generated notes before persisting them.

## Reference(s):

- [Heleni Self Learning on ClawHub](https://clawhub.ai/netanel-abergel/skills/heleni-self-learning)
- [Jarvis learning note](https://jarvis.ripper234.com/learn.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell scripts and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update persistent Markdown learning logs and configuration notes when the agent is granted file-editing authority.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
