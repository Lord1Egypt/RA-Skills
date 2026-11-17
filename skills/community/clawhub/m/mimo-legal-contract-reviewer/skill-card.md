## Description:

合同审查助手 reviews Chinese-law contract text, identifies risky clauses, grades risks, and suggests edits while reminding users that major contracts should be reviewed by a qualified lawyer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to review employment, lease, commercial cooperation, service, sales, confidentiality, authorization, procurement, and loan contracts for clause-level risks and practical revision suggestions. It is an assistant for contract-risk triage and does not replace professional legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake contract-risk guidance for formal legal advice.

Mitigation: State that the review is for reference only and recommend a qualified lawyer for high-value, cross-border, or complex contracts.

Risk: Contracts may contain unnecessary sensitive personal, employment, financial, or business information.

Mitigation: Ask users to share only the contract text needed for review and omit unnecessary sensitive details.

Risk: Legal guidance can become outdated as laws and regulations change.

Mitigation: Remind users to verify current law and seek professional advice before relying on recommendations.

## Reference(s):

- [legal-contract-reviewer detailed reference](references/details.md)
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/skills/mimo-legal-contract-reviewer)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Chinese Markdown contract review report with risk tables, revision comparisons, signing recommendation, and action checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default legal frame is Chinese law; cross-border contracts require the applicable jurisdiction to be stated.]

## Skill Version(s):

1.3.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
