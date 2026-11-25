## Description:

Helps Xiaohongshu creators plan and generate product videos such as Vlogs, unboxings, product experiences, and image-to-video clips through Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External Xiaohongshu creators, buyers, and commerce marketers use this skill to plan and generate product videos for product notes, video posts, and livestream promotion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow asks users to share an API key in chat, which could expose credentials.

Mitigation: Keep the key out of chat; configure it locally through qhkit or QHKIT_TOKEN and use a secure local secret store.

Risk: The release relies on two unpinned packages that may change between installations.

Mitigation: Review the packages and pin trusted versions before installation.

Risk: The security scan was partial because some referenced paths were missing, so it does not provide complete assurance.

Mitigation: Review the setup instructions and available files before installing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-xiaohongshu-viral-video)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Video, Text, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Generated video files and text or Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video model, duration, aspect ratio, language, and media inputs depend on the request and available model options.]

## Skill Version(s):

0.1.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
