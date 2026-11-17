## Description:

Integrates with MissionClaw for project management and AI agent orchestration, including project creation, task tracking, team routing, and status lookups through the configured MissionClaw API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sureshchitmil](https://clawhub.ai/user/sureshchitmil)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to send project requests to MissionClaw, list projects, check project status, and understand available MissionClaw teams from an agent conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project names, descriptions, and status requests are sent to the configured MissionClaw API.

Mitigation: Keep MISSIONCLAW_URL set to localhost or another trusted MissionClaw service, and review project details before submission.

Risk: The artifact documentation describes broader MissionClaw app capabilities that are not all implemented by this skill command handler.

Mitigation: Treat dashboard, scheduler, organization chart, and agent-management behavior as connected MissionClaw app capabilities rather than direct commands implemented by this skill.

## Reference(s):

- [Missionclaw ClawHub listing](https://clawhub.ai/sureshchitmil/skills/missionclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown command responses with inline command examples and project status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the configured MISSIONCLAW_URL endpoint, defaulting to localhost.]

## Skill Version(s):

1.6.0 (source: server release metadata; artifact package.json is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
