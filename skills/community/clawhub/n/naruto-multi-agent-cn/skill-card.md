## Description:

Multi-agent dispatcher that turns the main agent into a Chinese Naruto-themed coordinator which delegates work to five persistent sub-agent sessions with fixed session keys and round-robin scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[be1human](https://clawhub.ai/user/be1human)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to coordinate agent work through reusable sub-agent sessions while preserving a Chinese Naruto-themed dispatcher persona. It is suited to task routing, parallel task decomposition, and delegated agent execution where the user accepts the persistent-session coordination model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly forces real work into persistent sub-agent sessions without clear user control or containment.

Mitigation: Install only when persistent delegated sessions are desired, and avoid tasks requiring direct main-agent inspection, strict context isolation, or independent result verification.

Risk: Delegated sessions may expose or retain sensitive context across tasks.

Mitigation: Do not use this skill for secrets, credentials, private code, regulated data, or other sensitive inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/be1human/skills/naruto-multi-agent-cn)
- [Publisher profile](https://clawhub.ai/user/be1human)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown responses with delegated sub-agent task requests and synthesized results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegates work through five named persistent sub-agent sessions using fixed session keys and a 300 second run timeout.]

## Skill Version(s):

1.5.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
