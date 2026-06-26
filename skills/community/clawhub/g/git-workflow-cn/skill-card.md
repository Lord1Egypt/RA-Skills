## Description: <br>
Git 工作流助手 - 分支管理、冲突解决、提交规范。适合：开发者、团队协作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill as a Chinese-language Git workflow helper for branch management, conflict resolution, commit conventions, common recovery tasks, and command reference guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Git commands for hard resets, forced cleanup, branch deletion, history rewriting, garbage collection, or shared-branch pushes can discard work or alter repository history. <br>
Mitigation: Confirm the repository, branch, remote target, and intended data loss before execution, and require explicit approval for destructive or shared-remote operations. <br>
Risk: Global Git configuration changes can affect future work outside the current repository. <br>
Mitigation: Prefer repository-local configuration unless the user explicitly asks for a global setting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/git-workflow-cn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, text] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language Git workflow reference and command suggestions; command execution requires git.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
