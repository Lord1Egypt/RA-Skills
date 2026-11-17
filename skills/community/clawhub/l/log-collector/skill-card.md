## Description:

Permanent log collection agent. Collects logs and history from all nodes via SSH/VPN every 3 hours. Stores in logs.db with 30-day retention. Multi-node capable with fallback logic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikikari](https://clawhub.ai/user/kikikari)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to collect system, application, VPN, and SSH status logs from multi-node OpenClaw clusters on a recurring schedule. It is intended for controlled environments where centralized log collection and retention are approved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring SSH collection can centralize sensitive system and application logs.

Mitigation: Run only in approved clusters, minimize or redact collected logs, and confirm retention controls before production use.

Risk: Unsafe SSH host-key verification and weak credential scoping can expose collection jobs to unauthorized hosts or broad credential use.

Mitigation: Require SSH host-key verification, dedicated least-privilege keys, and a node allowlist before enabling recurring collection.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown documentation with inline code blocks, shell commands, JSON configuration examples, and a Python log-collection script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime script writes collected log records to logs.db with 30-day retention and writes collection status logs under logs/log-collector.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
