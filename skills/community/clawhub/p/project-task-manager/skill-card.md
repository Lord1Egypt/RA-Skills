## Description:

Guides agents in creating hierarchical project plans, breaking down tasks, and tracking progress through AgentPMT.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and project teams use this skill to turn objectives into task trees, decompose individual tasks, and monitor or update project progress across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project objectives, task notes, and progress are sent to AgentPMT and task trees persist across sessions.

Mitigation: Share only the planning details needed; exclude proprietary or sensitive information unless remote storage is acceptable.

Risk: Supporting setup skills may be installed from unverified or changing sources.

Mitigation: Prefer verified or pinned installation paths for supporting setup skills.

## Reference(s):

- [Project Task Manager on ClawHub](https://clawhub.ai/agentpmt/skills/project-task-manager)
- [AgentPMT marketplace listing](https://www.agentpmt.com/marketplace/project-task-manager)
- [Project Task Manager action schema](artifact/schema.md)
- [AgentPMT account setup skill](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Text]

**Output Format:** [Markdown guidance and JSON task-plan responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task trees can persist across sessions; generation, updates, and status checks use AgentPMT credits.]

## Skill Version(s):

1.0.1 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
