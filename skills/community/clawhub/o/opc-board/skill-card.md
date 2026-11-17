## Description:

OPC Board uses five advisor perspectives to stress-test a solo project idea across logic, deliverability, growth, viability, and risk, then produces a scored Go/No-Go feasibility report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris1wang3](https://clawhub.ai/user/chris1wang3)

### License/Terms of Use:

MIT-0

## Use Case:

External users, solo founders, indie developers, and maintainers use this skill to evaluate one-person companies, side projects, SaaS ideas, and open-source project feasibility before committing effort. It collects project context, applies deterministic five-dimension scoring, and returns a decision-oriented feasibility report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The HTML report path can render user-provided content in a browser.

Mitigation: Prefer Markdown output, or escape placeholders, validate class/style/SVG values, and render HTML reports in a sandbox before opening reports built from untrusted input.

Risk: Users may over-rely on feasibility scoring for regulated or high-stakes business decisions.

Mitigation: Use the report as decision support only, preserve the skill's disclaimer, and require human review for legal, financial, medical, or compliance-sensitive ideas.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chris1wang3/skills/opc-board)
- [Deterministic scoring engine](artifact/references/scoring-engine-deterministic.md)
- [Markdown report template](artifact/references/report-template-markdown.md)
- [HTML professional report template](artifact/references/report-template-pro.html)
- [Advisor personas and phrasing](artifact/references/soul.md)
- [Intake form asset](artifact/assets/intake-form.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Guidance]

**Output Format:** [Markdown or HTML feasibility report with scored tables, advisor challenges, Go/Conditional/No-Go decision, OPC decision card, MoSCoW scope, Pre-Mortem risks, and action list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can use a reusable HTML intake form; prefer Markdown or sandboxed HTML rendering for untrusted input.]

## Skill Version(s):

1.4.2 (source: release evidence and artifact/claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
