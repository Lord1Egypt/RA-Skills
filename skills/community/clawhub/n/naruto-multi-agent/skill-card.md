## Description:

Naruto-themed multi-agent dispatcher that has an agent roleplay as Tsunade, assess mission ranks, and delegate tasks to five named sub-agent sessions with round-robin scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[be1human](https://clawhub.ai/user/be1human)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to route substantive work through a Naruto-themed dispatcher that assigns tasks to persistent sub-agent sessions. It is best suited for workflows where roleplay-heavy coordination and named delegation are desired.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User requests may include credentials, secrets, or unrelated private data that could be passed into delegated sub-agent task briefings.

Mitigation: Avoid including secrets or unrelated private context unless that information is intended to be shared with the delegated sub-agent.

Risk: The skill is a roleplay-heavy dispatcher and may add themed narration around task routing.

Mitigation: Use it where themed coordination is acceptable, and review delegated task briefings for clarity before relying on the results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/be1human/skills/naruto-multi-agent)
- [Publisher profile](https://clawhub.ai/user/be1human)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with delegated task briefings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegates work to named sub-agent sessions and instructs the dispatcher not to use execution, file, or search tools directly.]

## Skill Version(s):

1.0.0 (source: server evidence, SKILL.md frontmatter, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
