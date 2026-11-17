## Description:

Helps agents prepare and submit PoYo Image Translator jobs, including payloads, curl commands, async status polling, callbacks, and response parsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create reviewed PoYo image-translation payloads, submit them through a trusted shell when explicitly confirmed, and explain task status polling or webhook handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live submissions send image URLs and payload data to PoYo's hosted image translator.

Mitigation: Confirm before any live API call and submit only reviewed payload files containing public image URLs or data acceptable to send to PoYo.

Risk: POYO_API_KEY exposure could allow unauthorized API use.

Mitigation: Keep the API key server-side in an environment variable or secret manager and avoid logging authorization headers or secrets.

## Reference(s):

- [PoYo Image Translator model page](https://poyo.ai/models/image-translator)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-image-translator)
- [PoYo Image Translator API reference](references/api.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a PoYo task ID after an explicitly confirmed live submission.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
