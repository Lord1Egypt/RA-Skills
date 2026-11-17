## Description:

Hit Preview EN analyzes English short-video scripts for TikTok, YouTube Shorts, Instagram Reels, and similar platforms, producing hit-potential predictions and improvement suggestions with AI or local fallback analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[makclaw](https://clawhub.ai/user/makclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and developers use this skill to evaluate short-form video scripts and receive concise guidance on hooks, cliffhangers, hit potential, and platform adaptation before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI mode can send the complete analyzed script to the configured external provider.

Mitigation: Use AI mode only with scripts that are appropriate to share with the selected provider, or rely on local fallback behavior for private scripts.

Risk: Provider base URL environment variables can direct requests to endpoints selected by the local environment.

Mitigation: Run the skill only where provider base URL variables are trusted and reviewed before use.

Risk: Connection tests or AI requests may involve valuable LLM API credentials.

Mitigation: Avoid running connection tests in shared logs and protect provider API keys in the execution environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/makclaw/skills/hit-preview-en)
- [Hit Preview Web Version](https://hit-preview.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style English analysis report with scores and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports cover hook analysis, cliffhanger design, hit-potential prediction, and platform adaptation suggestions; AI mode may send the analyzed script to the configured external provider, while fallback mode runs locally.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
