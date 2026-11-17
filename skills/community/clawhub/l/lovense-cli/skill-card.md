## Description:

Control Lovense toys (Lush, Hush, Nora, Solace, ...) over the local network from the shell.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2b-jr26](https://clawhub.ai/user/2b-jr26)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent issue local-network shell commands for Lovense toy discovery, vibration, patterns, raw actions, and immediate stop actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install flow fetches executable Python code from a mutable GitHub branch.

Mitigation: Audit the referenced script and pin it to a fixed commit or verified digest before use.

Risk: The skill can control physical devices and may affect someone wearing the device.

Mitigation: Require explicit consent, keep sessions opt-in, prefer bounded durations, and send the stop command immediately on any stop request.

## Reference(s):

- [Server-resolved source repository](https://github.com/2b-jr26/lovense-cli)
- [ClawHub skill page](https://clawhub.ai/2b-jr26/skills/lovense-cli)
- [Referenced executable download](https://raw.githubusercontent.com/2b-jr26/lovense-cli/main/lovense.py)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local IP and port placeholders, strength and duration values, preset names, custom pattern steps, and stop commands.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
