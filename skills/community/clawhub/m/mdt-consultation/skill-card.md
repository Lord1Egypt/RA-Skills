## Description:

MDT Consultation coordinates multiple specialist agents in parallel to review complex work, then synthesizes their findings into a structured consultation report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luaqnyin](https://clawhub.ai/user/luaqnyin)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to organize multi-perspective reviews of contracts, official documents, brand campaigns, strategic decisions, technical plans, and medical or health-related proposals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive consultation reports may be retained locally after reviews.

Mitigation: Require explicit user consent before saving reports, and keep retained summaries redacted, scoped, and deletable.

Risk: The skill can direct changes to skill or agent instruction files.

Mitigation: Disable automatic edits to SKILL.md and SOUL.md unless a human reviewer approves the change.

Risk: Multi-agent sharing can expose confidential legal, medical, contract, or business-strategy material to more agents than intended.

Mitigation: Use the skill only where multi-agent sharing is acceptable, and limit or redact sensitive inputs before consultation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luaqnyin/skills/mdt-consultation)
- [Consultation Guide](references/consultation-guide.md)
- [Evaluation Criteria](references/eval.md)
- [Consultation Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown consultation reports with structured findings, risk levels, and action recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include specialist-agent summaries, consensus points, disagreements, host judgment, and quality scoring.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
