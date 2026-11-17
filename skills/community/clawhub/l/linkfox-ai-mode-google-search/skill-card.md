## Description:

Google-AI Mode 搜索 retrieves a Google AI Overview / AI Mode result for one keyword and returns the captured answer as Markdown with source links for live web research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and research agents use this skill to ask one Google AI Mode search question at a time for deep research, technical question answering, long-tail product analysis, and overseas consumer preference research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and some agent or session metadata may be sent to LinkFox.

Mitigation: Avoid sensitive queries and use the skill only when sharing that information with LinkFox is acceptable.

Risk: Full search responses are retained in local response files.

Mitigation: Review and clear saved response files according to the user's local data-retention policy.

Risk: Onboarding and billing flows may involve phone numbers, SMS codes, API keys, and payment actions.

Mitigation: Use these flows only intentionally, verify billing steps before proceeding, and manage API keys through a secure credential store.

Risk: Search output is live AI Overview text and may be unavailable, change between calls, or be incomplete.

Mitigation: Preserve source links, tell users when no AI Overview is returned, and avoid treating the Markdown as structured data.

## Reference(s):

- [Google AI Search API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-ai-mode-google-search)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Files, Shell commands, Guidance]

**Output Format:** [Markdown answer text and JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single keyword per call; full API responses are saved locally, with large responses summarized on stdout unless inline output is requested.]

## Skill Version(s):

1.0.7 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
