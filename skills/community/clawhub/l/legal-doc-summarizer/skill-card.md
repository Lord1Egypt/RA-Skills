## Description:

Reads contracts, NDAs, terms of service, employment agreements, leases, and SaaS MSAs to produce structured plain-language summaries with risk flags, clause explanations, market-norm comparisons, and redline checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users use this skill to understand legal documents before negotiation or legal review. It summarizes obligations, flags clauses that may need pushback, and explains when to escalate to licensed counsel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on generic wording when a user did not intend to invoke contract review.

Mitigation: Use contract-specific prompts and confirm the intended document type before relying on the summary.

Risk: Users may mistake summaries for legal advice in high-value, regulated, or jurisdiction-specific matters.

Mitigation: Treat the output as general information and route high-stakes or jurisdiction-specific documents to licensed counsel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/legal-doc-summarizer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown summary with risk flags, market deviations, redline checklist, and escalation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides general legal information only and is not a substitute for licensed counsel.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
