## Description:

YouTube (youtube.com). Use this skill for ANY YouTube request — reading, creating, updating, and deleting data. Whenever a task involves YouTube, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent with an OOMOL-connected YouTube account use this skill to find and manage YouTube videos, channels, playlists, comments, and captions, including creating or changing content when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can automatically run unverified third-party installation code and may change other agents' installed skills.

Mitigation: Review and approve CLI installation separately before setup; use a verified, fixed CLI release where available.

Risk: Write or destructive actions can publish, change, or delete YouTube content.

Mitigation: Confirm the exact action and payload with the user before writes, and retain the documented confirmation steps for public posts and deletions.

## Reference(s):

- [YouTube Data API documentation](https://developers.google.com/youtube/v3/docs)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [YouTube](https://www.youtube.com/)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [YouTube resource data and action results, typically JSON, with text guidance when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include guidance for oo CLI actions; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
