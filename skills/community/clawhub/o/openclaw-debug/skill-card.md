## Description: <br>
When users encounter OpenClaw-related issues or errors, the skill guides an agent to check official OpenClaw documentation and GitHub issues before recommending fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skyan](https://clawhub.ai/user/skyan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and support agents use this skill to diagnose OpenClaw issues, check whether problems are known or fixed, and provide version, configuration, workaround, or upgrade guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Troubleshooting notes or logs may contain secrets, tokens, or sensitive operational details. <br>
Mitigation: Avoid pasting secrets, tokens, or sensitive logs into troubleshooting notes. <br>
Risk: The skill may suggest recording todo entries or reminders for follow-up on known bugs. <br>
Mitigation: Confirm the user's intent before creating follow-up reminders or todo entries. <br>
Risk: Version-specific fix guidance can become stale if OpenClaw documentation, issues, or changelog entries change. <br>
Mitigation: Verify recommendations against official OpenClaw documentation, GitHub issues, and the changelog before presenting final upgrade or workaround guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skyan/openclaw-debug) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw GitHub issues](https://github.com/openclaw/openclaw/issues?q=is%3Aissue) <br>
- [OpenClaw changelog](https://raw.githubusercontent.com/openclaw/openclaw/main/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline command and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include issue links, fix status, workaround steps, and upgrade recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
