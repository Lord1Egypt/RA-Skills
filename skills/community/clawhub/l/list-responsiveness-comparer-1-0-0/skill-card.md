## Description:

Compares tender or procurement requirement lists against bid-response lists item by item, quantity by quantity, and parameter by parameter, flagging differences without making legal or disqualification decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement reviewers, bid teams, and compliance staff use this skill to compare tender or procurement checklists with bid-response checklists, surface missing, extra, inconsistent, or arithmetically incorrect items, and prepare a structured review report. It is designed to support human review committees rather than replace their legal or procurement judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes tender and bid-response lists that may contain sensitive procurement or bidder information.

Mitigation: Use it only when sharing those lists with the agent and declared knowledge-base connector is acceptable under the applicable procurement process.

Risk: Red, yellow, and blue findings could be mistaken for final legal or bid-disqualification decisions.

Mitigation: Treat the findings as comparison support only and leave substantive responsiveness or disqualification decisions to the responsible review body.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/list-responsiveness-comparer-1-0-0)
- [Artifact README](artifact/README.md)
- [Artifact manifest](artifact/manifest.yaml)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [Structured Markdown comparison report with a JSON diff_items handoff object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses red, yellow, and blue severity labels; reports may be batched for lists over 200 items.]

## Skill Version(s):

1.0.0 (source: manifest.yaml, artifact/_meta.json, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
