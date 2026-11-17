## Description:

ohmytoken tracks LLM token counts and visualizes usage as real-time pixel art at ohmytoken.dev.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x5446](https://clawhub.ai/user/0x5446)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to observe LLM usage by sending model names and input/output token counts to ohmytoken.dev, where the usage is visualized as a pixel-art dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model names and input/output token counts are sent to ohmytoken.dev after LLM calls and can reveal usage patterns in some work environments.

Mitigation: Install only where sharing those metrics with ohmytoken.dev is acceptable.

Risk: Storing the ohmytoken API key in project configuration can lead to accidental exposure through version control.

Mitigation: Use the OHMYTOKEN_API_KEY environment variable for configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0x5446/skills/ohmytoken)
- [ohmytoken Dashboard](https://ohmytoken.dev)
- [Support Issues](https://github.com/0x5446/ohmytoken-oss/issues)

## Skill Output:

**Output Type(s):** [API calls, configuration, guidance]

**Output Format:** [JSON over HTTPS with Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends model name, prompt token count, and completion token count after LLM calls when configured with an ohmytoken API key.]

## Skill Version(s):

2.0.3 (source: server release evidence and artifact configuration)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
