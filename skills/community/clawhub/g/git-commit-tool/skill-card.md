## Description: <br>
Helps an agent analyze Git changes, stage logical file groups, generate Conventional Commit messages, and create local commits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangchencheng](https://clawhub.ai/user/wangchencheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when they want an agent to inspect Git diffs, prepare coherent file staging, and produce Chinese Conventional Commit messages with an AI-GEN footer before creating a local commit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can stage files and create local commits, so unintended files or secrets could be included. <br>
Mitigation: Review git status, diffs, and staged files before approval, and exclude secrets or credentials from the commit. <br>
Risk: Generated Chinese commit messages and the AI-GEN footer may not match a repository's contribution conventions. <br>
Mitigation: Confirm repository commit standards and edit the proposed message or footer before running git commit. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/wangchencheng/git-commit-tool) <br>
- [Publisher profile](https://clawhub.ai/user/wangchencheng) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and commit message text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commit messages are expected to use Simplified Chinese and may include an AI-GEN footer.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
