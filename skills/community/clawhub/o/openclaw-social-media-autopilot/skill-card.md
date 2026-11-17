## Description:

Generate a complete 7-day social media content calendar with Instagram-ready captions, hashtags, optimal posting times, and content mix strategy for any brand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dreamsarts](https://clawhub.ai/user/dreamsarts)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, small business operators, and content creators use this skill to generate a week of platform-ready social media post plans from brand, niche, audience, tone, platform, and start-date inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reaches into a hard-coded personal .env file for secrets.

Mitigation: Review before installing and change secret loading to read only an explicitly provided GEMINI_API_KEY from the current environment or a user-selected configuration file.

Risk: Dependencies are not pinned.

Mitigation: Pin dependencies before deployment and review dependency updates during maintenance.

Risk: Business-planning inputs are sent to Gemini for caption generation.

Mitigation: Document that Gemini receives brand, niche, audience, tone, platform, and calendar-planning inputs so users can avoid submitting sensitive data.

Risk: Scheduling or account actions are under-scoped.

Mitigation: Remove automated posting behavior or tightly gate scheduling and account actions behind explicit user review and approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dreamsarts/skills/openclaw-social-media-autopilot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON content calendar with captions, hashtags, posting times, visual directions, calls to action, content pillars, and strategy metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write the generated calendar to a JSON file when an output path is provided.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
