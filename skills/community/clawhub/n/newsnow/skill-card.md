## Description:

CLI tool to fetch trending news and hot topics from 66 sources across 44 platforms, returning structured news items with titles, URLs, and metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sorrycc](https://clawhub.ai/user/sorrycc)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agents use this skill to list available news sources and fetch trending items from selected platforms, including machine-readable JSON for downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run an unpinned npm CLI through npx, so executed code may change after review.

Mitigation: Prefer a pinned, preinstalled, reviewed newsnow binary before deployment.

Risk: PRODUCTHUNT_API_TOKEN may be exposed to the CLI environment when using the Product Hunt source.

Mitigation: Provide the token only for Product Hunt requests and scope it according to internal credential handling policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sorrycc/skills/newsnow)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; the invoked CLI can return JSON news data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require npm installation and PRODUCTHUNT_API_TOKEN for the Product Hunt source.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
