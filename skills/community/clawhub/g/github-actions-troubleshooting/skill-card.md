## Description: <br>
Troubleshoot GitHub Actions workflows, particularly for Go projects. Diagnose failing workflows, distinguish between code and environment issues, interpret logs, and apply fixes for common CI/CD problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[irook661](https://clawhub.ai/user/irook661) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect GitHub Actions failures, review logs and artifacts, and decide whether CI problems come from code, dependencies, or environment configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to use the active GitHub CLI login for repository troubleshooting. <br>
Mitigation: Confirm the intended GitHub account and repository before running suggested gh commands. <br>
Risk: Downloaded workflow artifacts or logs may contain sensitive project information. <br>
Mitigation: Review artifacts locally before sharing them or including their contents in follow-up prompts. <br>
Risk: Dependency or linter fixes may modify local project files. <br>
Mitigation: Inspect generated changes before committing or pushing them. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/irook661/github-actions-troubleshooting) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/irook661) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose GitHub CLI, Git, Go module, and linter commands for review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
