## Description:

A local checker for industry-specific worksheets that runs 14 built-in checks per organization directory and prints one conclusion line per organization, with findings citing the source file and line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations staff at hospitals, clinics, schools, training providers, restaurants, hotels, logistics or export organizations, utilities, and bank financing teams use this skill before close, settlement, reconciliation, or reporting. It checks each organization folder against built-in industry worksheet rules and returns one conclusion line per organization with cited evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local institution materials supplied by the user.

Mitigation: Run it only on materials the operator is authorized to process, and keep sensitive input directories within the intended local environment.

Risk: Outputs can be mistaken for audit, pricing, reimbursement, policy, or legal conclusions.

Mitigation: Treat outputs as reconciliation aids with source citations, and require domain review before using findings for operational, audit, or compliance decisions.

Risk: The maintenance script can rewrite package engine files when used outside the documented checking workflow.

Mitigation: Use the documented node scripts/run.mjs commands for normal operation, and reserve rebuild_free.py for package maintainers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/industry-vertical-pack-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)
- [Skill documentation](artifact/SKILL.md)
- [Runner script](artifact/scripts/run.mjs)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Console text or JSON from the documented Node runner, with Markdown documentation and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite organization, check, source file, and line. During documented use, the skill reads local materials and writes results to stdout rather than modifying files.]

## Skill Version(s):

1.0.25 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
