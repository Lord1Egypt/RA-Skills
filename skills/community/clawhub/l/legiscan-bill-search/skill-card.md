## Description:

Search and track active or completed state bills by keyword and state using the LegiScan API with configurable filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n4cra](https://clawhub.ai/user/n4cra)

### License/Terms of Use:


## Use Case:

Developers and policy-focused users can use this skill to query state legislative activity by state, keyword, and bill status. It helps produce concise bill summaries and links for monitoring topics such as cryptocurrency, bitcoin, and blockchain legislation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The LegiScan API key, selected state, and configured search keywords are sent to LegiScan during searches.

Mitigation: Use a dedicated revocable LegiScan API key and choose search terms with that data sharing in mind.

Risk: Request URLs include the API key, which can be exposed if URLs are logged by surrounding tooling.

Mitigation: Avoid logging full request URLs and rotate the API key if exposure is suspected.

Risk: Scheduled runs can consume API quota depending on frequency and keyword volume.

Mitigation: Run scheduled searches at a cadence compatible with the LegiScan API quota.

## Reference(s):

- [LegiScan API](https://legiscan.com/legiscan)
- [ClawHub Skill Page](https://clawhub.ai/n4cra/skills/legiscan-bill-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown text with bill summaries, last-action dates, descriptions, and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a LegiScan API key supplied through the LEGISCAN_API_KEY environment variable.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
