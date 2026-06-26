## Description: <br>
Automates GitHub pull request review workflows from structured review through issue tracking, CI validation, and merge-readiness reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review GitHub pull requests, convert blocking findings into GitHub issues, configure CI quality gates, and summarize whether a PR is ready to merge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change GitHub repositories and influence merge flow when broad credentials are granted. <br>
Mitigation: Use a fine-grained GitHub token limited to selected repositories and require explicit confirmation before creating issues, changing workflows, assigning users, or enabling merge-related behavior. <br>
Risk: Automated review findings or quality-gate decisions may be incomplete or incorrect. <br>
Mitigation: Keep branch protection and human review in place for high-impact changes, and treat generated review results as decision support rather than sole approval authority. <br>


## Reference(s): <br>
- [PR Review Factory README](artifact/README.md) <br>
- [PR Review Factory workflow definition](artifact/workflow.json) <br>
- [PR Review Factory on ClawHub](https://clawhub.ai/zlszhonglongshen/pr-review-factory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON-like summaries, YAML workflow snippets, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or suggest GitHub issues, PR comments, CI workflow files, quality-gate checks, and merge-readiness summaries when granted repository access.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
