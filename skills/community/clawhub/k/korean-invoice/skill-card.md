## Description:

Generates Korean-style quotes and tax invoices with business registration fields and automatic VAT calculations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:

MIT

## Use Case:

External users, business operators, and agents use this skill to create Korean quotes or tax invoices, manage client and item records, and produce HTML or PDF files for review and delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe HTML/PDF rendering can expose users to problems if untrusted parties control invoice fields such as client names, item names, notes, or dates.

Mitigation: Use only trusted invoice data until HTML escaping and output-path validation are fixed.

Risk: Client, item, business profile, and generated invoice data may contain sensitive business information.

Mitigation: Protect data/*.json and output files, and avoid placing the skill directory in shared or synced repositories.

Risk: The release has a suspicious security verdict and depends on maintained runtime packages.

Mitigation: Review before installing, keep dependencies updated, and run the skill only in a trusted local environment.

## Reference(s):

- [Korean Invoice Skill Page](https://clawhub.ai/mupengi-bot/skills/korean-invoice)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration]

**Output Format:** [HTML and PDF files, with command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores client, item, and business profile data in local JSON files and writes generated documents under an output directory.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
