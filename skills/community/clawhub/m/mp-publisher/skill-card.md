## Description:

Automates a WeChat official-account article workflow from topic generation through drafting, review, image creation, and draft creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuxixixi](https://clawhub.ai/user/wuxixixi)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators and developers use this skill to coordinate AI-assisted WeChat article production, including topic selection, article drafting, review scoring, image generation, and creation of official-account drafts for manual review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on WeChat and image-generation credentials and stores credential templates in local .env files.

Mitigation: Use least-privilege WeChat credentials, set .env files to owner-only permissions, and enable IP allowlisting before installation or use.

Risk: Image generation can be routed through a configurable DMX_BASE_URL endpoint.

Mitigation: Leave DMX_BASE_URL unset unless the endpoint is trusted and review generated assets before attaching them to drafts.

Risk: The draft-publisher test path prints a prefix of the WeChat access token.

Mitigation: Remove token-prefix logging before operational use and avoid sharing command output from credential checks.

Risk: Automated article drafting can introduce factual or editorial errors before a draft reaches the WeChat account.

Mitigation: Manually review article text, cited facts, generated images, and draft contents before any real publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuxixixi/skills/mp-publisher)
- [Publisher profile](https://clawhub.ai/user/wuxixixi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Files, Guidance]

**Output Format:** [Markdown articles, PNG image files, shell commands, environment-variable configuration, JSON status records, and WeChat draft API requests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates WeChat draft entries rather than live published posts; uses local workspace files and configured WeChat and DMX API credentials.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
