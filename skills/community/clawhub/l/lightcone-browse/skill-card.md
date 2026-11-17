## Description:

Lightcone Browse delegates browser tasks such as browsing, scraping, price checks, form filling, and web application operation to Lightcone's cloud computer-use automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddieogola](https://clawhub.ai/user/eddieogola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to delegate website browsing, scraping, price checks, form filling, and web app operation to a cloud browser when a local browser is unavailable or parallel visual automation is useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud browser automation may send user data, submit forms, post content, or change account state.

Mitigation: Require explicit user confirmation before logins, payments, form submissions, posting, account changes, or handling confidential business or personal data.

Risk: Delegated browsing may expose sensitive instructions, page content, or secrets to Lightcone's cloud browser environment.

Mitigation: Avoid secrets unless necessary and install only when the operator is comfortable delegating browsing to Lightcone's cloud browser.

## Reference(s):

- [Lightcone documentation](https://docs.lightcone.ai)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or text responses with returned page content and screenshot context]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TZAFON_API_KEY; supports a natural-language instruction, optional starting URL, and optional maxSteps limit.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
