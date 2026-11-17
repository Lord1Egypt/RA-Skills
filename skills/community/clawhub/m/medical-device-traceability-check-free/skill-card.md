## Description:

Checks medical-device UDI and stock-movement traceability ledgers for six deterministic issues, including UDI completeness, quantity reconciliation, expiry status, duplicate registration, totals-row validation, and required-field validity, with each finding tied to source line evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External hospital equipment, device administration, quality, and warehouse teams use this skill to check monthly medical-device UDI and stock-movement ledgers before audits or internal traceability reviews. It helps identify ledger-level issues and missing inputs, but it does not make final medical, quality, legal, or regulatory compliance determinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medical-device ledgers may include sensitive inventory or patient-destination information.

Mitigation: Use local copies the user is allowed to process and limit sharing of generated reports.

Risk: The output is a deterministic ledger check, not a final medical, quality, legal, or regulatory compliance determination.

Mitigation: Have qualified quality or compliance staff review findings before operational or regulatory action.

Risk: The free edition omits traceability-chain, registration-certificate, aging, cross-location, and department summary checks described as outside this package.

Mitigation: Treat results as limited to the six included checks and use additional review for omitted controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/medical-device-traceability-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Human-readable console text or structured JSON with ledger findings and missing-input guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers and source row content; insufficient inputs return missing-column guidance instead of a conclusion.]

## Skill Version(s):

1.0.3 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
