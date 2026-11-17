## Description:

Instagram Video Downloader parses Instagram video links through the redfox.hk API and returns watermark-free video download URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, editors, collectors, and researchers use this skill to parse public Instagram Reel or post video links and obtain direct MP4 download links for authorized saving, editing, backup, or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-submitted Instagram URLs are sent to redfox.hk for parsing.

Mitigation: Submit only public Instagram URLs that the user owns or is authorized to download, and avoid private or unrelated URLs.

Risk: The skill uses a RedFox API key and supports command-line or local-file credential handling.

Mitigation: Prefer the REDFOX_API_KEY environment variable, avoid passing keys on the command line, and confirm the key source, scope, expiration, and revocation path before use.

Risk: The security evidence reports external output and weak safeguards around third-party results.

Mitigation: Review returned links before opening or downloading them, and scan downloaded media according to local security policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/instagram-video-downloader)
- [RedFox API keys](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFox Instagram video download API endpoint](https://redfox.hk/story/api/parseWork/videoDownload/instagram)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown and terminal text with full download and cover URLs; optional JSON output from the script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one Instagram link per request; batch upload is not supported.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
