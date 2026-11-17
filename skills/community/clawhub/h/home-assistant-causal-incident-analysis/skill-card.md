## Description:

Trace Home Assistant incidents by correlating automations, logbook attribution, entity history, and device registry records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextaltair](https://clawhub.ai/user/nextaltair)

### License/Terms of Use:

MIT-0

## Use Case:

External Home Assistant users and support engineers use this skill to investigate unexpected device state changes by building a narrow, evidence-ranked causal chain from automations, logbook context, entity history, and registry data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incident reports may expose sensitive Home Assistant data such as bearer tokens, MAC addresses, registry identifiers, or unrelated household configuration.

Mitigation: Keep analysis scoped to the incident and redact sensitive identifiers and unrelated configuration before sharing the report.

Risk: Causal conclusions may be overstated when Home Assistant recorder data lacks decisive measurements or when telemetry semantics are ambiguous.

Mitigation: Label direct, indirect, and speculative evidence separately, preserve gaps and polling delays, and name the smallest additional measurement needed to distinguish alternatives.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nextaltair/skills/home-assistant-causal-incident-analysis)
- [ClawHub publisher profile](https://clawhub.ai/user/nextaltair)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown narrative with evidence levels, alternatives, missing evidence, and recommended measurements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code or shell commands are produced by the skill itself.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
