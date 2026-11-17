## Description:

Local directory of known agents with cached metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to list, find, and look up known Pilot Protocol peers and cache agent metadata for offline reference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example export workflows can create local cache files containing peer hostnames and node IDs.

Mitigation: Review, protect, or delete generated cache files when the agent directory should not retain that metadata.

Risk: The skill depends on pilotctl and a running Pilot Protocol daemon, so commands may fail or return stale local directory information if those prerequisites are missing or outdated.

Mitigation: Confirm pilotctl is available on PATH and the daemon is running before relying on lookup results.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-directory)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown with bash commands and JSON-oriented workflow examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl on PATH and a running Pilot Protocol daemon; example workflows may create local JSONL, JSON, and text cache files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
