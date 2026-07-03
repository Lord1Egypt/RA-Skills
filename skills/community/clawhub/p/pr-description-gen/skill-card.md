## Description: <br>
Auto-generate pull request descriptions from git diff and commit history. / 从 git diff 和提交历史自动生成 PR 描述。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingaiwork](https://clawhub.ai/user/kingaiwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to draft pull request descriptions from git diffs and commit history for personal, team, and enterprise workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository diffs and commit history may contain secrets, internal URLs, customer data, or personal metadata. <br>
Mitigation: Review and sanitize repository content before asking an agent or external tool to summarize it. <br>
Risk: Generated pull request descriptions may be incomplete or misleading. <br>
Mitigation: Review the generated description against the actual diff and commit history before publishing it. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/kingaiwork/skills/pr-description-gen) <br>
- [Project homepage](https://kingai.work/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown pull request description text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable payload; generated descriptions should be reviewed before publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
