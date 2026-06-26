## Description: <br>
Sends daily Git change reports for image-tool remote branches and voc dev branches, with security and general code review for the previous day. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kidok](https://clawhub.ai/user/kidok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to schedule recurring Git activity summaries, changed-file statistics, and code review findings for monitored repositories. It is useful for daily team visibility when the listed repositories and DingTalk recipient are authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring reports may share commit details, changed files, statistics, and review findings outside the intended audience. <br>
Mitigation: Install only for repositories authorized for monitoring, verify DingTalk target 1923216025-1426160278 before scheduling, and remove the scheduled job when reporting is no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kidok/git-daily-report) <br>
- [Publisher profile](https://clawhub.ai/user/kidok) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires git, curl, and rg; sends recurring reports through DingTalk when scheduled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
