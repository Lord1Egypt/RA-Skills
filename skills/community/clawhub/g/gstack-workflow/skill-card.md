## Description: <br>
Structured development workflow inspired by Garry Tan's gstack for building features, starting projects, reviewing code, and shipping code through a disciplined Think, Plan, Build, Review, Test, and Ship process. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jahonn](https://clawhub.ai/user/jahonn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to run a structured development sprint from product framing through implementation, review, testing, and release. It is suited to feature work, new project starts, code review workflows, and shipping branches with staged checkpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can direct an agent to edit files, create commits, push to remotes, open pull requests, and take deploy-like release steps. <br>
Mitigation: Require explicit user confirmation before commits, browser actions on non-local systems, git pull or rebase, git push, opening pull requests, or deploy-like actions. <br>
Risk: Release actions could run against the wrong repository, branch, remote, diff, or commit message. <br>
Mitigation: Confirm the repository, branch, remote, pending diff, test status, and commit or pull request text before allowing release steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jahonn/gstack-workflow) <br>
- [Phase prompts](references/prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and conversational guidance with inline shell commands and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce DESIGN.md, PLAN.md, review reports, test reports, commits, pull requests, and release notes depending on the selected phase.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
