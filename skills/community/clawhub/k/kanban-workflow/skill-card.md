## Description: <br>
Kanban Workflow is a TypeScript skill for a stage-based agentic co-worker that integrates PM platforms via CLI-auth adapters only (no direct HTTP auth). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonvanlaak](https://clawhub.ai/user/simonvanlaak) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to standardize project-management work across GitHub, Planka, Plane, and Linear using a shared stage lifecycle and CLI-authenticated adapters. It supports setup, work-item selection, status updates, comments, task creation, completion, polling, diffing, and progress-update automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated PM CLIs may post comments, create tasks, assign tasks, or move workflow stages in repositories and projects available to the user's session. <br>
Mitigation: Install and run the skill only where the relevant PM CLIs are authenticated for the intended repositories or projects, and review write-oriented verbs before execution. <br>
Risk: Recurring progress updates can create unwanted noise or expose sensitive work status in project comments. <br>
Mitigation: Enable recurring progress updates only on appropriate projects and persist automation state so comments are posted at the intended interval. <br>


## Reference(s): <br>
- [Kanban Workflow README](README.md) <br>
- [Adapter documentation](src/adapters/README.md) <br>
- [Requirements](references/REQUIREMENTS.md) <br>
- [Technical Plan](references/TECH_PLAN.md) <br>
- [Architecture Review](references/ARCH_REVIEW.md) <br>
- [GitHub CLI](https://cli.github.com/) <br>
- [Planka CLI](https://github.com/voydz/planka-cli) <br>
- [Plane CLI](https://github.com/simonvanlaak/plane-cli) <br>
- [Linear CLI](https://github.com/simonvanlaak/linear-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with inline commands and JSON configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update project-management work items through the user's authenticated platform CLIs.] <br>

## Skill Version(s): <br>
0.1.12 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
