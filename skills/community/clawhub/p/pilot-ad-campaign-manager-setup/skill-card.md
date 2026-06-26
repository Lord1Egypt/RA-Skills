## Description: <br>
Deploy an ad campaign management system with four agents that automate campaign strategy, creative production, real-time bidding, and performance analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure a four-agent advertising workflow for campaign planning, creative production, bid management, and performance reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Campaign reporting can send audience, spend, performance, or conversion data to Slack, webhooks, or external dashboards. <br>
Mitigation: Configure destinations deliberately, avoid raw audience or user-level data, and use test campaign data until reporting boundaries are confirmed. <br>
Risk: The setup depends on multiple pilot-* skills, including escrow and bridge components that affect trust, reporting, and spend workflows. <br>
Mitigation: Review the required dependencies before installation and establish handshakes only with intended peer agents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-ad-campaign-manager-setup) <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [Skill README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands and JSON manifest examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes role-specific setup manifests, peer handshakes, and dependency installation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
