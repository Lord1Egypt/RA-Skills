## Description:

Checks hotel night-audit and room-revenue tables by recalculating line items, totals, duplicates, blanks, and negative amounts, with each finding citing source text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Hotel finance, cashier, and night-audit staff use this skill to check hotel night-audit and room-fee income tables during closing, reconciliation, and inventory workflows. It performs the free edition's deterministic checks and identifies missing evidence instead of producing conclusions when the input is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker handles hotel revenue data locally but may still process sensitive operational or financial records.

Mitigation: Run it only in an approved local environment and provide only the table data needed for the night-audit checks.

Risk: The skill is not a substitute for accounting policy review or reconciliation against source systems.

Mitigation: Treat findings as deterministic table checks and confirm final accounting decisions against hotel policy, PMS/POS exports, bank records, and authorized reconciliation procedures.

Risk: The free edition omits several additional checks listed by the artifact, including reference-tolerance, available-night, ADR-range, free-room-ratio, and channel-order comparisons.

Mitigation: Review the listed withheld checks before relying on a clean result, and use additional reconciliation steps when those checks matter.

Risk: The output and help text are mostly Chinese, which can lead to misinterpretation by reviewers who do not read Chinese.

Mitigation: Have a Chinese-reading reviewer confirm the reported findings, missing inputs, and withheld-check notes before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/hotel-night-audit-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)
- [Skill definition](artifact/SKILL.md)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Human-readable console text or structured JSON result object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally through a Node.js command-line checker and reports executed checks, withheld free-edition checks, missing inputs, and cited findings.]

## Skill Version(s):

1.0.48 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
