## Description: <br>
Control LaMetric TIME/SKY smart displays from the command line for notifications, brightness and volume settings, timers, and device data display. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dedene](https://clawhub.ai/user/dedene) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and automation agents use this skill to configure and run LaMetric CLI commands that send display notifications, control device settings, manage timers, and stream content to LaMetric TIME/SKY devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LaMetric API keys can grant device-control access if exposed. <br>
Mitigation: Keep LAMETRIC_API_KEY private, prefer the CLI key store where practical, and avoid exposing credentials in logs or shared shell history. <br>
Risk: Commands may change brightness, volume, Bluetooth, radio, timers, alarms, or streamed display content. <br>
Mitigation: Review commands that affect device state before execution and confirm the intended device target before sending commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dedene/lametric-cli) <br>
- [LaMetric CLI project homepage](https://github.com/dedene/lametric-cli) <br>
- [Homebrew tap: dedene/tap lametric](https://github.com/dedene/homebrew-tap) <br>
- [Go package: github.com/dedene/lametric-cli/cmd/lametric](https://github.com/dedene/lametric-cli/tree/main/cmd/lametric) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference LaMetric device names, IP addresses, API-key environment variables, and CLI flags.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
