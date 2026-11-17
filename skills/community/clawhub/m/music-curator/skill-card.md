## Description:

Curates personalized playlists and music recommendations with strict intent preservation, taste and version constraints, and clear boundaries between official identity and similarity-based discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neqq3](https://clawhub.ai/user/neqq3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to classify music requests, curate strict official or similarity-based playlists, filter noisy versions, and hand final selections to playback or discovery tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected music and discovery tools may search, enqueue, or start playback when the user asks for music.

Mitigation: Review those tools' permissions separately and ask for confirmation when curation confidence is medium or low.

Risk: Strict playlist requests can be diluted by similarity matches, noisy versions, or unrelated substitutions.

Mitigation: Classify each request first, filter non-canonical versions by default, and report missing canonical tracks instead of silently substituting unrelated songs.

## Reference(s):

- [Music Curator on ClawHub](https://clawhub.ai/neqq3/skills/music-curator)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown or plain text with curated track lists and concise rationale tags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include availability notes and short confirmation prompts before queueing uncertain selections.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
