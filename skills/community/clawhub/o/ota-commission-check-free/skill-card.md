## Description:

Checks hotel OTA settlement tables for commission, net settlement, totals, duplicate channels, and blank or placeholder fields, with findings tied to source line numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Hotel and short-term rental operators use this skill to review monthly OTA settlement tables from channels such as Ctrip, Meituan, and Fliggy. It recalculates commission and net settlement amounts, checks column totals, and flags duplicate or incomplete channel rows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free tier omits several anomaly checks, including out-of-range commission rates, negative or excessive net settlement, negative other fees, and high combined fee ratio checks.

Mitigation: Review the omitted-check list in the output and perform those checks separately before relying on the result for final settlement decisions.

Risk: The skill does not validate OTA contract terms, undisclosed deductions, tax treatment, or channel-specific settlement rules.

Mitigation: Compare flagged results and clean results against the applicable channel contract, invoice records, and any separate deduction reports.

Risk: Poorly formatted or incomplete settlement-table input can prevent the skill from reaching a conclusion.

Mitigation: Provide a table that includes recognizable headers for channel, room revenue, commission rate, commission, other fees, and net settlement; treat insufficient-input output as no conclusion.

Risk: The skill runs a local Node.js script on settlement-table text supplied by the user.

Mitigation: Run it in a controlled workspace and inspect the included artifact files before use, consistent with the clean security scan guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/ota-commission-check-free)
- [Artifact skill definition](artifact/SKILL.md)
- [Sample input](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable terminal text or JSON result objects with findings, summaries, executed checks, omitted checks, and source line references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library code; accepts JSON or pasted settlement-table text and returns insufficient-input status instead of conclusions when required table fields are missing.]

## Skill Version(s):

1.0.31 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
