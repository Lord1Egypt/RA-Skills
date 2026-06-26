## Description: <br>
Writes clear, structured GitHub pull request descriptions using a standardized template populated from branch diffs or provided context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djc00p](https://clawhub.ai/user/djc00p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to draft or update GitHub pull request bodies with summaries, change descriptions, impact notes, and testing guidance before review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A generated PR body may disclose sensitive details present in diffs or commit messages. <br>
Mitigation: Review and redact the generated PR description before posting it to GitHub. <br>
Risk: GitHub CLI actions could target the wrong repository or branch if context is stale or ambiguous. <br>
Mitigation: Confirm the target repository and branch before allowing any GitHub CLI action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/djc00p/github-pr-writer) <br>
- [Pull Request Template](artifact/assets/pull_request_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown pull request description with optional shell commands for gathering diff context.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review the generated PR body before posting, especially when diffs or commit messages include sensitive details.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
