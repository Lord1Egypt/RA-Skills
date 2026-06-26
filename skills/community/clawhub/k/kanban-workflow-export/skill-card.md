## Description: <br>
Kanban Workflow is a TypeScript skill for a stage-based agentic co-worker that integrates PM platforms via CLI-first adapters and provides setup, workflow verbs, polling, diffing, and automation hooks around a canonical Kanban stage model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonvanlaak](https://clawhub.ai/user/simonvanlaak) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate work items across GitHub, Planka, Plane, and Linear through a shared stage workflow. It helps agents select the next task, start work, post updates or questions, complete work for review, create backlog items, and run scheduled progress automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and update work items using the permissions of authenticated PM CLIs or API-key backed adapter commands. <br>
Mitigation: Use least-privilege accounts, scoped tokens, and repo- or project-limited CLI sessions for each adapter. <br>
Risk: The generated config file contains workspace, repository, project, and stage-mapping metadata that may reveal internal structure. <br>
Mitigation: Review config/kanban-workflow.json before committing or sharing it, and treat it as sensitive metadata. <br>
Risk: Cron-driven autopilot and automatic progress updates can post recurring external comments or stage changes. <br>
Mitigation: Enable scheduled automation only in workspaces where periodic comments and transitions are expected and acceptable. <br>


## Reference(s): <br>
- [Kanban Workflow README](README.md) <br>
- [Security](SECURITY.md) <br>
- [Adapter Notes](src/adapters/README.md) <br>
- [Requirements](references/REQUIREMENTS.md) <br>
- [Architecture Review](references/ARCH_REVIEW.md) <br>
- [Technical Plan](references/TECH_PLAN.md) <br>
- [GitHub CLI](https://cli.github.com/) <br>
- [Planka CLI](https://github.com/voydz/planka-cli) <br>
- [Plane](https://github.com/makeplane/plane) <br>
- [Linear GraphQL API](https://api.linear.app/graphql) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text CLI output, including work-item details, workflow status, comments, next-step tips, and setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may reflect project-management data available to the authenticated adapter CLI.] <br>

## Skill Version(s): <br>
0.1.4 (source: package.json, CHANGELOG, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
