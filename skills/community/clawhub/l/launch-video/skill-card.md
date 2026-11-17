## Description:

Launch Video helps an agent submit a startup or product launch brief, URL, screenshot, or media to Pexo and return a finished launch-ready video with music.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pexo](https://clawhub.ai/user/pexo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn product launch briefs, landing-page URLs, screenshots, or uploaded media into finished launch videos for Product Hunt, landing pages, and launch-day social posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Launch briefs, URLs, screenshots, and media are sent to Pexo's hosted service.

Mitigation: Use only approved input data and avoid uploading confidential or regulated material without approval.

Risk: The skill uses a Pexo API key and local ~/.pexo/config configuration.

Mitigation: Use a dedicated API key and keep the config file private with restrictive permissions.

Risk: Custom PEXO_BASE_URL values can direct requests to a non-default endpoint.

Mitigation: Use the default https://pexo.ai endpoint unless the alternate endpoint is fully trusted.

Risk: The artifact includes invite-code and billing guidance.

Mitigation: Treat invite-code and billing content as commercial messaging, not as a security requirement.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pexo/skills/launch-video)
- [Pexo Homepage](https://pexo.ai)
- [Setup Checklist](references/SETUP-CHECKLIST.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON status data, and plain-text asset URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PEXO_API_KEY and PEXO_BASE_URL; generated video delivery is asynchronous and typically requires polling.]

## Skill Version(s):

0.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
