## Description: <br>
Reviews pull requests with scope validation, requirements compliance, and line comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review GitHub or GitLab pull and merge requests against stated scope, requirements, version consistency, hygiene, and review quality expectations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide posting review comments, creating issues, publishing insights, and retaining review knowledge outside the local chat. <br>
Mitigation: Require explicit approval before posting to PRs, creating issues, publishing insights, or retaining knowledge-capture entries. <br>
Risk: The security scan flags under-scoped external posting and persistent knowledge-capture behavior for user review. <br>
Mitigation: Disable broad triggers where possible and use --no-capture unless persistent knowledge capture is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-sanctum-pr-review) <br>
- [OpenClaw metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [GitHub PR comment patterns](artifact/modules/github-comments.md) <br>
- [Knowledge capture module](artifact/modules/knowledge-capture.md) <br>
- [PR hygiene module](artifact/modules/pr-hygiene.md) <br>
- [Version validation module](artifact/modules/version-validation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review reports with inline shell command examples and optional PR or issue comments.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include classified findings, scope compliance checks, version validation results, backlog items, and knowledge-capture summaries.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
