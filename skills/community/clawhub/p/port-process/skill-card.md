## Description:

Port Process helps agents and developers find processes bound to local ports, list active ports, and terminate selected processes on macOS and Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wang-junjian](https://clawhub.ai/user/wang-junjian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill while debugging local services, automation scripts, and port conflicts to identify which process owns a port and decide whether to terminate it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Terminating the wrong process can interrupt unrelated local services.

Mitigation: Run the find or dry-run flow first and verify the port, PID, user, and command before approving termination.

Risk: Forceful process termination can cause data loss or service disruption, especially on shared or production systems.

Mitigation: Prefer the safe SIGTERM flow, save work before terminating stateful processes, and avoid using the skill on shared or production hosts unless authorized.

Risk: Using elevated privileges can terminate processes outside the current user's normal control.

Mitigation: Avoid sudo unless the target process is understood and the operator has explicit permission to manage it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wang-junjian/skills/port-process)
- [Publisher profile](https://clawhub.ai/user/wang-junjian)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON output from bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include process identifiers, usernames, commands, ports, protocols, and termination recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
