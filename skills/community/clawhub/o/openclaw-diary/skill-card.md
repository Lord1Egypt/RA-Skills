## Description: <br>
Set up and manage an OpenClaw automatic learning diary by guiding users through forking the diary repository, connecting it to OpenClaw, scheduling daily updates, and publishing with GitHub Pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Trae1ounG](https://clawhub.ai/user/Trae1ounG) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to configure an automated public learning diary workflow backed by a forked GitHub repository, scheduled OpenClaw tasks, and GitHub Pages publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sets up an automatic public diary publisher using GitHub repository access. <br>
Mitigation: Use a fine-grained GitHub token limited to the diary fork, keep the token out of chat and logs, and review content before public pushes. <br>
Risk: Scheduled cron or heartbeat tasks may continue publishing after the user no longer wants automation. <br>
Mitigation: Confirm the user knows how to stop the cron or heartbeat task and revoke the GitHub token. <br>
Risk: Generated diary entries could expose private personal information or conversation content. <br>
Mitigation: Require user consent before publishing and avoid real names, IDs, phone numbers, passwords, API keys, tokens, and private conversation content. <br>


## Reference(s): <br>
- [OpenClaw-Diary GitHub repository](https://github.com/YAI-Lab/OpenClaw-Diary) <br>
- [Openclaw Diary ClawHub listing](https://clawhub.ai/Trae1ounG/openclaw-diary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, HTML snippets, configuration steps, and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responds in the user's language and proposes commands and public publishing steps that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
