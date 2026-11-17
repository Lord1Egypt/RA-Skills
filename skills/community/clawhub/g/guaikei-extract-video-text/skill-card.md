## Description:

Converts video or audio from a URL or local file into cleaned transcript text, and can apply a custom prompt to summarize, rewrite, extract highlights, outline scenes, or translate the content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to turn video or audio sources into polished transcripts, summaries, rewritten social copy, highlights, meeting notes, scripts, and translations through a command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends video content, prompts, task identifiers, filenames, and an API token to the provider's cloud service.

Mitigation: Use only explicit user-approved media and prompts, and avoid processing confidential or regulated content unless the provider relationship and data handling terms are acceptable.

Risk: The skill can fetch broad user-supplied URLs and upload local files, which can expose sensitive local paths, private-network URLs, localhost URLs, metadata-service URLs, or redirected links.

Mitigation: Prefer known public HTTPS media URLs or approved local files, and reject private-network, localhost, metadata-service, or untrusted redirected URLs before execution.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/engheng-art/skills/guaikei-extract-video-text)
- [GuaiKei service website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text on stdout, with progress logs and errors on stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and GUAIKEI_API_TOKEN; accepts a media URL, local media file path, or previous task ID plus an optional prompt.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
