## Description:

Searches synchronized Etsy category data by keyword and returns matching category names, ids, and parentIds for product or shop filtering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up Etsy category identifiers from a synchronized LinkFox category dataset for product and shop filtering workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses LinkFox network services and handles API keys.

Mitigation: Install only if comfortable using LinkFox services; obtain keys through the official LinkFox UI or a secret manager and avoid pasting keys into shared transcripts or shell profiles.

Risk: The onboarding flow can guide phone-based login and payment order creation.

Mitigation: Run login or payment commands only when explicitly intended, and confirm the selected plan and payment method before creating an order.

Risk: The category search script saves full API responses as local JSON files.

Mitigation: Review the saved output location and avoid running the script in workspaces where persisted response data should not be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-etsy-category-search)
- [_ehunt_etsyCategorySearch API reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Configuration guidance]

**Output Format:** [JSON responses, saved JSON result files, and concise Markdown guidance with command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Large API responses are summarized in stdout while full responses are saved to local session data files.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
