## Description:

Token Usage Tracker provides OpenClaw utilities for per-call token logging, alerts, timestamp normalization, and context summarization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gerhardvr26](https://clawhub.ai/user/gerhardvr26)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to add transparent token accounting, alerts, timestamp normalization, and optional context summarization to OpenClaw message workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Log maintenance utilities can rewrite local JSONL token logs and may be unsafe in directories writable by other users.

Mitigation: Review the scripts, use a private trusted log directory, and avoid running migration or dedupe utilities as root unless temporary-file handling is hardened.

Risk: The systemd unit is an example template with placeholder user and paths.

Mitigation: Customize the user and paths and review the unit before enabling any service.

## Reference(s):

- [Systemd token-interceptor service template](references/systemd/token-interceptor.service.txt)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; utility scripts produce JSONL logs and terminal text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Token logs are written locally as JSONL using the configured timezone and log folder.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
