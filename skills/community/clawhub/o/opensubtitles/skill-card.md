## Description:

Read-only OpenSubtitles skill for searching and downloading subtitles via API and extracting timestamped scene context while avoiding spoilers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisooki](https://clawhub.ai/user/dennisooki)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search OpenSubtitles, request subtitle download links, and extract local SRT context around a timestamp for spoiler-aware answers about a show.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenSubtitles API keys, passwords, or tokens could be exposed in agent output or logs.

Mitigation: Keep credentials in environment variables and do not echo secrets in commands, logs, or user-facing responses.

Risk: An unverified OPENSUBTITLES_BASE_URL could direct API requests away from the expected OpenSubtitles service.

Mitigation: Leave OPENSUBTITLES_BASE_URL unset unless it was returned by OpenSubtitles login and verified as an OpenSubtitles host.

Risk: Shared or writable subtitle cache directories could expose downloaded subtitle files or create file-boundary issues.

Mitigation: Use a private subtitle cache and read only expected .srt files from that cache.

Risk: Download-link requests can consume account quota.

Mitigation: Check the local subtitle cache before requesting download links and report remaining quota after download-link actions.

## Reference(s):

- [OpenSubtitles API Reference](references/opensubtitles-api.md)
- [OpenSubtitles API Consumers](https://www.opensubtitles.com/consumers)
- [OpenSubtitles API v1](https://api.opensubtitles.com/api/v1)
- [ClawHub skill page](https://clawhub.ai/dennisooki/skills/opensubtitles)
- [Publisher profile](https://clawhub.ai/user/dennisooki)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and extracted subtitle text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenSubtitles API key and User-Agent; download-link flows may require account credentials or a token and quota awareness.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
