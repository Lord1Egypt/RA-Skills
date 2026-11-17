## Description:

Search and browse the MusicBrainz music encyclopedia (artists, releases, recordings, labels, works), fetch Cover Art Archive images, resolve musicbrainz.org URLs, and — with OAuth configured — submit your own tags, ratings, and collection edits. Use when the user asks about music metadata, discographies, album/artist/recording details, MBIDs, cover art, or wants to tag/rate music on MusicBrainz.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to find and inspect music metadata, discographies, MusicBrainz identifiers, and cover art. With OAuth configured, it can also submit user-approved tags, ratings, and collection edits to the user's MusicBrainz account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth-enabled actions can change the user's MusicBrainz tags, ratings, or collection.

Mitigation: Configure OAuth only when account edits are needed, review each confirmation preview, and submit only after user approval.

Risk: The security review did not cover external server code or setup.

Mitigation: Review the server implementation and deployment configuration separately before enabling OAuth writes.

## Reference(s):

- [MusicBrainz](https://musicbrainz.org)
- [Clawhub skill release](https://clawhub.ai/chrischall/skills/musicbrainz-mcp)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Structured MusicBrainz lookup results, cover art URLs, and account-change previews or receipts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only lookups need no credentials; account edits require OAuth and user confirmation.]

## Skill Version(s):

1.3.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
