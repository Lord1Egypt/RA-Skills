## Description: <br>
Auto-generate beautiful changelogs from git history, grouped by conventional commit types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fratua](https://clawhub.ai/user/Fratua) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release managers use this skill to generate categorized Markdown changelogs or release notes from git commit history, including conventional commit grouping, selected ranges, and breaking-change detection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated release notes may omit, miscategorize, or overstate changes if commit messages are incomplete or non-conventional. <br>
Mitigation: Review generated changelogs before publishing and provide an explicit range or path when precision matters. <br>
Risk: The skill can update CHANGELOG.md when requested, which may modify release documentation before it is ready. <br>
Mitigation: Request file output only when ready for a file change and review the resulting diff before release. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Fratua/git-changelog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown changelog text with categorized sections and optional CHANGELOG.md updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or prepend to CHANGELOG.md only when the user requests file output.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
