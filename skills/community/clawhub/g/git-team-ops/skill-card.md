## Description: <br>
Role-based GitOps skill for OpenClaw agents with junior and senior operating modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[launchthatbot](https://clawhub.ai/user/launchthatbot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and teams use this skill to coordinate OpenClaw coding agents in GitHub repositories with junior PR-only and senior review, merge, workflow, and release-control roles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Senior mode can merge pull requests, manage repository workflows, and trigger release or deployment workflows. <br>
Mitigation: Install only for repositories where this authority is intended; enforce branch protection, require CI to pass before merge, and prefer least-privilege GitHub App installation tokens. <br>
Risk: Fallback PATs, BYO GitHub App private keys, and onboarding tokens can expose repository access if mishandled. <br>
Mitigation: Prefer short-lived installation tokens, treat all credentials as sensitive, do not print or commit secrets, and never persist onboarding tokens beyond one session. <br>
Risk: Bundled workflow and CODEOWNERS templates may not match a team's repository controls. <br>
Mitigation: Review and adapt templates in a bootstrap pull request before merging them to the default branch. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/launchthatbot/git-team-ops) <br>
- [LaunchThatBot website](https://launchthatbot.com) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>
- [Junior PR validation workflow template](templates/github/workflows/junior-pr-validate.yml) <br>
- [Senior release control workflow template](templates/github/workflows/senior-release-control.yml) <br>
- [CODEOWNERS template](templates/github/CODEOWNERS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text operational guidance, Git commands, PR descriptions, and repository configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports role mode, repository, branch, changed files or workflows, and the next required human approval step.] <br>

## Skill Version(s): <br>
0.1.5 (source: SKILL.md frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
