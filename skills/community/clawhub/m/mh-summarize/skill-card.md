## Description:

Summarize or extract text and transcripts from URLs, podcasts, and local files, including best-effort YouTube or video transcript extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue)

### License/Terms of Use:


## Use Case:

Developers, employees, and external users can use this skill to summarize web pages, local files, podcasts, and YouTube or video links through the summarize CLI. It is useful when an agent needs concise summaries, extracted text, or best-effort transcripts from supported inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URLs, file contents, or transcript text may be sent to the selected model provider and, when enabled, to Firecrawl or Apify.

Mitigation: Use the skill only with content whose external processing is acceptable, avoid confidential or authenticated inputs unless approved, and disable optional fallback services when they are not needed.

Risk: The skill depends on the local summarize CLI and configured provider credentials.

Mitigation: Install the expected summarize binary, configure only the required provider API keys, and review command output before relying on it for decisions.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/mohdalhashemi98-hue/skills/mh-summarize)
- [Publisher profile](https://clawhub.ai/user/mohdalhashemi98-hue)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with inline shell commands and optional JSON output from the summarize CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports length controls, output token limits, extract-only mode, provider model selection, and optional Firecrawl or Apify fallback services.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
