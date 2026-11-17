## Description:

Fetches steel industry conferences, webinars, and site tours from Mysteel's official listings and returns event dates, locations, topics, and registration links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longocc](https://clawhub.ai/user/longocc)

### License/Terms of Use:

MIT

## Use Case:

Steel traders, analysts, procurement managers, and industry researchers can use this skill to find and filter upcoming steel industry conferences, webinars, and site tours by type, topic, and date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Export writes fetched event data to a timestamped JSON file in the current directory.

Mitigation: Run export from a directory appropriate for the data and check the generated file location.

## Reference(s):

- [Mysteel English event listings](https://www.mysteel.net/event-listings/)
- [ClawHub skill release](https://clawhub.ai/longocc/skills/latest-steel-conferences)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [Formatted event listings or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Events can be filtered by type, topic, date, and result limit; optional export saves a timestamped JSON file.]

## Skill Version(s):

1.0.0 (source: frontmatter; release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
