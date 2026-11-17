## Description:

Watch and control running processes in real time. Use when scanning active PIDs, monitoring resource spikes, reporting trees, alerting on crashes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, administrators, and support engineers use Procmon to inspect running processes, monitor resource spikes, identify zombie processes, view process trees, inspect listening ports, and log matching process statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The log command can append data outside the intended log folder when given process names containing pathname characters.

Mitigation: Use trusted process names only, avoid slashes and dot-dot path components, and add name validation plus symlink refusal before allowing untrusted input.

Risk: Process and port inspection can expose local runtime information.

Mitigation: Run the skill only in environments where the agent is allowed to inspect local process state and listening ports.

## Reference(s):

- [ClawHub Procmon skill page](https://clawhub.ai/bytesagain3/skills/procmon)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Plain text terminal output and append-only log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local process and listening-port state; the log command appends matching process statistics under ~/.procmon.]

## Skill Version(s):

3.0.0 (source: server release metadata, SKILL.md frontmatter, and script VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
