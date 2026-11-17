## Description:

Podcast Pipeline helps podcast creators prepare interviews, turn transcripts or solo episode ideas into publish-ready assets, and track episodes, sponsors, and seasons across a local history file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris](https://clawhub.ai/user/chris)

### License/Terms of Use:

MIT-0

## Use Case:

External podcast creators and production teams use this skill to prepare guest interviews, generate show notes, chapter markers, short-form clip ideas, platform-specific social posts, YouTube descriptions, and lightweight episode or sponsor records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Podcast episode history, transcripts, sponsor contacts, and ad scripts may be sensitive when retained in podcast-data.json.

Mitigation: Save records only when retention is intended, avoid storing confidential material, and review or delete podcast-data.json when the project no longer needs it.

Risk: Generated chapter timestamps, show notes, social posts, and YouTube descriptions may need editorial review before publication.

Mitigation: Verify timestamps against the recording and review generated publishing copy before using it externally.

## Reference(s):

- [Podcast Pipeline on ClawHub](https://clawhub.ai/chris/skills/podcast-pipeline)
- [Publisher profile](https://clawhub.ai/user/chris)
- [README](README.md)
- [CHANGELOG](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown sections with optional local JSON record updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or update a local podcast-data.json when the user explicitly asks to log episodes, sponsors, or seasons; chapter timestamps are estimates that should be checked before publishing.]

## Skill Version(s):

1.1.0 (source: frontmatter, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
