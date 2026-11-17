## Description:

Generates periodic pharmaceutical intelligence briefs for drugs, therapeutic areas, or technology modalities by summarizing R&D, clinical, regulatory, deal, news, and competitive developments within a strict time window.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Pharmaceutical intelligence and strategy teams use this skill to monitor defined drugs, targets, indications, modalities, organizations, and competitors over an explicit date range. It produces source-traceable briefs that separate factual events from competitive interpretation and disclose retrieval coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted source links in generated HTML reports may execute browser content.

Mitigation: Generate reports from trusted data, review or patch URL escaping and safe-scheme validation, and open reports in an isolated context before hosting them in authenticated internal environments.

Risk: Pharmaceutical brief content may be mistaken for legal, medical, or unsupported business conclusions.

Mitigation: Treat patent entries as signals rather than FTO conclusions, do not use clinical entries as medical advice, label commercial implications as inference, and link each insight to event or source IDs.

## Reference(s):

- [Drug type mapping](artifact/references/drug_type_mapping.md)
- [Legacy pharmaceutical intelligence module contracts](artifact/references/legacy-module-contracts.md)
- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/pharma-intelligence-brief)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Files, Guidance]

**Output Format:** [Validated JSON data and rendered HTML report, with concise source-backed narrative sections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses explicit date windows, module coverage reporting, event deduplication, source IDs, and unresolved-field placeholders instead of fabricated values.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
