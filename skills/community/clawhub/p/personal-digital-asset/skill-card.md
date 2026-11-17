## Description:

Helps individuals inventory digital assets through a nine-question self-check and evidence-backed asset cards, with an optional authorized zengzhi.life workflow that stops before public publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atoa727](https://clawhub.ai/user/atoa727)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals use this skill to identify and document potentially marketable digital assets, supporting evidence, and next steps. With their authorization, it can prepare a report and display-page draft on zengzhi.life for their review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Platform mode shares personal asset descriptions, evidence files, and account-linked data with zengzhi.life.

Mitigation: Use the account-free inventory mode unless the user agrees to share those materials; review and limit sensitive uploads.

Risk: A zengzhi.life API key grants the agent access to account-linked drafting actions.

Mitigation: Provide a key only when intending to authorize platform actions; do not log, save, or repeat it, and rotate it if exposed.

Risk: Unverified asset claims or draft contents could be mistaken for approved listings.

Mitigation: Mark missing evidence, and have the user personally review and perform any publication, listing, signing, or transaction confirmation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/atoa727/skills/personal-digital-asset)
- [Nine-question self-check and asset-card templates](references/selfcheck.md)
- [zengzhi.life Agent API reference](references/zengzhi-api.md)
- [zengzhi.life Agent guide](https://zengzhi.life/agent-guide.html?utm_source=skill)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown asset cards and guidance; optional platform report and display-page draft details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each asset card records evidence gaps and payment-validation confidence; publication remains a user action.]

## Skill Version(s):

1.1.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
