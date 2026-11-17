## Description:

Process Manage lets an agent list, search, inspect, and terminate local operating-system processes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moxin1044](https://clawhub.ai/user/moxin1044)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect local process state, find processes by name or command line, view detailed process metadata, and terminate selected processes when maintaining a workstation or runtime environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can terminate local processes, including forcefully by PID.

Mitigation: Use it from a least-privileged account, avoid administrator/root execution unless required, and manually verify the PID before kill actions.

Risk: Name-based termination can affect multiple matching processes without a separate confirmation step.

Mitigation: Prefer PID-based termination and use find or info actions first to narrow targets before kill_name.

Risk: Forceful termination can cause unsaved data loss or local system instability.

Mitigation: Try graceful termination first and reserve force:true for known, non-critical processes.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text process tables, detail reports, error messages, and termination status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include process identifiers, usernames, command lines, paths, resource usage, and termination results.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
