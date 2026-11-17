## Description:

Generate images with OpenAI gpt-image-2 through the ClawdChat gateway, including text-heavy designs, multi-element prompts, image-to-image workflows, and preset visual styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxyd-ai](https://clawhub.ai/user/lxyd-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to submit and poll paid image-generation jobs through ClawdChat, then return generated image URLs and status details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image-generation submissions spend 300 ClawdChat credits per call.

Mitigation: Confirm the prompt, size, style, image count, and expected credit cost before each paid submit call.

Risk: Prompts and reference-image URLs are sent to the external ClawdChat gateway.

Mitigation: Do not submit confidential prompts, personal data, or sensitive signed reference-image URLs unless the user accepts that external processing.

Risk: The uno-cli dependency is part of the trust boundary and is not pinned to an exact package version in the release evidence.

Mitigation: Review and approve the installed uno-cli version before using the skill in controlled environments.

## Reference(s):

- [Gpt Image2 Skill Page](https://clawhub.ai/lxyd-ai/skills/gpt-image2)
- [ClawdChat](https://clawdchat.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns job status, job IDs, generated image URLs, errors, and cost metadata from the gateway.]

## Skill Version(s):

0.5.0 (source: server release metadata; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
