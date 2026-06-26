## Description: <br>
Generate conventional commit messages from code changes or diff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hazy-ca](https://clawhub.ai/user/hazy-ca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to draft Conventional Commits messages from git diffs or natural-language descriptions of code changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diffs can contain secrets or sensitive implementation details. <br>
Mitigation: Review and redact diffs before sharing them with the skill. <br>
Risk: Generated commit messages may not accurately summarize the change. <br>
Mitigation: Review the selected message before copying it or using it in a git commit. <br>
Risk: Optional clipboard or git commit actions could apply a message before the user has chosen it. <br>
Mitigation: Only allow clipboard actions or actual commits after explicit user selection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hazy-ca/it-commit-helper) <br>
- [Publisher profile](https://clawhub.ai/user/hazy-ca) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with Conventional Commit message options and analysis notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces concise, standard, and full commit-message variants; no executable code or hidden access.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
