## Description:

Provides agent guidance for using SkillBoss to call OpenAI text-to-speech through an OpenAI-compatible API with a single SkillBoss API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure a SkillBoss API key and call the openai/tts-1 text-to-speech model through SkillBoss for text-to-speech requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TTS prompts and the SkillBoss API key are routed through SkillBoss.

Mitigation: Review SkillBoss terms and privacy posture before use, and avoid sensitive or regulated text unless that review is complete.

Risk: The remote setup instruction is unpinned and can enable broad non-TTS SkillBoss capabilities.

Mitigation: Inspect setup instructions before allowing an agent to follow them, and constrain use to the intended text-to-speech workflow.

Risk: The configured SkillBoss access can expose many unrelated APIs beyond text-to-speech.

Mitigation: Use the key only in environments intended for SkillBoss access, monitor usage, and revoke or rotate the key if scope changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/modestyrichards/skills/modesty-openai-tts-api)
- [Publisher profile](https://clawhub.ai/user/modestyrichards)
- [SkillBoss setup instructions](https://skillboss.co/skill.md)
- [SkillBoss console](https://skillboss.co/console)
- [SkillBoss products](https://skillboss.co/products)
- [SkillBoss API endpoint](https://api.skillboss.co/v1/run)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
