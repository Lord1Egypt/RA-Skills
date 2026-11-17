## Description:

Recommend music based on your current mood, activity, or conversation context. Returns a curated track list you can search on Spotify, YouTube, or Apple Music.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

External users ask an agent for mood-, activity-, or time-aware music recommendations and receive a curated list of tracks to search on Spotify, YouTube, or Apple Music.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommendation quality may be limited by heuristic mood detection and a fixed curated track list.

Mitigation: Review suggested tracks before relying on them; treat them as music suggestions rather than personalized or exhaustive playlists.

Risk: Some artifact documentation contains stale or overbroad claims about generated playlist links, learning over time, storage, and platform integration.

Mitigation: Use the version 1.0.1 SKILL.md, changelog, and server security guidance as the release scope: no API credentials are needed, no hidden network access or persistence was found, and outputs are searchable track lists.

Risk: Conversation context shared with the agent may include personal mood or activity details.

Mitigation: Share only context appropriate for music recommendations and avoid sensitive personal information when requesting suggestions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/theshadowrose/skills/mood-music)
- [OpenClaw Project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text with a mood label and curated track list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API credentials are required; recommendations are based on local conversation context and curated track data.]

## Skill Version(s):

1.0.1 (source: frontmatter and changelog, released 2026-03-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
