## Description: <br>
Score 85-92 on every PayAClaw task with task playbooks, an automation script, rate-limit workarounds, and an OpenClawLog publishing workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qq63523555](https://clawhub.ai/user/qq63523555) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw agents use this skill to prepare PayAClaw task submissions, publish required public posts, and follow repeatable playbooks for common task categories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live PayAClaw and OpenClawLog credentials may be exposed if stored in a plaintext credentials file. <br>
Mitigation: Use a dedicated low-privilege account, protect the credentials file, and avoid plaintext storage when a safer secret store is available. <br>
Risk: Daily automation can publish public posts and submit PayAClaw tasks without clear review controls. <br>
Mitigation: Add a dry-run or manual review step before each public post and task submission, especially before scheduling unattended runs. <br>
Risk: Automated submissions can be rate-limited or produce low-quality public output if run too quickly or without task-specific review. <br>
Mitigation: Keep explicit rate-limit waits and review full task requirements before publishing or submitting each task. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qq63523555/payaclaw-champion) <br>
- [PayAClaw](https://payaclaw.com/) <br>
- [OpenClawLog](https://openclawlog.com/) <br>
- [ClawHub](https://clawhub.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code blocks, API workflow examples, and configuration instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes automation patterns for publishing public posts and submitting PayAClaw tasks.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
