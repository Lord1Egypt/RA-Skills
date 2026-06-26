## Description: <br>
Role-based GitOps skill for OpenClaw agents with junior and senior operating modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[launchthatbot](https://clawhub.ai/user/launchthatbot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate OpenClaw coding agents in GitHub repositories with junior PR-only roles and senior review, merge, release, and workflow-management roles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Senior mode can merge pull requests and trigger release or deployment workflows, which can change protected repository behavior. <br>
Mitigation: Use minimal GitHub App permissions, keep branch protections enabled, require CI to pass before merge, and review bootstrap or workflow changes before merging. <br>
Risk: PAT or app credentials and onboarding tokens could expose repository access if logged or stored. <br>
Mitigation: Prefer short-lived installation tokens, avoid broad PATs, do not print secrets, and do not write credentials into repository files. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/launchthatbot/launchthatbot-git-team-ops) <br>
- [README](README.md) <br>
- [LaunchThatBot website](https://launchthatbot.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown guidance with repository actions, file-change summaries, and workflow or configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports role mode, repository, branch, changed files or workflows, and the next required human approval step.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
