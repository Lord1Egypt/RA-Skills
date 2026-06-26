## Description: <br>
Deploy an automated code review pipeline with three agents that scan pull requests, analyze code quality, and report review results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to configure a three-agent pull request review workflow with scanner, reviewer, and reporter roles. It helps set up required skills, hostnames, manifests, handshakes, subscriptions, and reporting flows for automated code review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub, Slack, webhook, and PR reporting can disclose sensitive repository or vulnerability details outside the intended audience. <br>
Mitigation: Use restricted GitHub and Slack credentials, send notifications only to approved channels or webhooks, and avoid forwarding raw vulnerability details from private repositories unless organizational policy allows it. <br>
Risk: The setup depends on bridge skills and the pilotctl binary that can route review data between agents and external services. <br>
Mitigation: Confirm dependent Pilot bridge skills, the pilotctl binary, and the clawhub binary are from trusted sources before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-code-review-pipeline-setup) <br>
- [Publisher profile](https://clawhub.ai/user/teoslayer) <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces role-specific setup guidance for scanner, reviewer, and reporter agents, including manifests, handshakes, subscriptions, and publish examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
