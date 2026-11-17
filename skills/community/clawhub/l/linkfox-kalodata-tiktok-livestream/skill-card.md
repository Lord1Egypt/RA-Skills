## Description:

Searches Kalodata TikTok Shop livestream leaderboards and retrieves detailed metrics for a selected livestream, including revenue, viewers, duration, GPM, and product count.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to browse TikTok Shop livestream rankings by region, currency, language, and date range, then fetch one livestream's detailed performance data by livestreamId. It is suited for presenting livestream analytics data without providing subjective business advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes that the skill should be reviewed before use because it stores full API responses locally and includes account, payment, and feedback-related flows.

Mitigation: Use the skill only in a trusted environment, review generated files before sharing, and require explicit user approval before feedback submission, account onboarding, or order/payment actions.

Risk: Endpoint override environment variables could route requests to unintended services.

Mitigation: Avoid untrusted LINKFOX_* endpoint overrides and confirm the configured gateway before use.

Risk: API keys and phone verification codes may be exposed if routed through shared logs or transcripts.

Mitigation: Keep LINKFOX API keys and verification codes out of shared logs, screenshots, and public issue reports.

## Reference(s):

- [Kalodata-TikTok直播搜索与详情 API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-kalodata-tiktok-livestream)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON data summaries and optional saved JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are saved locally; small responses may also be printed inline, while larger responses are summarized.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
