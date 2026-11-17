## Description:

Fetches popular HuggingFace Papers entries for daily, weekly, or monthly periods, translates abstracts to Chinese with DeepLX or an OpenAI-compatible backend when configured, and generates bilingual Markdown reports with trend analysis and reading recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isongxw](https://clawhub.ai/user/isongxw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agent users use this skill to monitor trending AI and machine learning papers on HuggingFace Papers, translate abstracts when needed, and produce note-ready Markdown reports for research tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paper abstracts may be sent to the configured DeepLX or OpenAI-compatible translation provider.

Mitigation: Use --no-translate when third-party translation is not acceptable, and configure only trusted HTTPS translation endpoints.

Risk: Translation credentials may be required for the enabled backend.

Mitigation: Keep API keys in a local .env file or environment variables and avoid committing secrets.

Risk: The skill fetches live HuggingFace pages and writes local report files.

Mitigation: Install dependencies in a virtual environment with pinned versions where possible, and review generated Markdown before sharing or importing it.

## Reference(s):

- [HuggingFace Papers](https://huggingface.co/papers)
- [Date Override Reference](references/date-override.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and optional JSON paper lists, with shell commands and environment-variable configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can be written to local .md files, printed to stdout, translated to Chinese, or generated in English with --no-translate.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
