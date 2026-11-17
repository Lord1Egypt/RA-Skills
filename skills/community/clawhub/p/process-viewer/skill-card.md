## Description:

Process Viewer helps agents record local process observations, monitoring notes, alerts, benchmarks, reports, and exports through a Bash command-line logbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, system administrators, and operations teams can use this skill to keep a local plaintext record of process scans, monitoring observations, alerts, fixes, benchmark results, and health-review notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext local logs may expose sensitive operational details if users enter secrets, customer data, or infrastructure details.

Mitigation: Do not enter passwords, tokens, customer data, or sensitive infrastructure details; review logs before sharing.

Risk: Exported JSON, CSV, or TXT files may contain sensitive logged data or behave unexpectedly when opened in spreadsheet tools.

Mitigation: Treat exported files as untrusted data, inspect them before sharing, and sanitize records before opening them in downstream tools.

Risk: Some logging commands may fail because Bash local declarations appear outside functions.

Mitigation: Validate the script in a non-production shell before relying on it for operational records.

## Reference(s):

- [Process Viewer ClawHub Skill Page](https://clawhub.ai/ckchzh/skills/process-viewer)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; command output is stdout text and optional JSON, CSV, or TXT export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes plaintext log entries under the local process-viewer data directory and can export collected entries.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
