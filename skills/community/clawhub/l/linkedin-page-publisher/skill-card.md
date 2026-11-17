## Description:

Publishes text, image, carousel, video, and article preview posts to a LinkedIn Company Page through LinkedIn's versioned REST Posts API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webtaken](https://clawhub.ai/user/webtaken)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators, developers, and automation engineers use this skill to publish or automate LinkedIn Company Page posts, including text, images, carousels, videos, and article previews. It also guides setup, token acquisition, and troubleshooting for LinkedIn's versioned REST Posts API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OAuth helper requests broader LinkedIn scopes than the posting workflow usually needs.

Mitigation: Reduce requested scopes to the minimum required for the intended workflow, preferably w_organization_social for posting-only use.

Risk: Long-lived access and refresh tokens can be exposed through terminal output, logs, shell profiles, or committed environment files.

Mitigation: Run token acquisition only in a private local session, avoid shared or logged environments, and store tokens in a secret manager rather than plaintext files.

Risk: Running the publisher without dry-run mode can create public Company Page posts.

Mitigation: Use --dry-run to inspect request bodies and require explicit human approval before live publishing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/webtaken/skills/linkedin-page-publisher)
- [Setup guide](references/setup.md)
- [Troubleshooting](references/troubleshooting.md)
- [LinkedIn Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api)
- [LinkedIn Images API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/images-api)
- [LinkedIn Videos API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/videos-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python snippets, JSON dry-run request bodies, and published post URNs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform live LinkedIn API calls when run without dry-run mode]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
