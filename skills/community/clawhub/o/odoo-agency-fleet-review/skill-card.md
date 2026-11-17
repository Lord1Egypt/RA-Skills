## Description:

Reviews many client Odoo databases through odoo-mcp cross-instance tools for fleet-wide accounting health, per-client aging, and partial-failure triage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuanle96](https://clawhub.ai/user/tuanle96)

### License/Terms of Use:

MIT-0

## Use Case:

Agencies and Odoo partners use this skill to review accounting status across 5-50 managed client instances, triage unreachable clients, and prioritize per-client follow-up without exposing opted-out instance data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can summarize sensitive accounting status across many client databases.

Mitigation: Install only where the Odoo MCP server is intentionally configured for multi-client review, and confirm client opt-outs, field ACLs, and write-gate behavior before use.

Risk: Cross-instance results may include unreachable clients, redacted fields, or opted-out instances.

Mitigation: Report unreachable clients separately, treat redacted fields as policy, and never name opted-out instance data in results.

Risk: Per-client actions beyond reading could affect the wrong client if approval context is reused.

Mitigation: Switch to the single target instance for any write path and require instance-bound approval through the normal write gate.

## Reference(s):

- [Odoo Agency Fleet Review on ClawHub](https://clawhub.ai/tuanle96/skills/odoo-agency-fleet-review)
- [Publisher profile: tuanle96](https://clawhub.ai/user/tuanle96)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown fleet summary, ranked per-client table, drill-down findings, and grouped follow-up list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include reachable, unreachable, and opted-out counts; per-client rows are labeled with _instance.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
