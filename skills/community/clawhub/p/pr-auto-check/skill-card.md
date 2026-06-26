## Description: <br>
Automated PR submission pipeline that runs code review, verifies service health, and posts the result to a Discord channel when a new PR needs automated review, health validation, and team notification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and repository maintainers use this skill to inspect pull requests, collect CI and diff information, run or reuse health checks, and notify a team through Discord. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide GitHub PR review workflows and produce notifications that affect public repository coordination. <br>
Mitigation: Review GitHub comments, labels, close actions, and proof-publishing commands before allowing them, as recommended by the security guidance. <br>
Risk: The Discord webhook posts PR status information to an external service. <br>
Mitigation: Use only approved webhook URLs and review the generated result file before sending notifications. <br>


## Reference(s): <br>
- [PR Auto-Check on ClawHub](https://clawhub.ai/terrycarter1985/pr-auto-check) <br>
- [Output format](references/output-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands and JSON result data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces pull request status summaries, health status, changed-file lists, temporary JSON result files, and Discord notification payloads.] <br>

## Skill Version(s): <br>
3.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
