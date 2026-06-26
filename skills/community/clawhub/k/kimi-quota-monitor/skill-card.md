## Description: <br>
Kimi Quota Monitor helps agents check Kimi membership quota usage, calculate monthly quota cycle status, and configure daily WeChat reports through OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawntribbiani](https://clawhub.ai/user/shawntribbiani) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers who use Kimi Chat can use this skill to monitor quota consumption, calculate reset-cycle status, and set up recurring quota reports to WeChat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires live Kimi session cookies and localStorage tokens that may be stored in plaintext. <br>
Mitigation: Use only on a trusted machine, keep credential files out of source control and backups, restrict file permissions, and rotate or revoke Kimi credentials if exposure is possible. <br>
Risk: The skill can send recurring quota reports through WeChat when scheduled with cron. <br>
Mitigation: Verify the OpenClaw WeChat target ID before use and enable scheduled reporting only when daily background messages are intentional. <br>


## Reference(s): <br>
- [Quota Rules Reference](artifact/quota_rules.md) <br>
- [Kimi Subscription Page](https://www.kimi.com/membership/subscription) <br>
- [ClawHub Release Page](https://clawhub.ai/shawntribbiani/kimi-quota-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration examples; runtime reports are text messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Kimi cookies, localStorage tokens, Chrome or Chromium, Playwright, and OpenClaw WeChat configuration before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
