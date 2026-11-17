## Description:

Use this skill when an agent needs to build and run exact-place Google Maps review scraping workflows through an Apify actor and return structured review rows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hundevmode](https://clawhub.ai/user/hundevmode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to extract Google Maps reviews for exact place URLs, CID URLs, review URLs, or Place IDs. It supports local SEO, reputation monitoring, sentiment analysis, competitor research, BI exports, and similar review-data workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says agents have too much room to override the Apify actor ID and run arbitrary Apify actors with the user's token.

Mitigation: Review before installing, keep the default actor unless another actor is intentional, and use a limited Apify token with budget limits.

Risk: The security review says the skill collects reviewer profile data by default.

Mitigation: Set personalData=false unless reviewer profile fields are explicitly needed and appropriate to retain.

Risk: Apify runs can consume paid usage.

Mitigation: Use --budget-usd or maxTotalChargeUsd for controlled runs and split large jobs by place list.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hundevmode/skills/google-maps-reviews-scraper-apify)
- [Project homepage from ClawHub metadata](https://github.com/hundevmode/apify-google-maps-reviews-scraper-agent-skill)
- [Apify Google Maps Reviews Scraper actor](https://apify.com/x_guru/google-maps-reviews-scraper)
- [Input and output contract](references/input-output-contract.md)
- [Sample input](references/sample_input.json)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payloads, shell commands, and JSON run output from the Apify actor.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIFY_TOKEN; runner output includes ok, actorId, fetchedAt, inputUsed, itemCount, and rows.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
