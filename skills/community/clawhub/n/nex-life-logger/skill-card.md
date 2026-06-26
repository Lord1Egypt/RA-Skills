## Description: <br>
Track computer activity (browser history, active windows, YouTube videos) locally and query it with AI. All activity data stays on your machine. LLM features require explicit user configuration. Ask your agent what you were doing at any time. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[nexaiguy](https://clawhub.ai/user/nexaiguy) <br>

### License/Terms of Use: <br>
Creative Commons Attribution-NonCommercial 4.0 International <br>


## Use Case: <br>
External users and developers use this skill to collect local computer activity, search personal browsing and application history, generate summaries, and export activity records through a CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can continuously record browser history, foreground windows, searches, and YouTube activity. <br>
Mitigation: Install and run it only when the user intentionally wants activity logging, and stop or disable the background service when tracking should pause. <br>
Risk: The local database and exported reports may contain highly sensitive personal activity data. <br>
Mitigation: Keep the database and exports on trusted local storage with restrictive permissions, and avoid sharing exports without review. <br>
Risk: Remote summary generation can disclose local activity to the configured LLM provider. <br>
Mitigation: Use AI summaries only with a trusted provider or local endpoint, and avoid remote summaries for sensitive activity. <br>
Risk: Stored API keys may fall back to local plaintext owner-only storage on some platforms. <br>
Mitigation: Prefer the AI_API_KEY environment variable or the strongest OS credential store available. <br>


## Reference(s): <br>
- [Nex Life Logger on ClawHub](https://clawhub.ai/nexaiguy/nex-life-logger) <br>
- [Nex AI homepage](https://nex-ai.be) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and JSON CLI output, summarized by the agent in Markdown when responding to users.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI output may include local activity records, summaries, transcripts, statistics, and export file paths.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
