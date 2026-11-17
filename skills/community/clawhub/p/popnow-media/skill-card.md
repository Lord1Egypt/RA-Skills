## Description:

Create or edit images, videos, music and voiceovers with PopNow, including model discovery, exact USD quotes, approved generation and task status. Use for requested media creation with the PopNow API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyuminjo](https://clawhub.ai/user/kyuminjo)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Agents use this skill to create or edit images, videos, music, and voiceovers on request. They can discover model options, present an exact maximum price for approval before generation, and return task status and output links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media generation can charge the separate prepaid API USD balance.

Mitigation: Present the exact maximum USD quote and get explicit approval for each task; use a dedicated API key with model and spending limits.

Risk: Prompts and reference media are sent to PopNow and generation providers, and host logs may retain command inputs and results.

Mitigation: Avoid sensitive content, do not include credentials in prompts, and review PopNow's privacy policy before submitting material.

## Reference(s):

- [PopNow Documentation](https://popnow.ai/docs)
- [PopNow Task Documentation](https://popnow.ai/docs/tasks)
- [PopNow Privacy Policy](https://popnow.ai/privacy)

## Skill Output:

**Output Type(s):** [Images, Video, Music, Speech, Guidance]

**Output Format:** [Generated media returned through output links; workflow guidance in Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation is submitted only after approval of the exact quoted maximum USD charge; the helper returns links and does not download generated files.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
