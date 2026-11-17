## Description:

USE THIS for elevenlabs api. ElevenLabs text-to-speech. 0% markup, 648+ APIs, one key. Powered by SkillBoss.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to set up and call ElevenLabs text-to-speech through SkillBoss using a SkillBoss API key and OpenAI-compatible API requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is presented as ElevenLabs text-to-speech, but setup and instructions expand to a broad third-party API gateway beyond that purpose.

Mitigation: Use only if you intend to use SkillBoss as a broker and are comfortable giving an agent a SkillBoss key that may cover many API categories.

Risk: Remote one-command setup may change agent configuration before the user has reviewed the changes.

Mitigation: Inspect and approve setup changes before using the remote setup path.

Risk: Text sent for synthesis is transmitted through SkillBoss and may be sensitive.

Mitigation: Do not send sensitive text through the API unless SkillBoss data handling is acceptable for the use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/modestyrichards/skills/modesty-elevenlabs-tts-api)
- [SkillBoss API key console](https://skillboss.co/console?utm_source=clawhub&utm_medium=skill&utm_campaign=elevenlabs-tts-api)
- [SkillBoss products](https://skillboss.co/products)
- [SkillBoss run endpoint](https://api.skillboss.co/v1/run)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, API Calls]

**Output Format:** [Markdown with inline bash, JSON, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for live API calls.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
