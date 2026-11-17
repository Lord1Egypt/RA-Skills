## Description:

Use an OOMOL-connected Bluesky account to read profiles and timelines, search posts, and create text posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to read Bluesky profiles and timelines, search posts, and create text posts through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute remote installation code.

Mitigation: Review and approve CLI installation separately, using a verified release.

Risk: Setup may install or update additional agent skills.

Mitigation: Decide whether to allow each additional skill installation or update.

Risk: Creating a post changes the connected Bluesky account, and requests pass through OOMOL.

Mitigation: Review the exact post and retain confirmation before posting.

## Reference(s):

- [Bluesky API documentation](https://docs.bsky.app/)
- [Bluesky](https://bsky.social)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [oo CLI commands with JSON payloads; structured JSON responses summarized as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return Bluesky data; creating a post changes account state and requires confirmation.]

## Skill Version(s):

1.0.5 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
