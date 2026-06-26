## Description: <br>
提交与建 PR 桥接自动化。负责将“可提交”改动落成 commit、推送分支并创建 PR，衔接 peter-code-review 与 peter-pr-ops。用于用户提到“帮我提交”“推分支”“创建 PR”“从 review 到 merge 串起来”等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinasilva](https://clawhub.ai/user/chinasilva) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to turn reviewed local changes into a commit, push the active feature branch, and create or report a pull request. It is intended for workflows where code review has already determined that changes are ready to submit or ready with explicitly noted risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change Git state and publish a branch or pull request using the user's configured GitHub account. <br>
Mitigation: Before use, confirm the repository, branch, remote, diff, staged files, and active gh account. <br>
Risk: Repository workflow checks may execute local project code, which is riskier in untrusted repositories. <br>
Mitigation: Use the skill only in trusted repositories or inspect the configured workflow commands before allowing them to run. <br>
Risk: Unrelated local changes could be included in a commit if file selection is not reviewed. <br>
Mitigation: Stage only task-relevant files and avoid broad staging unless explicitly requested. <br>


## Reference(s): <br>
- [Peter Commit Ops on ClawHub](https://clawhub.ai/chinasilva/peter-commit-ops) <br>
- [Publisher profile: chinasilva](https://clawhub.ai/user/chinasilva) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with inline shell commands and status sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports pre-checks, executed Git and GitHub actions, commit SHA, branch, PR URL or blocking reason, and next-step guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
