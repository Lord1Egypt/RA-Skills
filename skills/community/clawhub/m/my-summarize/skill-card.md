## Description:

Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).

This skill is ready for commercial/non-commercial use.

## Publisher:

[shahuquan-dotcom](https://clawhub.ai/user/shahuquan-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to ask an agent for concise summaries of web pages, local files, PDFs, images, audio, and YouTube links through the summarize CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on installing and invoking an external summarize CLI from a Homebrew tap.

Mitigation: Install only when the publisher, CLI, and Homebrew tap are trusted for the intended environment.

Risk: Summarized files, URLs, media, or extracted content may be sent to the selected model provider or optional extraction services.

Mitigation: Avoid private, regulated, or sensitive inputs unless the selected provider and optional services are approved for that data; configure only the API key needed for the chosen provider.

## Reference(s):

- [My Summarize on ClawHub](https://clawhub.ai/shahuquan-dotcom/skills/my-summarize)
- [summarize homepage](https://summarize.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and optional JSON output from the summarize CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports length and output-token controls through CLI flags; JSON output is available with --json.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
