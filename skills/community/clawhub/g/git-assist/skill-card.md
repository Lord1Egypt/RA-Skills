## Description: <br>
Generate commit messages from diffs, write PR descriptions, create changelogs, and suggest branch names for Git workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to draft conventional commit messages, pull request summaries, changelog groupings, and branch names from local Git repository context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads staged diffs and commit history, which may include sensitive repository content. <br>
Mitigation: Use it only in repositories where that context is appropriate to expose to the local or configured model. <br>
Risk: Generated commit messages, PR descriptions, changelogs, or branch names may be inaccurate or incomplete. <br>
Mitigation: Review generated text before committing, publishing, or opening a pull request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/git-assist) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/TheShadowRose) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with Git command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are generated from local repository diffs, commit history, and user-provided branch descriptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
