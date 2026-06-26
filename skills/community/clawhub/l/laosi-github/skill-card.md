## Description: <br>
GitHub操作助手 provides PR, issue, code search, repository management, CI status monitoring, release management, and code review assistance through the GitHub CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to operate GitHub repositories from an agent workflow, including PR handling, issue management, repository inspection, code search, CI status checks, release management, and code review assistance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to use the logged-in GitHub CLI context for repository-changing actions such as merging PRs, closing issues, creating releases, or posting comments. <br>
Mitigation: Require an explicit repository, PR or issue number, and user confirmation before allowing state-changing GitHub operations. <br>
Risk: Examples include repository actions without consistent scoping guidance, which can cause changes to be applied to the wrong repository or target. <br>
Mitigation: Prefer commands and wrapper calls that specify the repository or verify the current repository before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/laosi-github) <br>
- [Publisher profile](https://clawhub.ai/user/534422530) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Assumes an authenticated GitHub CLI (`gh`) context.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
