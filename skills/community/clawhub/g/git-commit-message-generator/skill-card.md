## Description: <br>
Generate conventional commit messages by analyzing staged changes automatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelatamuk](https://clawhub.ai/user/michaelatamuk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn staged Git changes into concise Conventional Commits messages with appropriate type, scope, body, and breaking-change details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Staged diffs can include secrets, regulated data, or proprietary code that the agent will inspect while generating a message. <br>
Mitigation: Review staged files before invoking the skill and avoid using it on sensitive or proprietary material you do not want analyzed. <br>
Risk: Generated commit messages may misclassify the change type, scope, or breaking-change impact. <br>
Mitigation: Treat the output as a draft and review the message before committing. <br>


## Reference(s): <br>
- [Conventional Commits Specification](https://www.conventionalcommits.org) <br>
- [Commit Types Quick Reference](COMMIT_TYPES_REFERENCE.md) <br>
- [Real-World Commit Message Examples](EXAMPLES.md) <br>
- [Commitlint Documentation](https://commitlint.js.org) <br>
- [Semantic Release](https://semantic-release.gitbook.io) <br>
- [Semantic Versioning](https://semver.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text commit-message drafts with optional inline shell commands and footers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires staged Git changes for best results; generated messages should be reviewed before committing.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
