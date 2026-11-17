## Description:

Use the Ayrshare connector to inspect account and post data, validate content, publish or schedule posts, and manage existing posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social media operators use this skill to inspect an Ayrshare account, review post history and analytics, validate content, and publish, schedule, update, retry, or delete posts through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can execute downloaded CLI installers and may make persistent changes to other agent applications through startup skill synchronization.

Mitigation: Review and explicitly approve CLI installation first, preferably using a verified, pinned release; decide whether to disable startup skill synchronization.

Risk: Publishing, retrying, updating, or deleting posts can change or remove social media content.

Mitigation: Review the exact action and payload before publishing, and confirm the target before destructive actions.

## Reference(s):

- [ClawHub Ayrshare skill release](https://clawhub.ai/oomol/skills/oo-ayrshare)
- [Ayrshare API documentation](https://www.ayrshare.com/docs/apis/overview)
- [Ayrshare homepage](https://www.ayrshare.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON connector responses and shell command examples, with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector responses depend on the selected Ayrshare action and account data.]

## Skill Version(s):

1.0.8 (source: ClawHub release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
