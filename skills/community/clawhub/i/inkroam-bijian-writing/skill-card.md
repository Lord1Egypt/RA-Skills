## Description:

Collects a topic, viewpoints, and reference material, calls the Bijian AI writing service, and returns a publish-ready article.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytearch1990-beep](https://clawhub.ai/user/bytearch1990-beep)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to draft public-facing articles for channels such as WeChat public accounts by providing a topic, key viewpoints, and reference material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill loads workspace configuration as shell code.

Mitigation: Use only a trusted, private .bijian_config file, avoid workspace-supplied configs, and do not place shell commands in the config.

Risk: Tokens and article content can be sent to an unpinned API destination.

Mitigation: Keep the API URL pinned to the legitimate Bijian HTTPS endpoint and use a limited-scope token when available.

Risk: Reference material may include confidential notes, credentials, unpublished business material, or private documents.

Mitigation: Do not provide sensitive material unless you intend to send it to Bijian.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytearch1990-beep/skills/inkroam-bijian-writing)
- [Bijian API key page](https://sso.aizmjx.com/home/apikey)
- [Bijian writing space page](https://bj.aizmjx.com/space)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, Writing guidance]

**Output Format:** [Markdown article content with setup commands and generation status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include article title, word count, cover-image status, preview text, and next-step guidance.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
