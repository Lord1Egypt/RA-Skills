## Description: <br>
gstack-review guides agents through multi-perspective code reviews using CEO/Product, Engineering, and QA lenses while gathering git diff, test, lint, and build context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[klesenchang](https://clawhub.ai/user/klesenchang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to have an agent review code changes, pull requests, branches, or recent commits with product, architecture, security, correctness, and testing perspectives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to run tests, lint, build, git, or npx commands in a target repository, which can execute repository-controlled code. <br>
Mitigation: Use it on trusted repositories, or instruct the agent to inspect files only and avoid command execution when reviewing untrusted projects. <br>


## Reference(s): <br>
- [Garry Tan gstack inspiration](https://github.com/garrytan/gstack) <br>
- [ClawHub skill page](https://clawhub.ai/klesenchang/gstack-review-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review report with shell command context and action items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include test, lint, and build status summaries when the agent runs repository checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
