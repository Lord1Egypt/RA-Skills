## Description:

Pre-campaign audience quality and follower authenticity analysis across TikTok, Instagram, and YouTube, including geography, language, age, gender, interests, and creator comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengyu-xixihaha](https://clawhub.ai/user/chengyu-xixihaha)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing teams, creator partnerships teams, and agents use this skill to evaluate whether creators' audiences match an intended campaign profile and to compare audience quality before outreach or spend decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The provider gateway receives creator identifiers and audience-analysis API requests.

Mitigation: Use only creator identifiers and campaign criteria that are appropriate to share with the configured gateway, and review organizational data-sharing requirements before execution.

Risk: A project .env can route paid API keys to a configured SCRUMBALL_BASE_URL.

Mitigation: Set SCRUMBALL_BASE_URL only to a trusted endpoint and avoid storing paid API keys in project-local .env files unless the endpoint and workspace are trusted.

Risk: The helper creates a stable install ID that can correlate requests across sessions until deleted.

Mitigation: Review this behavior before installation and delete the install ID if a reset is required by local policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chengyu-xixihaha/skills/influencer-audience-fit-scoring)
- [API Index](artifact/references/api-index.md)
- [Request and Response Guide](artifact/references/request-response.md)
- [Operation Manifest](artifact/references/operations.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional JSON API call results and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include a fit score with confidence, a dimension-by-dimension score breakdown, a go/test/no-go decision, and the next validation action.]

## Skill Version(s):

1.0.3 (source: server release metadata and config.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
