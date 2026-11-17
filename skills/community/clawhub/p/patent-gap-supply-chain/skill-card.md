## Description:

Infers likely supplier, customer, or technology-licensing relationships from patent gaps through trade-secret checks, multi-lead verification, negative verification, patent quality scoring, evidence freshness tracking, and financial cross-validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianzhiceng297-boop](https://clawhub.ai/user/tianzhiceng297-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and agents use this skill to research patent gaps, supplier or customer relationships, technology dependencies, and competitive supply-chain signals in hardware, manufacturing, pharma, materials, and related industries. It is designed to produce confidence-scored inference reports rather than definitive legal, procurement, or investment conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent-gap and supply-chain inferences can be wrong or stale.

Mitigation: Review the skill's confidence ratings, evidence timestamps, negative verification results, and financial corroboration before relying on a conclusion.

Risk: A patent gap can reflect trade-secret protection, normal component procurement, or an ODM business model rather than a supplier dependency.

Mitigation: Run the documented applicability check, trade-secret assessment, alternative-hypothesis checklist, and industry-specific guide before treating a patent gap as dependency evidence.

Risk: The workflow may be misused as a general company research or investment-decision assistant.

Mitigation: Use it only for the specialized public-source competitive-intelligence workflow described by the release evidence, and keep final business or investment decisions under human review.

## Reference(s):

- [Detailed Workflow](references/workflow.md)
- [Checklists and Confidence Rules](references/checklists.md)
- [Industry-Specific Patent and Trade Secret Guide](references/industry-guide.md)
- [Sample Output](examples/sample-output.md)
- [Real Case Study](examples/real-case.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown supply-chain inference report with confidence tables and follow-up recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes evidence timestamps, confidence levels, patent quality scores, negative verification results, financial corroboration, and alternative-hypothesis checks.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata; artifact frontmatter and changelog state 0.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
