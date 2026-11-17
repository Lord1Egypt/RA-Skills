## Description:

Use this skill to work with Opper through an OOMOL-connected account, including listing models and generating chat completions or messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to list models available through an OOMOL-connected Opper account and request chat completions or messages. Generation requests are billed and non-streaming.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid chat and message generation actions are not identified as write actions, which can make their cost easy to overlook.

Mitigation: Require clear authorization and a spending limit before making paid generation requests.

Risk: The first-time setup instructions can execute a downloaded CLI installer; the installer and connector behavior are unverified.

Mitigation: Review the CLI installation and check its automatic skill-synchronization settings before installing.

Risk: Prompts and request data are processed by OOMOL and Opper.

Mitigation: Send only information that is intended for OOMOL and Opper to process.

## Reference(s):

- [Opper API documentation](https://docs.opper.ai/build/gateway/drop-in-sdks)
- [Opper](https://opper.ai)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Opper on ClawHub](https://clawhub.ai/oomol/skills/oo-opper)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Shell commands]

**Output Format:** [JSON request and response data, with generated text for chat and message requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation requests are billed and non-streaming.]

## Skill Version(s):

1.0.2 (source: frontmatter metadata, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
