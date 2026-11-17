## Description:

MBTI Coach helps users assess their MBTI type, track cognitive-function development, plan growth exercises, and receive coaching from different MBTI perspectives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leilei926524-tech](https://clawhub.ai/user/leilei926524-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as a personal MBTI development coach for type assessment, daily cognitive-function exercises, progress tracking, and scheduling growth tasks. Developers or agent operators may also use its scripts to generate progress charts and create Feishu/Lark calendar events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a local personality profile that may contain sensitive self-assessment and development data.

Mitigation: Keep the profile local, restrict file permissions, and avoid adding secrets or unrelated personal data to the profile.

Risk: Calendar features can send scheduling data to Feishu/Lark.

Mitigation: Use calendar integration only with user consent and make the external sharing behavior explicit before creating or listing events.

Risk: The Feishu/Lark helper has unsafe credential handling and command construction according to the authoritative security evidence.

Mitigation: Review and harden the helper before installation: remove or restrict token printing, avoid sourcing untrusted .env files, and fix unsafe python3 -c interpolation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leilei926524-tech/skills/mbti-coach)
- [Feishu Open API](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with optional JSON profile updates, shell commands, calendar API calls, and generated chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local profile JSON file and a radar chart image when the corresponding workflow is used.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
