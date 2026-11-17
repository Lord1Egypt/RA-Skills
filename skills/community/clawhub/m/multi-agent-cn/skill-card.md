## Description:

Multi-Agent CN is a Chinese-language dispatcher that triages user tasks and delegates work to five reusable sub-agent sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[be1human](https://clawhub.ai/user/be1human)

### License/Terms of Use:


## Use Case:

Developers and agent users can use this skill to coordinate coding, review, research, documentation, and other work across five reusable sub-agent sessions with Chinese-language task triage and round-robin delegation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates work through persistent sub-agent sessions, which can retain copied task context across delegated runs.

Mitigation: Avoid sensitive, private, credential-bearing, or regulated tasks unless persistent delegated sessions are acceptable.

Risk: The skill restricts the main agent to dispatching and reporting, which may reduce direct oversight of tool use and task execution.

Mitigation: Review delegated task plans and results before applying code, configuration, or operational changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/be1human/skills/multi-agent-cn)
- [Publisher profile](https://clawhub.ai/user/be1human)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Code, Markdown]

**Output Format:** [Markdown and delegated agent responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes work through persistent alpha, bravo, charlie, delta, and echo sub-agent sessions.]

## Skill Version(s):

1.2.0 (source: server release and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
