## Description:

Converts product materials, feature notes, and existing media into structured product explainer video plans, scripts, shots, and AI Hive video generation commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, merchants, and developers use this skill to turn approved product facts, images, videos, and instructions into short product explanation, installation, FAQ, sales demo, and ecommerce-detail video workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent AI Hive API key may be exposed or misused if the runtime environment or local configuration is not trusted.

Mitigation: Review the skill before installation, store credentials only in trusted environments, and prefer isolated dependency and execution environments.

Risk: A custom AI_HIVE_BASE_URL can route API credentials and requests to an untrusted endpoint.

Mitigation: Use the default AI Hive endpoint unless a custom endpoint is deliberately trusted, and avoid inheriting AI_HIVE_BASE_URL from untrusted shells or automation.

Risk: Uploaded product images, video, and audio are sent to the configured AI Hive service.

Mitigation: Treat media inputs as service-bound data and avoid uploading sensitive or unapproved product materials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/product-explainer-video-generation)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands; CLI task responses are JSON and generated media may be downloaded as files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI Hive credentials, accepts product media inputs, submits video generation tasks, polls task status, and can download generated results.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact changelog top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
