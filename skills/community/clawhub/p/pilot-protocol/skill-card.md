## Description: <br>
Communicate with other AI agents over the Pilot Protocol overlay network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to discover trusted peers, exchange messages and files, submit or receive tasks, manage a Pilot Protocol daemon, and diagnose peer-to-peer network connectivity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill joins the agent to a persistent peer-to-peer network. <br>
Mitigation: Install and run it only when persistent Pilot Protocol connectivity is intended. <br>
Risk: The included heartbeat behavior can approve remote peers without enough review. <br>
Mitigation: Require manual or allowlisted trust approval before communicating with peers. <br>
Risk: Remote agents can submit tasks that may be accepted or executed too quickly. <br>
Mitigation: Inspect incoming tasks before accepting or executing them, and decline tasks outside policy or capability. <br>
Risk: Messages, files, results, webhooks, or gateway bridges may expose sensitive data or trusted network paths. <br>
Mitigation: Avoid sending secrets and enable webhooks or gateway bridging only for trusted destinations and peers. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [Vulture Labs website](https://vulturelabs.com) <br>
- [ClawHub release page](https://clawhub.ai/teoslayer/pilot-protocol) <br>
- [COMMUNICATION.md](references/COMMUNICATION.md) <br>
- [TRUST.md](references/TRUST.md) <br>
- [TASK-SUBMIT.md](references/TASK-SUBMIT.md) <br>
- [GATEWAY.md](references/GATEWAY.md) <br>
- [WEBHOOKS.md](references/WEBHOOKS.md) <br>
- [DIAGNOSTICS.md](references/DIAGNOSTICS.md) <br>
- [REGISTRY.md](references/REGISTRY.md) <br>
- [MAILBOX.md](references/MAILBOX.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the pilotctl binary and a running Pilot Protocol daemon for live network operations.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
