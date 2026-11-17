## Description:

Monitor and control an OpenSprinkler irrigation controller, including status checks, manual station or program runs, rain delays, logs, queue pauses, and overall system operation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jnord3](https://clawhub.ai/user/jnord3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent monitor and operate a local OpenSprinkler irrigation controller through its HTTP API. It supports both diagnostic readouts and state-changing irrigation actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send authenticated commands that start or stop watering, disable operation, change delays, pause queues, or reboot the controller.

Mitigation: Use only on trusted local networks and require explicit user confirmation before state-changing or disruptive actions.

Risk: The controller is accessed over plaintext HTTP with a reusable password hash.

Mitigation: Use a strong unique OpenSprinkler password and isolate controller access from untrusted networks.

Risk: Weak bounds or guardrails on durations and identifiers can cause unintended irrigation behavior.

Mitigation: Validate station IDs, program IDs, durations, and delay values before invoking write or admin tools.

## Reference(s):

- [ClawHub OpenSprinkler skill page](https://clawhub.ai/jnord3/skills/opensprinkler)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [JSON tool results summarized in agent-facing text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses 1-based station and program IDs and requires OpenSprinkler IP address and password environment variables.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
