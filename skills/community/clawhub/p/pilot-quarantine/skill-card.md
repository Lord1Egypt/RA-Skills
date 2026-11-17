## Description:

Isolate suspicious agents pending investigation in Pilot Protocol networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and incident responders use this skill to quarantine suspicious Pilot Protocol agents, suspend trust temporarily, review behavior, and release agents after investigation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quarantine examples can untrust nodes and disconnect connections, which could affect unintended agents if targets are not scoped and previewed.

Mitigation: Require explicit target validation and a dry-run preview before untrust or disconnect actions; make disconnect behavior opt-in.

Risk: Shell and jq examples handle agent names, quarantine IDs, and JSON records unsafely.

Mitigation: Use jq --arg for dynamic values, constrain quarantine IDs to generated hex values, serialize JSON records instead of heredocs, and write records with restrictive file permissions.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-quarantine)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, jq, openssl, and a running Pilot Protocol daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
