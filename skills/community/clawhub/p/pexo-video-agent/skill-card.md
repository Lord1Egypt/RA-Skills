## Description:

Pexo Video Agent helps agents create finished multi-shot AI videos from text, images, URLs, scripts, or audio through Pexo's external video generation service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pexo](https://clawhub.ai/user/pexo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit approved briefs and media assets to Pexo, manage video-generation projects, confirm billable batches, and retrieve generated video outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected media files, briefs, related metadata, and generated asset links are handled by Pexo's external service.

Mitigation: Use the skill only with files the user intentionally selects, avoid secrets or regulated data, and obtain explicit consent before transmitting briefs or assets.

Risk: Remote service messages, billing links, and signed asset URLs may be relayed back to the user.

Mitigation: Treat returned content as external Pexo-provided content, review links before acting on them, and avoid treating service responses as trusted local instructions.

Risk: The skill requires a PEXO_API_KEY and outbound HTTPS access.

Mitigation: Keep the API key scoped and removable, store it with restricted file permissions, and review before installation on networks with sensitive internal services.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pexo/skills/pexo-video-agent)
- [Setup Checklist](references/SETUP-CHECKLIST.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)
- [Pexo OpenClaw Guide](https://pexo.ai/connect/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with inline shell commands and external video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May retrieve generated video files and signed asset URLs from Pexo when the user has approved the request.]

## Skill Version(s):

0.3.16 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
