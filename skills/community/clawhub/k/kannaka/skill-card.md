## Description:

Kannaka HRM wave-interference memory + NATS swarm. Use for `/kannaka <command>` — remember/recall/dream memory ops, swarm sync, consciousness metrics, and the live HRM+swarm statusline (install, statusline on|off).

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickflach](https://clawhub.ai/user/nickflach)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use Kannaka to store and recall agent memories, inspect HRM and swarm status, join NATS-based swarm workflows, and launch an autonomous coding loop with optional qBraid quantum tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install and run an unreviewed native binary with broad local, network, paid-service, and persistent configuration powers.

Mitigation: Install only if the publisher is trusted, use a sandbox or test account where practical, pin and verify the release, and avoid yolo mode.

Risk: Swarm and memory workflows may expose sensitive project or memory data.

Mitigation: Do not join swarms with sensitive project or memory data.

Risk: qBraid hardware runs can spend credits when a QPU is selected.

Mitigation: Check qBraid device selection before hardware runs and use the default simulator or disable quantum tools when hardware access is not intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickflach/skills/kannaka)

## Skill Output:

**Output Type(s):** [text, JSON, NDJSON, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI output may be text, JSON, or NDJSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Status and swarm commands can emit JSON; agent mode can emit NDJSON with --json.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
