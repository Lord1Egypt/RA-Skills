## Description:

Use when diagnosing KWDB incidents from logs, metrics, or system evidence, especially crashes, OOM, slow SQL, restarts, and cluster-wide availability symptoms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kwdb](https://clawhub.ai/user/kwdb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support engineers use this skill to diagnose KWDB incidents from logs, metrics, system evidence, SQL evidence, and optional source-code context. It focuses on time anchoring, evidence triage, fault localization, and concise Chinese diagnostic reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Performance diagnosis may ask an agent to run EXPLAIN ANALYZE on supplied SQL, which can affect a live database.

Mitigation: Use the skill only for authorized KWDB diagnostics; require operator approval and run SQL analysis against a safe target such as a read-only staging system or replica with timeouts and resource limits.

Risk: The skill can guide agents toward shell commands that inspect logs, system evidence, process arguments, and source repositories.

Mitigation: Limit use to authorized environments and provide only evidence paths or tool access that the operator is permitted to inspect.

## Reference(s):

- [KWDB Troubleshooting on ClawHub](https://clawhub.ai/kwdb/skills/kwdb-troubleshooting)
- [KWDB source repository reference](https://gitee.com/kwdb/kwdb)
- [Key Rules](references/key-rules.md)
- [Intake Gate](references/intake-gate.md)
- [Path Discovery](references/path-discovery.md)
- [Triage Playbook](references/triage-playbook.md)
- [Fault Localization Chain](references/fault-localization.md)
- [Evidence Rules](references/evidence-rules.md)
- [Output Modes](references/output-modes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese Markdown diagnostic report with targeted command snippets when evidence collection or localization requires them]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Diagnosis-only output; unknown fields are marked as pending rather than guessed.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
