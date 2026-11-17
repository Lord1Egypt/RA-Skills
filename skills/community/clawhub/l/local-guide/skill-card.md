## Description:

Local Guide - Food & Travel helps an agent search for locally trusted food, lodging, attractions, hot springs, parking, and other travel recommendations while prioritizing official and local-source evidence over commercial review platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pythonmango](https://clawhub.ai/user/pythonmango)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather local recommendations for restaurants, snacks, hotels, attractions, hot springs, shopping, nightlife, coffee shops, and parking. It is intended to produce detailed, source-aware recommendations with location, navigation, pricing, hours, reasons to visit, and practical cautions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback search path can execute attacker-supplied shell input.

Mitigation: Replace shell=True command construction with a safe argument list and treat location, type, and recommendation text as untrusted data before using the fallback with user-provided inputs.

Risk: Search queries and optional Feishu card content may be sent to external services.

Mitigation: Configure Exa and Feishu credentials only in trusted environments, and avoid submitting sensitive locations, contacts, or private travel details unless external disclosure is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pythonmango/skills/local-guide)
- [OpenClaw](https://openclaw.ai)
- [Exa Search Engine](https://exa.ai)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown recommendations, optional Feishu card JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send search queries to Exa and optional Feishu card data to Feishu when those credentials and channels are configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
