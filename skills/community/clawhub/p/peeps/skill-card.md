## Description:

Personal network intelligence for remembering people, finding connections, and drafting introductions with contacts stored locally as plain Markdown files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilyabelikin](https://clawhub.ai/user/ilyabelikin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Peeps to maintain a private local record of people and organizations, retrieve relationship context, find network connections, and draft introductions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive contact and relationship notes are stored as local plaintext files.

Mitigation: Avoid secrets or highly sensitive third-party details, and keep the mind/peeps directory out of shared repositories and sync folders.

Risk: External web searches or image downloads can expose names or relationship context outside the local workspace.

Mitigation: Require explicit user confirmation before web searches or image downloads, and leave image fetching disabled unless the user has accepted the privacy tradeoff.

Risk: Mutable update and install paths can pull unreviewed changes.

Mitigation: Review the fetched source and pin the exact release or commit before installing or updating.

Risk: Automatic housekeeping can silently change the action history.

Mitigation: Use the cleanup behavior only where short retention is acceptable, and review or back up actions before relying on them as records.

## Reference(s):

- [Peeps ClawHub listing](https://clawhub.ai/ilyabelikin/skills/peeps)
- [Publisher profile](https://clawhub.ai/user/ilyabelikin)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [Haah skill](https://github.com/haah-ing/haah-skill)
- [Pages skill](https://github.com/haah-ing/pages-skill)
- [Vibes skill](https://github.com/haah-ing/vibes-skill)
- [Digs skill](https://github.com/haah-ing/digs-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files, plain text responses, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local mind/peeps Markdown files, organization files, configuration, and action queues.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
