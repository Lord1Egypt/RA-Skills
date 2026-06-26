## Description: <br>
Automated pull request review providing detailed feedback on correctness, security, performance, maintainability, testing, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and reviewers use this skill to collect pull request diff context and produce structured review guidance across correctness, security, performance, maintainability, testing, and best practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository diffs may contain secrets, private code, or other sensitive project context. <br>
Mitigation: Use the skill only on repositories and pull requests you are authorized to review, and avoid sharing generated diff context outside approved channels. <br>
Risk: Fetching GitHub pull request diffs uses the local GitHub CLI identity. <br>
Mitigation: Use a GitHub CLI account with only the access needed for the pull requests under review. <br>
Risk: Automated review guidance can miss issues or suggest changes that do not match project intent. <br>
Mitigation: Treat generated findings as reviewer input and keep human review as the decision point before merging or requesting changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/pr-review-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown review data by default, JSON when requested, or GitHub-comment-ready Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes changed-file stats, focus areas, and diff context; review output may be truncated when file or diff-size limits are reached.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
