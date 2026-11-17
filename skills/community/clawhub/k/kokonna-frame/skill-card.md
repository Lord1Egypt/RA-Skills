## Description:

Control KoKonna AI e-ink art frames by uploading images, querying device info, and managing multiple frames.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guooscar](https://clawhub.ai/user/guooscar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send images to configured KoKonna e-ink frames, check frame status, and manage one or more personal display devices through an OpenClaw agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured API keys and uploaded images may be sent to any api_base_url set in the local configuration.

Mitigation: Keep api_base_url set to the official HTTPS endpoint and review configuration changes before running upload or device-info commands.

Risk: Uploaded images may contain sensitive personal, location, or business information.

Mitigation: Review images before upload and avoid sending sensitive content to the KoKonna service.

Risk: The all-devices option can update every configured frame.

Mitigation: Use a specific device name for routine uploads and reserve all-devices operations for deliberate bulk updates.

Risk: Device API keys are stored in a local configuration file.

Mitigation: Restrict access to the configuration file and rotate keys if the file is exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guooscar/skills/kokonna-frame)
- [KoKonna website](https://kokonna.art)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python snippets, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate KoKonna API calls that upload resized images or retrieve frame status when used with configured device API keys.]

## Skill Version(s):

1.2.0 (source: server release evidence, SKILL.md frontmatter, and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
