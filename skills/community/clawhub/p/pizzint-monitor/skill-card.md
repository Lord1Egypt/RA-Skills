## Description:

PizzINT Monitor gathers public PizzINT signals and formats a geopolitical OSINT-style status report with NEH, DOUGHCON, pizza shop activity, PolyPulse, Polymarket, and OSINT summary sections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kai157isme-lgtm](https://clawhub.ai/user/kai157isme-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to collect or parse public PizzINT data and produce a concise geopolitical monitoring report. It is intended for informal OSINT correlation and should not be used as authoritative intelligence, investment advice, or a basis for operational decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated threat report may be mistaken for authoritative intelligence or decision guidance.

Mitigation: Treat the report as informal OSINT correlation and verify findings against primary sources before making financial, operational, or safety decisions.

Risk: Real-time data collection can fail or be incomplete because pizzint.watch is client-side rendered.

Mitigation: Use a browser-based capture path when current data is required and report unavailable values explicitly instead of inferring them.

Risk: Broad geopolitical trigger terms and risk labels may overstate weak correlations.

Mitigation: Preserve the skill's logic checks, keep threshold statements tied to observed values, and disclose correlation-versus-causation limits in the report.

## Reference(s):

- [PizzINT live data source](https://pizzint.watch/)
- [ClawHub skill release page](https://clawhub.ai/kai157isme-lgtm/skills/pizzint-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with tables, status summaries, source notes, and logic validation warnings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are primarily Chinese-language and may include geopolitical risk labels, threshold checks, browser-captured data notes, and warnings when live data cannot be retrieved.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
