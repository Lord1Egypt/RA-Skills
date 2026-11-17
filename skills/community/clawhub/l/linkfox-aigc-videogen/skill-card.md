## Description:

Generates short AI videos from an input image, optional ending frame, and prompt using supported LinkFox video models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to turn a source image, optional final frame, and prompt into a generated video. Agents can create an asynchronous LinkFox generation task, poll for completion, and return the saved local video path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles reusable LinkFox API keys and phone-based onboarding credentials.

Mitigation: Use securely stored API keys, avoid exposing secrets in shared shell startup files or logs, and rotate credentials if they may have been disclosed.

Risk: The skill can initiate billing or quota purchase flows.

Mitigation: Review plan, payment method, and order details before creating any order, and do not allow unattended purchases.

Risk: Image URLs and prompts are sent to external LinkFox processing services.

Mitigation: Submit only content approved for external processing and avoid sensitive or confidential image URLs and prompts.

Risk: Endpoint environment variables can redirect requests away from the expected LinkFox services.

Mitigation: Do not override LinkFox endpoint environment variables unless the destination is trusted and intentionally configured.

## Reference(s):

- [AI Video API Reference](artifact/references/api.md)
- [Authentication and Billing Onboarding](artifact/references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-aigc-videogen)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown or plain text with local video file paths and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated videos under the session media directory and response JSON under data; generation can take up to 20 minutes.]

## Skill Version(s):

1.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
