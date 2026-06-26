## Description: <br>
Summarize or extract text/transcripts from URLs, podcasts, and local files (great fallback for "transcribe this YouTube/video"). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to summarize URLs, articles, podcasts, YouTube links, and local files, or to extract best-effort transcripts when a transcript is requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Content from confidential files, private URLs, or sensitive transcripts may be sent to the configured AI provider or optional Firecrawl and Apify services. <br>
Mitigation: Use the skill only with trusted providers and avoid sensitive inputs unless the user is comfortable with those services processing the content. <br>
Risk: The skill depends on the third-party summarize CLI and Homebrew tap. <br>
Mitigation: Install only from a trusted tap and review the CLI behavior before using it in sensitive workflows. <br>


## Reference(s): <br>
- [summarize.sh](https://summarize.sh) <br>
- [ClawHub skill page](https://clawhub.ai/mohdalhashemi98-hue/mh-summarize) <br>
- [Publisher profile](https://clawhub.ai/user/mohdalhashemi98-hue) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON output from the summarize CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can summarize content at requested lengths and optionally produce machine-readable CLI output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
