## Description: <br>
Generate conventional, descriptive commit messages from git diffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericlooi504](https://clawhub.ai/user/ericlooi504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to draft, rewrite, or validate Conventional Commits messages from staged changes, branch diffs, commit ranges, or provided diffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Git diffs or commit history can contain secrets, credentials, or sensitive implementation details. <br>
Mitigation: Review staged changes before use, avoid running the skill on diffs containing secrets, and do not provide credentials because the skill does not need them. <br>
Risk: Generated commit messages can omit context or mischaracterize a change, especially for large diffs summarized at chunk level. <br>
Mitigation: Review and edit the proposed message before using it in a commit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ericlooi504/git-commit-gen) <br>
- [Publisher profile](https://clawhub.ai/user/ericlooi504) <br>
- [Skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with Conventional Commits message blocks and brief rationale] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Proposed messages are shown for review before the user commits changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
