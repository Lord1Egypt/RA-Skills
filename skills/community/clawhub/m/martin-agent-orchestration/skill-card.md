## Description:

Spawn and manage sub-agents with structured prompts, progress tracking, outcome reviews, and optional SkillBoss API routing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create clearer delegated-agent prompts, choose research/build/review agent patterns, track active agents, and capture lessons from completed work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional SkillBoss API usage can send selected prompt messages to a third-party service.

Mitigation: Use explicit approval and avoid sending credentials, private code, customer data, or sensitive conversation history in API-routed messages.

Risk: Local tracking notes may record details about active work and agent outcomes.

Mitigation: Keep tracking notes scoped to non-sensitive task metadata and review them before sharing outside the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godferylindsay/skills/martin-agent-orchestration)
- [Publisher profile](https://clawhub.ai/user/godferylindsay)
- [SkillBoss setup guide](https://skillboss.co/skill.md)
- [Active agents tracking template](examples/active-agents.md)
- [Builder agent template](templates/builder-agent.md)
- [Research agent template](templates/research-agent.md)
- [Review agent template](templates/review-agent.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with prompt templates, checklists, tables, and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local tracking note patterns and an optional SkillBoss API example.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
