## Description:

Fetch and track OpenRouter AI model rankings (weekly trends, top models, top apps, market share). Use when user asks about OpenRouter rankings, AI model popularity, token usage statistics, or wants weekly automated reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yufeinever](https://clawhub.ai/user/yufeinever)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to fetch current OpenRouter model, provider, and app rankings and create weekly usage reports for trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script opens OpenRouter with Playwright and depends on the live rankings page structure.

Mitigation: Review generated reports before using them for decisions or automated publication.

Risk: The --save option writes report files under the user's home directory.

Mitigation: Run in an expected user context and confirm the output path before enabling scheduled saves.

Risk: The documented Feishu push path is under-specified and appears unimplemented in the bundled script.

Mitigation: Verify or implement the Feishu integration separately before relying on --push or configuring external report delivery.

## Reference(s):

- [OpenRouter Rankings](https://openrouter.ai/rankings)
- [ClawHub Skill Page](https://clawhub.ai/yufeinever/skills/openrouter-rankings)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, shell commands, configuration guidance]

**Output Format:** [Markdown report and optional JSON data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When run with --save, stores dated JSON and Markdown reports under ~/.openclaw/data/openrouter-rankings.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
