## Description:

Screens publicly accessible product image URLs with Ruiguan visual-similarity search to identify matches against known policy-violating products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce operators, marketplace teams, and compliance reviewers use this skill to pre-screen product images for possible policy risk before listing or review. It helps compare a submitted image with known prohibited-product records and presents similarity-ranked matches for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product images and detection requests are sent to LinkFox services, and local image uploads create publicly accessible URLs.

Mitigation: Prefer already-public product images, avoid confidential local files, and submit local images only when a temporary public URL is acceptable.

Risk: The skill handles API keys, account setup, billing, and payment-related onboarding flows.

Mitigation: Verify LINKFOX_* endpoint variables before use, keep API keys private, and start phone, SMS, or payment flows only when the user explicitly intends to do so.

Risk: Full API responses are saved locally and may include sensitive image URLs, match details, detection identifiers, or account-adjacent data.

Mitigation: Treat saved response files as sensitive, avoid unnecessary inline output for confidential results, and clean up local LinkFox output directories according to the user's retention requirements.

Risk: Feedback reporting can transmit information about skill behavior or user reactions to LinkFox.

Mitigation: Do not include secrets, private images, or confidential business context in feedback content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-ruiguan-gun-parts-search)
- [Publisher profile](https://clawhub.ai/user/linkfox-ai)
- [Ruiguan image compliance API reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown result summaries with optional JSON response files and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a single imageUrl input, writes full API responses to local JSON files, may summarize large responses, and can upload supported local image files to obtain a temporary public URL.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
