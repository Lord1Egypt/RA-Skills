## Description:

Track computer activity (browser history, active windows, YouTube videos) locally and query it with AI. All activity data stays on your machine. LLM features require explicit user configuration. Ask your agent what you were doing at any time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexaiguy](https://clawhub.ai/user/nexaiguy)

### License/Terms of Use:

Creative Commons Attribution-NonCommercial 4.0 International

## Use Case:

Employees and external users can use this skill to let an agent search, summarize, and export their local computer activity history. It is intended for personal activity recall and productivity review across browser history, active windows, YouTube transcripts, extracted keywords, and AI-generated summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs continuous local activity monitoring that records browser history, active window focus, and YouTube transcript data.

Mitigation: Install only when persistent local activity recording is intended, review setup.sh before running it, and stop or disable the collector service when tracking is not needed.

Risk: AI summary generation may send activity summaries to a configured LLM provider.

Mitigation: Avoid configuring an API key unless sharing activity context with that provider is acceptable; prefer environment variables for API keys.

Risk: Exports and the local database can contain sensitive personal activity data.

Mitigation: Treat exported JSON, CSV, and HTML files and the ~/.life-logger data directory as highly private files.

Risk: Credential storage falls back to an owner-only local file on Linux and macOS.

Mitigation: Prefer the AI_API_KEY environment variable for stronger control over API key storage.

## Reference(s):

- [Nex Life Logger on ClawHub](https://clawhub.ai/nexaiguy/skills/nex-life-logger)
- [Nex AI homepage](https://nex-ai.be)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV, HTML, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown responses, optional JSON/CSV/HTML exports, and shell commands for setup, service management, configuration, search, summaries, transcripts, statistics, and exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may summarize or expose highly private local activity data collected from browser history, active window focus, YouTube transcripts, keywords, and configured LLM summaries.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
