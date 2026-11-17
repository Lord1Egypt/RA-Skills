## Description:

Turn a podcast episode link, RSS feed, or direct audio URL into a timestamped transcript plus a production-ready Chinese two-host script package with outline.md, script.md, and notes.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haohuawu](https://clawhub.ai/user/haohuawu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and podcast producers use this skill to convert supported podcast sources into local transcript and production-script packages for Chinese two-host audio production. It supports staged, resumable work with scripted checks for transcript fetching, outline coverage, script format, and show notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch podcast, feed, transcript, image, and audio URLs and write downloaded content locally.

Mitigation: Run it in an isolated environment and avoid untrusted podcast, feed, transcript, image, and audio URLs.

Risk: The preflight --install path can install unpinned faster-whisper dependencies and pre-download an ASR model into the current Python environment or cache.

Mitigation: Preinstall pinned dependencies in a virtual environment and avoid running preflight --install on sensitive machines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haohuawu/skills/podcast-to-script)
- [Script format spec](artifact/references/script-spec.md)
- [Shownotes format spec](artifact/references/notes-spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text files with staged shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes an episode directory containing raw audio, transcript files, optional images, outline.md, script.md, and notes.md when all gates pass.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
