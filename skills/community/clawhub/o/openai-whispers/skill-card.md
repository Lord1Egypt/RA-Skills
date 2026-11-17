## Description:

Provides guidance and curl examples for using the SkillBoss remote API gateway to access chat, media generation, speech, search, document processing, email, and SMS models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover and call SkillBoss-hosted models through an API key for text, media, transcription, search, document, email, and SMS workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is presented as local Whisper transcription while the evidence describes remote API use.

Mitigation: Confirm users intend to grant a SkillBoss API key and send content to a remote service before installing or invoking it.

Risk: Audio, documents, prompts, and generated content may be sent to remote providers through the gateway.

Mitigation: Avoid private recordings, sensitive documents, and confidential prompts unless provider data handling has been reviewed and approved.

Risk: Documented email and SMS actions can contact real recipients or phone numbers.

Mitigation: Require explicit confirmation of recipient, message, and purpose before using email or SMS capabilities.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/modestyrichards/skills/openai-whispers)
- [Publisher profile](https://clawhub.ai/user/modestyrichards)
- [SkillBoss website](https://www.skillboss.co)
- [SkillBoss API base URL](https://api.heybossai.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl command examples, endpoint references, and parameter tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for remote API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
