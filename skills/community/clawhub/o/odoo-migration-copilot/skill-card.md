## Description:

Plan and de-risk an Odoo version upgrade (16->17->18->19/20) using odoo-mcp's migration workbench: audit custom addons, classify upgrade-log failures into a worklist, resolve model renames, and preview JSON-2 payloads for the XML-RPC sunset.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuanle96](https://clawhub.ai/user/tuanle96)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and migration engineers use this skill to plan Odoo version upgrades, convert source scans and rehearsal logs into an evidence-backed worklist, and assess readiness for integration changes such as JSON-2 migration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on odoo-mcp being connected to the intended Odoo project and addon paths.

Mitigation: Install it only in the intended migration environment and keep ODOO_ADDONS_PATHS limited to the addons that should be reviewed.

Risk: Migration rehearsal fixes or data corrections could affect production data if applied in the wrong environment.

Mitigation: Use staging databases for rehearsals, avoid production edits during rehearsal, and review gated data fixes before applying them.

Risk: Incomplete upgrade logs can lead to unsupported conclusions about migration failures.

Mitigation: Require the relevant log slice and produce worklist entries with evidence lines and suggested fixes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tuanle96/skills/odoo-migration-copilot)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with phase-status headers, worklist tables, and go/no-go recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Worklist rows include action, category, evidence, suggested fix, and status; recommendations include the open needs_script count.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
