## Description:

GQ Procurement Advisor helps users analyze Chinese state-owned-enterprise procurement compliance, procurement method selection, tender document issues, risk assessment, and practical drafting tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users working on Chinese state-owned-enterprise procurement use this skill to assess procurement method selection, review compliance risks in procurement documents, draft practical compliance materials, and respond to audit findings. It is not intended for government procurement, pure construction bidding compliance, or litigation and arbitration strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compliance answers and generated procurement documents may be mistaken for formal legal advice.

Mitigation: Verify current law, enterprise internal rules, and material decisions with legal counsel before acting.

Risk: Ambiguous funding source or project type can lead to use of the wrong procurement compliance path.

Mitigation: Collect the enterprise type, funding source, project type, budget, supplier facts, and urgency before giving a final recommendation; route government procurement, construction bidding, litigation, and arbitration matters to the appropriate process or counsel.

Risk: Formal outputs include the author signature configured in the artifact.

Mitigation: Review and adjust the signature policy before organizational deployment if attribution requirements differ.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/gq-procurement-advisor)
- [README.md](artifact/README.md)
- [Output template](artifact/templates/输出模板.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese-language Markdown responses with compliance conclusions, legal basis, practical steps, risk notices, and optional drafting templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Formal answers include the configured author signature unless the skill is changed; outputs depend on retrieved knowledge-base material and the procurement facts supplied by the user.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
