## Description: <br>
Automated AI code review for GitLab merge requests via polling, including open MR discovery, diff review for security issues, bugs, and best practices, and posting inline comments plus summary notes on GitLab. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gotoloops](https://clawhub.ai/user/gotoloops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to configure an agent that periodically reviews open GitLab merge requests, applies default or project-specific review rules, and posts review feedback back to GitLab. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run unattended and post comments across all merge requests visible to the configured GitLab token. <br>
Mitigation: Use a dedicated low-privilege GitLab bot token scoped only to intended projects, monitor generated comments, and disable the cron job when not actively needed. <br>
Risk: The cron worker can load project-specific custom review prompts from source branches before posting comments. <br>
Mitigation: Review or change the cron prompt before enabling automation, including rules for custom prompt loading and automatic posting. <br>
Risk: GitLab credentials may be exposed if the local `.env` file is committed or broadly readable. <br>
Mitigation: Keep `.env` out of source control, restrict file permissions, and use a token with only the permissions needed for the intended projects. <br>
Risk: Duplicate review comments can occur if the reviewed-MR tracking file is missing or not writable. <br>
Mitigation: Ensure the reviewed log exists and is writable, and keep an explicit highest-priority cron rule to never re-review already recorded merge requests. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/gotoloops/gitlab-auto-review) <br>
- [Cron Worker Setup](references/cron-setup.md) <br>
- [Review Guidelines](references/review-guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Posts GitLab inline review comments and summary notes when configured with GitLab access.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
