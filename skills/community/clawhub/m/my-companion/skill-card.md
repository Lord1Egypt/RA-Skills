## Description: <br>
My Companion is a bilingual AI virtual companion for entertainment-oriented chat, contextual illustration generation, memory, and personality customization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanbihai](https://clawhub.ai/user/ryanbihai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for entertainment chat with a customizable virtual companion that can remember preferences, switch personalities, and attach a context-matched illustration to each conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plaintext memory files can persist sensitive conversation details and bundled memory may contain prior state. <br>
Mitigation: Clear bundled memory before installation, review what the skill writes, and avoid storing health, identity, financial, or intimate details. <br>
Risk: The skill can use USER.md personalization, image-generation network calls, and Weixin message sending. <br>
Mitigation: Enable the skill only after confirming those integrations are expected, authorized, and acceptable for the deployment environment. <br>
Risk: Entertainment companion behavior may be mistaken for emotional or mental health support. <br>
Mitigation: Keep the entertainment-purpose disclaimer visible and direct users to professional support for mental health needs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ryanbihai/my-companion) <br>
- [Quickstart](artifact/QUICKSTART.md) <br>
- [Setup Guide](artifact/docs/SETUP.md) <br>
- [Customization Guide](artifact/docs/CUSTOMIZATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Conversational text with generated illustration prompts and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send messages through the configured Weixin channel and may update plaintext memory files.] <br>

## Skill Version(s): <br>
2.7.1 (source: server release metadata and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
