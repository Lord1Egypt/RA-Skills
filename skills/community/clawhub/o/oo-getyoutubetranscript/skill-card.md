## Description:

Use GetYouTubeTranscript to search YouTube, browse playlists and channels, check credits, and retrieve video transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to search YouTube and retrieve channel, playlist, and transcript data through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructs the agent to execute remote installers without a separate approval step; the installers' exact behavior remains unverified.

Mitigation: Review setup before enabling the skill. Install a reviewed, version-pinned CLI yourself, check its automatic skill installation behavior across agent applications, and require approval for installation and persistent agent changes.

## Reference(s):

- [GetYouTubeTranscript documentation](https://getyoutubetranscript.com/docs)
- [GetYouTubeTranscript homepage](https://getyoutubetranscript.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [GetYouTubeTranscript skill page](https://clawhub.ai/oomol/skills/oo-getyoutubetranscript)
- [GetYouTubeTranscript connection setup](https://console.oomol.com/connections/getyoutubetranscript)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON connector responses; transcript content may be plain text or timestamped lines.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript timestamps are optional; available response fields depend on the selected action and its live schema.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
