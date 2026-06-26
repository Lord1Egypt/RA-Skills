## Description: <br>
GitHub issue and PR workflow automation for converting plans, reviews, and implementation results into GitHub issues, pull requests, comments, review feedback, and merge actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to manage GitHub issue and pull-request workflows, including issue registration, PR creation, review comments, dependency tracking, sanitization, and guarded merge preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make visible repository changes, including issue and PR edits, comments, dependency mutations, and merge-related actions. <br>
Mitigation: Install only when the agent is expected to manage GitHub issues and PRs, and require explicit approval for the exact target and action before writes or merges on important repositories. <br>
Risk: Approval rules for writes and merges are inconsistent across the workflow documentation. <br>
Mitigation: Tighten or override the rules before use so merges, dependency updates, public comments, and PR or issue edits require clear user confirmation. <br>
Risk: Repository language and public/private visibility rules may not match every team's workflow. <br>
Mitigation: Review and adapt the language and visibility rules before deployment, especially for multilingual teams or public repositories. <br>


## Reference(s): <br>
- [Github Flow on ClawHub](https://clawhub.ai/drumrobot/github-flow) <br>
- [GitHub Flow Skill Definition](SKILL.md) <br>
- [Issue Dependencies and Sub-issues](dependencies.md) <br>
- [Pull Request Workflow](pr.md) <br>
- [Merge Workflow](merge.md) <br>
- [Push Guards](push-guards.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, GitHub CLI/API examples, issue and PR body text, and review comment text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may guide visible GitHub repository changes through the user's configured GitHub credentials.] <br>

## Skill Version(s): <br>
0.4.1 (source: ClawHub release metadata and CHANGELOG, released 2026-06-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
