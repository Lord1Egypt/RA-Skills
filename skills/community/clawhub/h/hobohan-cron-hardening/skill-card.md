## Description: <br>
Guidelines for reliable OpenClaw cron jobs: model pinning, absolute paths, timeouts, delivery config, and error recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hohobohan](https://clawhub.ai/user/hohobohan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure reliable OpenClaw scheduled jobs, including model pinning, absolute paths, timeout choices, delivery settings, concurrency limits, and recovery checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hardcoded Telegram recipient values could send cron output or failure alerts to the wrong recipient. <br>
Mitigation: Replace every hardcoded Telegram recipient with the intended channel before enabling delivery or failure alerts. <br>
Risk: Personal absolute filesystem paths could fail or cause scheduled jobs to operate on the wrong files when reused. <br>
Mitigation: Replace personal paths with environment-specific absolute paths and verify each command before installing or updating crons. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hohobohan/hobohan-cron-hardening) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands] <br>
**Output Format:** [Markdown with JSON and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes timeout guidance, delivery settings, failure alerts, and recovery checks for cron jobs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
