## Description: <br>
Bridge GitHub webhook events as Pilot Protocol events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Pilot agents to receive GitHub webhook events and trigger agent actions from repository activity such as pushes and pull requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook-driven workflows can trigger agent actions from repository events. <br>
Mitigation: Review webhook relay configuration, GitHub event filters, and generated pilotctl commands before enabling automated actions. <br>
Risk: The skill depends on local prerequisites such as pilotctl, a running Pilot daemon, GitHub webhooks, gh CLI, and an HTTP relay server. <br>
Mitigation: Confirm the required binaries and services are installed and running before using the workflow. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub release page](https://clawhub.ai/teoslayer/pilot-github-bridge) <br>
- [Publisher profile](https://clawhub.ai/user/teoslayer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes pilotctl command examples and a webhook relay workflow example.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
