## Description:

Helps companies screen their patent portfolios for potential pledge financing and prepare a candidate list and document checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

External users at small and medium-sized companies use the skill to identify potentially suitable patents for bank pledge financing and organize supporting documents. It does not value patents, and final legal status should be checked against official records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated requests, redirects, or saved credentials may expose an API key or reach an unapproved destination.

Mitigation: Require HTTPS and approved-destination enforcement, handle redirects safely, use a limited PatentMax key, and protect saved credentials.

Risk: Unsafe cache paths or mismatched patent identities may affect cached patent data.

Mitigation: Review cache-path containment and validate patent identity before relying on cached data.

Risk: Company names, patent identifiers, and query terms are sent to PatentMax and may disclose confidential information; API use may also incur charges.

Mitigation: Avoid sending confidential invention details and confirm expected charges before querying.

Risk: Patent pledge status in returned data may not reflect the latest official registration.

Mitigation: Verify final pledge status against the relevant official records.

## Reference(s):

- [ClawHub release](https://clawhub.ai/ip930/skills/patent-pledge-prep)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [API reference](references/api-reference.md)
- [Search workflow](references/search-workflow.md)
- [Query syntax](references/query-syntax.md)

## Skill Output:

**Output Type(s):** [Analysis, Files, Guidance]

**Output Format:** [UTF-8 CSV candidate list and concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Candidate screening and document checklist; patent value is not assessed.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter; ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
