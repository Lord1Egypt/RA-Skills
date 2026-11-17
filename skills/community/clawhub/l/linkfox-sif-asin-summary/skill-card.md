## Description:

Analyzes Amazon ASIN exposure and traffic-source composition across organic search, paid ads, recommendations, and period-over-period keyword changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and ecommerce analysts use this skill to query ASIN-level SIF data, compare traffic-source structure, and summarize exposure shifts across the current and previous periods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ASIN query data and conversation-derived feedback content may be sent to LinkFox services.

Mitigation: Install only if that data sharing is acceptable, and avoid submitting sensitive or unnecessary business context with ASIN queries or feedback.

Risk: The onboarding flow handles API keys and can lead users into billing or order commands.

Mitigation: Use a dedicated low-value API key, keep secrets out of shell history and startup files, and run billing or order commands only when payment is intended.

Risk: Custom endpoint or SESSION_ID environment values may affect request destinations or data grouping.

Mitigation: Use default service endpoints and session values unless you control the custom values and understand the resulting data handling.

Risk: The security scan flags unsafe environment and file handling for review.

Mitigation: Review generated files and workspace output paths before deployment, and run the skill only in workspaces where LinkFox data files are expected.

## Reference(s):

- [SIF-ASIN traffic source API reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-sif-asin-summary)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses or compact response summaries, plus saved JSON data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API responses are cached for 24 hours for matching parameters; large responses are summarized in stdout while the full JSON response is saved to the workspace.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
