## Description: <br>
Enables an agent to operate Simple Analytics through an OOMOL-connected account using the oo CLI for reading analytics data and sending confirmed events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Simple Analytics websites, retrieve aggregated stats, export raw data points, and send confirmed server-side events through their connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a connected Simple Analytics account through OOMOL-managed credentials. <br>
Mitigation: Before installing, confirm that the requested Simple Analytics access and OOMOL connection match the intended account and use. <br>
Risk: The send_event action can create server-side events or pageviews in Simple Analytics. <br>
Mitigation: Confirm the exact payload and intended effect with the user before running write actions. <br>
Risk: The security evidence reports clean scanner signals but notes limited confirmation of exact permissions or behavior. <br>
Mitigation: Review the skill description and requested access before deployment, especially in environments with strict analytics or credential controls. <br>


## Reference(s): <br>
- [ClawHub Simple Analytics Skill](https://clawhub.ai/oomol/oo-simple-analytics) <br>
- [Simple Analytics Homepage](https://simpleanalytics.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>
- [OOMOL Simple Analytics Connection](https://console.oomol.com/app-connections?provider=simple_analytics) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the oo CLI to inspect live connector schemas before building action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
