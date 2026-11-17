## Description:

Compares technology routes and recommends patent portfolio priorities, filing timelines, and design-around options using PatentMax reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

R&D teams and patent strategists use this skill to compare technology directions and plan patent filings around budgets, disclosure dates, and competitive patent constraints. Recommendations are technical and business guidance, not legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Report inputs may include confidential inventions, customer names, and filing plans sent to an external service.

Mitigation: Review data handling before use and omit unnecessary trade secrets, identifiers, and sensitive strategy details.

Risk: The API key and sensitive report inputs could be sent to an untrusted destination if the service URL is changed.

Mitigation: Keep the API key secret, use the official PatentMax endpoint, and do not set PATENTMAX_BASE_URL unless the destination is trusted.

Risk: Cached requests or downloaded reports may retain confidential information locally.

Mitigation: Protect local files and clear PatentMax cache and report files when they are no longer needed.

Risk: Repeated paid submissions may incur extra charges.

Mitigation: Confirm the charge with the user before submission and resume an existing operation instead of resubmitting it.

Risk: Patent recommendations may miss unpublished applications or be mistaken for legal clearance.

Mitigation: State search limitations and have a qualified patent professional assess claims, freedom to operate, and filing decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ip930/skills/patentmax-roadmap)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [Business context guide](references/context-guide.md)
- [Analysis workflow](references/workflow.md)
- [Troubleshooting and API examples](references/faq.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Conversational summary and downloadable Word (.docx) report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PatentMax API key; report generation is paid and asynchronous.]

## Skill Version(s):

1.2.1 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
