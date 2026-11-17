## Description:

Helps agents capture failures, user corrections, feature requests, knowledge gaps, and better practices as durable learning records that can be promoted into long-term guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lygjoey](https://clawhub.ai/user/lygjoey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to make an agent record useful task experience, error patterns, and feature requests in local Markdown logs and promote repeated lessons into durable agent guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store task and user-derived details in durable local learning records.

Mitigation: Review or constrain writes to .learnings/ and redact secrets, private customer data, or sensitive research before using the skill.

Risk: The skill can promote repeated lessons into persistent agent rules or new skills without a clear approval gate.

Mitigation: Require explicit human approval before changes to AGENTS.md, TOOLS.md, SOUL.md, or skills/ are accepted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lygjoey/skills/proactive-self-improving)
- [ClawHub publisher profile](https://clawhub.ai/user/lygjoey)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with file templates and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local learning record formats and promotion guidance; no external API output is defined.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
