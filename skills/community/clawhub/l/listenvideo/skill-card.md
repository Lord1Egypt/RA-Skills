## Description:

Converts a video URL or local video file into cleaned text, and can use a custom prompt to summarize, rewrite, extract quotes, translate, or analyze the video content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, content creators, and agents use this skill to turn public or local videos into transcripts, summaries, meeting notes, subtitles, rewritten social copy, extracted quotes, or translated text. It is intended for one video at a time and requires a GUAIKEI_API_TOKEN for the vendor cloud workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos, prompts, token-authenticated requests, and possibly local path metadata may be sent to the vendor cloud workflow.

Mitigation: Avoid confidential media unless the vendor data handling, retention, and upload destinations are reviewed and accepted.

Risk: Attacker-supplied video URLs may introduce unsafe download or redirect behavior if URL handling, redirects, file size, and runtime are not constrained.

Mitigation: Process only trusted public HTTPS URLs or known local files, and add URL allowlisting, redirect validation, and file size/time limits before broader deployment.

Risk: The authoritative security verdict is suspicious because sensitive data destinations are under-disclosed.

Mitigation: Review and scan the skill before deployment, document network destinations, and allowlist only the expected vendor endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/listenvideo)
- [GuaiKei video-to-text service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or prompt-shaped text on stdout, with operational diagnostics on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may be full transcripts or prompt-derived summaries, rewrites, quote lists, subtitles, translations, meeting notes, or analysis.]

## Skill Version(s):

1.0.0 (source: package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
