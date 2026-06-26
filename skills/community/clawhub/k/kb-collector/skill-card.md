## Description: <br>
Kb Collector saves YouTube videos, URLs, and text to Obsidian with AI summarization, transcription, digest emails, and nightly research automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arbiger](https://clawhub.ai/user/arbiger) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to collect web pages, YouTube transcripts, and plain text into an Obsidian knowledge base, then generate digests or nightly AI trend research summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Digest and research scripts can email local vault-derived content when send options are enabled, including a hard-coded recipient in the digest script. <br>
Mitigation: Review and edit the scripts before installing or running; replace recipients, vault paths, Gmail/gog authorization, and cron examples before using send options. <br>
Risk: Fetched web pages, YouTube transcripts, and Tavily search results are saved into the user's vault and may contain untrusted or misleading content. <br>
Mitigation: Treat collected pages, transcripts, and generated summaries as untrusted until reviewed; do not rely on them without source checking. <br>
Risk: Nightly research requires an intentionally configured Tavily API key and may send external search queries. <br>
Mitigation: Set TAVILY_API_KEY deliberately, review the topic list and external API behavior, and avoid scheduled runs until the configuration is correct. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/arbiger/kb-collector) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown notes and digest text with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Obsidian Markdown files and optional email digest content; local paths, recipients, and API keys must be configured before use.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
