## Description: <br>
OpenNexum coordinates contract-driven multi-agent coding workflows with ACP, contract sync, webhook and dispatch-queue dispatch, cross-review, auto-retry, and batch progress tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayao99315](https://clawhub.ai/user/ayao99315) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use OpenNexum to coordinate AI coding agents around contract YAML tasks, scoped deliverables, cross-review, retry, notifications, and progress tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable project-control instructions and default commit-and-push behavior can publish code without a clear human review gate. <br>
Mitigation: Install only in repositories where agent commits and pushes are acceptable, protect main branches, review generated changes before publication, and disable or blank the git remote when automatic push is not intended. <br>
Risk: Webhook callbacks, dispatch replay, and watch daemon behavior can act on project state and configured secrets. <br>
Mitigation: Review nexum/config.json, avoid committing webhook tokens, use the watch daemon only for intentionally managed projects, and keep callback credentials out of source control. <br>
Risk: The skill writes or updates AGENTS.md guidance that can affect future agent behavior in the repository. <br>
Mitigation: Review AGENTS.md changes during setup and after sync operations, especially in repositories with existing agent instructions. <br>


## Reference(s): <br>
- [OpenNexum ClawHub page](https://clawhub.ai/ayao99315/opennexum) <br>
- [README](README.md) <br>
- [Architecture](docs/design/ARCHITECTURE.md) <br>
- [Contract Schema Reference](references/contract-schema.md) <br>
- [Orchestrator Guide](references/orchestrator-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML, JSON, and bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce task payload JSON and AGENTS.md protocol updates when used through the CLI.] <br>

## Skill Version(s): <br>
2.1.4 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
