## Description:

Tracks shipping transit data through the Strait of Hormuz from hormuzstraitmonitor.com and shipxy.com, then alerts when vessel count, throughput, or non-Iranian vessel exit thresholds indicate traffic recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laigen](https://clawhub.ai/user/laigen)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and operators use this skill to monitor Strait of Hormuz shipping activity and receive alerts when transit and throughput recovery thresholds are met.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime browser-driver download and Chrome automation may execute newly fetched driver software.

Mitigation: Run in an isolated virtual environment or container and pin the Selenium, webdriver-manager, Chrome, and ChromeDriver versions before deployment.

Risk: Chrome is launched with sandboxing disabled while visiting external websites.

Mitigation: Avoid running as root or with broad host filesystem access; use a constrained container or dedicated runtime account.

Risk: The skill writes monitoring and debug files under the OpenClaw workspace.

Mitigation: Review configured output paths and limit workspace permissions to the directories needed for CSV records and debug artifacts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laigen/skills/hormuz-strait-monitor)
- [hormuzstraitmonitor.com](https://hormuzstraitmonitor.com/)
- [shipxy.com Hormuz Page](https://www.shipxy.com/special/hormuz)
- [Configuration Reference](references/config.json)

## Skill Output:

**Output Type(s):** [Files, Text, Configuration, Shell commands]

**Output Format:** [CSV data file with textual alert messages and optional notification summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Appends timestamped transit metrics and alerts under ~/.openclaw/workspace/memory; notification channel is optional.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
