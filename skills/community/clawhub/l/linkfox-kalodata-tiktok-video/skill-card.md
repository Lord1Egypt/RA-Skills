## Description:

Searches Kalodata-powered TikTok Shop video leaderboards and retrieves detailed engagement, GMV, advertising, creator, duration, and linked-product metrics for a selected TikTok video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, analysts, and agent users use this skill to discover high-performing TikTok Shop shoppable videos and inspect one video's performance details by videoId. It supports region, currency, language, date-range, GMV-range, and sorting workflows for video ranking and analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill calls external LinkFox and Kalodata services with an API key.

Mitigation: Install only in environments where LinkFox endpoint variables are trusted and API keys are handled as credentials.

Risk: Authentication and onboarding flows may involve phone numbers, SMS codes, and API key retrieval.

Mitigation: Do not share OTPs or API keys in logs or conversation transcripts, and verify the account flow before use.

Risk: Billing support can create payment orders for additional credits.

Mitigation: Require explicit user confirmation before ordering credits and review plan and payment details before proceeding.

Risk: Full API responses are written to local session files.

Mitigation: Review local result files for sensitive data and apply normal workspace retention or cleanup controls.

Risk: The artifact includes automatic feedback reporting behavior.

Mitigation: Disable or remove automatic feedback behavior if conversation privacy or data minimization requirements apply.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-kalodata-tiktok-video)
- [Kalodata TikTok Video API Reference](artifact/references/api.md)
- [Authentication and Billing Onboarding](artifact/references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results or summaries saved as local JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full responses are stored under a local linkfox session directory; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
