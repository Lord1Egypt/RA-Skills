## Description:

PostNitro helps an agent create, import, render, and schedule on-brand carousels, single-image social posts, and short videos across LinkedIn, Instagram, TikTok, and Threads using the PostNitro CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iammuneeb](https://clawhub.ai/user/iammuneeb)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, developers, and agents use this skill to turn topics, articles, X threads, or structured slide JSON into draft or scheduled PostNitro social posts and videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the external @postnitro/cli package and a PostNitro API key with access to connected social accounts.

Mitigation: Install only when the package and account access are trusted, and prefer a scoped, temporary, or environment-provided API key.

Risk: Saved authentication can store the PostNitro API key in plaintext on the local machine.

Mitigation: Prefer the POSTNITRO_API_KEY environment variable or --api-key flag on shared machines, restrict saved config file permissions, and clear saved auth when it is no longer needed.

Risk: SCHEDULED actions can publish live social content to selected accounts at the configured time.

Mitigation: Confirm the target accounts, post content, and scheduled time before scheduling, and use DRAFT when the user is unsure.

## Reference(s):

- [PostNitro Skill Page](https://clawhub.ai/iammuneeb/skills/postnitro)
- [PostNitro Homepage](https://postnitro.ai)
- [CLI Reference](references/cli-reference.md)
- [Skill Examples](examples/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include PostNitro CLI commands that create, render, draft, or schedule social media content through a connected PostNitro account.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
