## Description: <br>
Dev Git Guard enforces a git-first repository workflow that checks status, reviews dirty files, validates changes, and creates detailed Chinese commit messages before and after coding tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ontheway23333](https://clawhub.ai/user/ontheway23333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill in local git repositories to preserve existing work, validate changes, and keep implementation work separated into auditable Chinese-language commits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause an agent to inspect worktrees, run project validation commands, stage changes, and create local commits automatically. <br>
Mitigation: Install only in repositories where this git workflow is desired, and review dirty changes plus validation results before commits are created. <br>
Risk: The required Chinese commit messages may conflict with repositories that require English-only metadata or manual approval before committing. <br>
Mitigation: Avoid using this skill in repositories with English-only commit policy, manual commit approval requirements, or stricter team governance. <br>


## Reference(s): <br>
- [Chinese commit template](references/commit-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/ontheway23333/git-commit-guard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and Chinese commit-message structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to stage files and create local git commits after review and validation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
