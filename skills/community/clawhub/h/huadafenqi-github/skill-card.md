## Description: <br>
Interact with GitHub through the `gh` CLI for issues, pull requests, CI runs, and advanced API queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huadafenqi](https://clawhub.ai/user/huadafenqi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to compose GitHub CLI commands for checking pull requests, workflow runs, issues, and structured API queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands may act through the user's authenticated GitHub CLI account. <br>
Mitigation: Confirm the active `gh` account, scope commands to specific repositories, and review proposed actions before execution. <br>
Risk: `gh api` calls can create, modify, delete, publish, or trigger GitHub data. <br>
Mitigation: Review each `gh api` endpoint and payload before running mutating requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huadafenqi/huadafenqi-github) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands rely on the user's authenticated `gh` CLI context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
