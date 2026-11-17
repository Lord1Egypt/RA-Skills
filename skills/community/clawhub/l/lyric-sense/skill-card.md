## Description:

Lyric Sense helps an agent search for timestamped lyrics by artist and song title, display synchronized lyric text, and guide online or local LrcApi use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adminlove520](https://clawhub.ai/user/adminlove520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to retrieve LRC lyrics and cover data for songs, display the current lyric line during playback, and configure either the public API or a self-hosted LrcApi service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled local LrcApi exposes broad file, database, network, and media-writing capabilities with weak defaults and incomplete disclosure.

Mitigation: Review before installing; bind self-hosted services to localhost, enable strong authentication, avoid public interfaces, and do not mount sensitive directories.

Risk: Online lyric and cover searches send artist and song title data to api.lrc.cx, and the included HTML UI also uses corsproxy.io.

Mitigation: Disclose third-party requests before use and prefer a reviewed local endpoint for sensitive listening history or private metadata.

Risk: Container deployment examples use latest Docker tags.

Mitigation: Pin a reviewed image tag and configuration before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adminlove520/skills/lyric-sense)
- [Lyric Sense artifact README](artifact/README.md)
- [Lyric Sense artifact skill file](artifact/SKILL.md)
- [Lyric Sense public demo](https://adminlove520.github.io/lyric-sense)
- [LrcApi documentation](https://docs.lrc.cx/)
- [LrcApi project](https://github.com/HisAtri/LrcApi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline API URLs, shell commands, and LRC timestamped lyric text when lyrics are returned]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call public lyric and cover APIs or guide configuration of a local LrcApi endpoint.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
