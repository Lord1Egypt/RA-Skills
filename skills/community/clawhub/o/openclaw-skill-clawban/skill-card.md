## Description: <br>
Openclaw Skill Clawban is a TypeScript skill for a stage-based agentic co-worker that integrates project-management platforms through CLI-first adapters and provides setup plus workflow verbs for a canonical kanban lifecycle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonvanlaak](https://clawhub.ai/user/simonvanlaak) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to discover, start, update, ask about, complete, and create work items across GitHub, Planka, Plane, or Linear while normalizing those systems to a shared kanban stage model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled automation can change external task state or post recurring comments. <br>
Mitigation: Use the skill first without --autopilot-install-cron, then enable cron or recurring comments only after reviewing affected repos, projects, stages, and the disable path. <br>
Risk: The skill inherits the privileges of the configured project-management CLI session or token. <br>
Mitigation: Use narrowly scoped accounts or tokens and verify the selected CLI authentication state before running workflow commands. <br>
Risk: The GitHub path may act on matching staged issues in scope rather than only tasks assigned to the agent. <br>
Mitigation: Configure GitHub repo and project scope narrowly, review candidate work items before automation, and avoid broad scopes until assigned-only behavior is confirmed. <br>


## Reference(s): <br>
- [Kanban Workflow requirements](references/REQUIREMENTS.md) <br>
- [Kanban Workflow technical plan](references/TECH_PLAN.md) <br>
- [Kanban Workflow architecture review](references/ARCH_REVIEW.md) <br>
- [Kanban Workflow adapters](src/adapters/README.md) <br>
- [GitHub CLI](https://cli.github.com/) <br>
- [planka-cli](https://github.com/voydz/planka-cli) <br>
- [Planka](https://github.com/plankanban/planka) <br>
- [Plane](https://github.com/makeplane/plane) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide or trigger project-management CLI actions that read, comment on, or transition external work items.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release evidence, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
