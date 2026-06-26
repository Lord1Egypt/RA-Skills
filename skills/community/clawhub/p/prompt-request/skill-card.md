## Description: <br>
Automates a GitHub Issue to implementation, pull request creation, review, and merge pipeline for issues marked with an [auto] tag. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ShunsukeHayashi](https://clawhub.ai/user/ShunsukeHayashi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and repository maintainers use this skill to configure a webhook-driven GitHub automation pipeline that turns trusted [auto] issues into branch work, tests, pull requests, review comments, and optional merges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook-triggered automation can give an agent broad repository write and merge authority. <br>
Mitigation: Install only on repositories with trusted issue authors, PR commenters, and webhook sources; use least-privilege GitHub credentials and require maintainer approval before merge. <br>
Risk: Automatic merge logic can merge unsafe changes if review or CI gates are weak. <br>
Mitigation: Disable or gate auto-merge, require passing CI, and do not treat missing CI as success for protected repositories. <br>
Risk: Delivery to chat channels can expose private repository or issue content. <br>
Mitigation: Enable Telegram or other external delivery only when that data flow is approved for the repository. <br>


## Reference(s): <br>
- [Skill overview](artifact/SKILL.md) <br>
- [Webhook message template](artifact/templates/messageTemplate.txt) <br>
- [Sample hook configuration](artifact/examples/sample-hook-config.json) <br>
- [ClawHub skill page](https://clawhub.ai/ShunsukeHayashi/prompt-request) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with issue templates, hook configuration JSON, and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for GitHub webhook events, GitHub CLI authentication, and repository write workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
