## Description:

This skill helps social media, ecommerce, game, and brand teams turn meme-video ideas into original Chinese production briefs, storyboard scripts, prompts, AI-HIVE generation commands, and quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, social media operators, ecommerce teams, and developers use this skill to convert authorized meme references, brand facts, audience constraints, and platform requirements into reviewable short-video plans and runnable AI-HIVE commands. It supports original adaptation, task tracking, and acceptance checks for meme-style promotional content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials can be exposed or sent to an unintended endpoint if users provide untrusted base URLs or environment configuration.

Mitigation: Use the official AI-HIVE URL, avoid untrusted --base-url or AI_HIVE_BASE_URL values, do not paste real keys into prompts or logs, and rotate the API key if it may have been used with a custom endpoint.

Risk: Generation commands can incur cost and downloaded media may be unsafe or unsuitable without review.

Mitigation: Confirm prompts, routing mode, model, price snapshot, output path, and batch size before execution; treat generated downloads as untrusted files until reviewed.

Risk: Meme adaptation can produce copyright, endorsement, platform-policy, or factual-claim issues if reference material and brand facts are not verified.

Mitigation: Use only authorized assets, rewrite protected references into original expressions, mark unverified claims as pending review, and avoid promises about traffic, sales, ranking, approval, or return on investment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/meme-short-video-generator-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON artifacts and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local project blueprints, run ffmpeg-based video edits, upload media, submit AI-HIVE generation tasks, poll task status, and download generated files when the user confirms the parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
