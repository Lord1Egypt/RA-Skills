## Description: <br>
An AI-driven coding workflow for orchestrating parallel coding agents, one-person-company development automation, Playwright testing, and automated PR management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LongFer](https://clawhub.ai/user/LongFer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering leads, independent builders, startup teams, and open-source maintainers use this skill to coordinate multiple coding agents across isolated worktrees, generate and run Playwright tests, and manage GitHub issue-to-PR workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow gives agents broad repository and GitHub authority, including creating branches, pushing code, opening PRs, and merging successful checks. <br>
Mitigation: Start in a disposable fork, use least-privilege GitHub credentials, require protected branches and CI, and keep human approval in front of push and merge steps. <br>
Risk: Autonomous coding teams may introduce incorrect code, incomplete tests, or conflicts while working in parallel. <br>
Mitigation: Limit concurrency, isolate each team in a worktree, review diffs and generated tests before integration, and require CI plus manual review before accepting changes. <br>
Risk: Playwright authentication state, logs, reports, and notifications can expose sensitive test data or credentials. <br>
Mitigation: Keep auth state and reports out of shared or public locations, avoid publishing notification contents with secrets, and rotate any credentials used during testing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/LongFer/multi-team-coding) <br>
- [README.md](README.md) <br>
- [One-Person Company Guide](ONE-PERSON-COMPANY.md) <br>
- [Playwright Automation Guide](PLAYWRIGHT-AUTOMATION.md) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [OpenClaw Repository](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions, Markdown] <br>
**Output Format:** [Markdown with bash, TypeScript, JSON, and workflow examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent prompts, Git and GitHub CLI commands, Playwright configuration and test snippets, status dashboards, and report templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
