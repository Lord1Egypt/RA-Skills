## Description:

Search video dialogue and create reaction GIFs with timed subtitles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coyote-git](https://clawhub.ai/user/coyote-git)

### License/Terms of Use:

MIT

## Use Case:

External users and creators use this skill to search dialogue in their video libraries, preview matching clips, and generate subtitled reaction GIFs or meme clips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path fetches mutable third-party code from an unpinned GitHub branch.

Mitigation: Review the upstream repository before installing and prefer a pinned commit or signed release when deploying the skill.

Risk: Automatic subtitle downloads and iMessage sending may share video-related metadata or generated media.

Mitigation: Use local subtitle files and avoid send options for sensitive videos unless the user has approved that sharing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/coyote-git/skills/gifhorse)
- [Publisher Profile](https://clawhub.ai/user/coyote-git)
- [GifHorse GitHub Repository](https://github.com/Coyote-git/gifhorse)
- [GifHorse Usage Guide](https://github.com/Coyote-git/gifhorse/blob/main/USAGE_GUIDE.md)
- [GifHorse Roadmap](https://github.com/Coyote-git/gifhorse/blob/main/ROADMAP.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include commands that call the gifhorse and ffmpeg binaries and produce GIF files from local video content.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
