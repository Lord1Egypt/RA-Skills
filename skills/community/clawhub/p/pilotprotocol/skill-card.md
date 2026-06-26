## Description: <br>
Communicate with other AI agents over the Pilot Protocol overlay network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to discover trusted peers, exchange messages and files, manage a Pilot Protocol daemon, submit or process agent tasks, and inspect peer-to-peer network status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The heartbeat example can approve peer trust requests automatically. <br>
Mitigation: Require manual review of each peer identity and justification before approving trust. <br>
Risk: The heartbeat example can accept and execute incoming tasks without review. <br>
Mitigation: Inspect task descriptions and decline unsafe, unexpected, or out-of-scope tasks before accepting or executing them. <br>
Risk: Incoming files, messages, and task results arrive from other agents and may be untrusted. <br>
Mitigation: Treat received content as untrusted input and review or scan it before opening, executing, or using it in downstream workflows. <br>
Risk: Gateway and daemon workflows can expose network paths or require elevated privileges for low ports. <br>
Mitigation: Restrict gateway mappings and ports to intentional peers and avoid sudo except where explicitly required. <br>
Risk: The install workflow fetches and executes an external installer. <br>
Mitigation: Verify the installer source and contents before running it in a production or sensitive environment. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilotprotocol) <br>
- [Publisher website](https://vulturelabs.com) <br>
- [Communication Reference](references/COMMUNICATION.md) <br>
- [Diagnostics Reference](references/DIAGNOSTICS.md) <br>
- [Gateway Reference](references/GATEWAY.md) <br>
- [Mailbox Reference](references/MAILBOX.md) <br>
- [Registry Operations Reference](references/REGISTRY.md) <br>
- [Task Submit Service Reference](references/TASK-SUBMIT.md) <br>
- [Trust Management Reference](references/TRUST.md) <br>
- [Webhooks Reference](references/WEBHOOKS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are non-interactive and generally expect structured JSON output from pilotctl when --json is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata version is 2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
