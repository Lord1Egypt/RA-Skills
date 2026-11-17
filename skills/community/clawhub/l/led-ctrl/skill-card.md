## Description:

Control Raspberry Pi GPIO pins remotely by setting specified pins HIGH or LOW through RPC calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yevladimir](https://clawhub.ai/user/yevladimir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent request simple Raspberry Pi GPIO on/off actions for configured pins through a remote Pi control endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends unauthenticated plaintext hardware commands to a Raspberry Pi endpoint.

Mitigation: Use only on a trusted, isolated network with a Pi server that independently authenticates requests.

Risk: The local script does not enforce the documented action or pin limits before sending requests.

Mitigation: Enforce action and pin allowlists on the Pi server, reject malformed JSON, and run with least GPIO privilege.

Risk: Connected hardware such as relays or actuators may switch if the endpoint is reachable or traffic is modified.

Mitigation: Limit network exposure and review connected hardware impact before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yevladimir/skills/led-ctrl)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Text]

**Output Format:** [Shell command invocation that sends a JSON HTTP request and returns command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a reachable Raspberry Pi control endpoint and caller-supplied action and pin values.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
