## Description:

Maejongdeok helps users view booking guidance, open BeautsGO clinic pages, submit appointment requests, contact online support, and query prices for Maison de M clinic in Seoul.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beautsgo](https://clawhub.ai/user/beautsgo)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to navigate BeautsGO booking flows for Maison de M clinic, submit appointment requests after providing contact details, check project pricing, or open consultation and app download links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The booking workflow sends appointment details, including user-provided contact information, to external services.

Mitigation: Use the skill only when the user intends to submit those details, and add an explicit confirmation step before transmission.

Risk: The security summary identifies unsafe URL opening and exposed API tokens as review-worthy risks.

Mitigation: Replace shell-based URL opening, rotate or remove embedded tokens, and document all external destinations before deployment.

Risk: The security guidance flags a direct APK download link.

Mitigation: Prefer official app-store links over direct APK downloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beautsgo/skills/maejongdeok-clinic-booking)
- [BeautsGO clinic page](https://i.beautsgo.com/cn/hospital/maisondem-clinic?from=skill)
- [BeautsGO booking page](https://i.beautsgo.com/cn/hospital/maisondem-clinic/skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [String responses, often Markdown-formatted booking guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include booking status, price query results, direct BeautsGO links, or app download instructions.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
