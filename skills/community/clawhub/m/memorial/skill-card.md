## Description: <br>
Builds memorial archives for loved ones from text, photos, chat logs, and voice messages, with optional persona reconstruction and local voice cloning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terry-cyx](https://clawhub.ai/user/terry-cyx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and families use this skill to organize memories, chat records, photos, interviews, and voice materials into memorial and persona archives. When voice mode is used, it can prepare local voice training and synthesis workflows for a memorial voice model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice mode can access sensitive family materials, including private chat history and voice messages. <br>
Mitigation: Use the skill only with materials you are authorized to process, prefer manual exports where possible, and run it in a dedicated local environment. <br>
Risk: The WeChat voice workflow can decrypt and enumerate local WeChat data. <br>
Mitigation: Review every command before database decryption, limit the selected chats and speakers, and delete decrypted work directories after use. <br>
Risk: Voice cloning can produce audio that listeners may mistake for the real person. <br>
Mitigation: Confirm consent or legal authority for the speaker voice and clearly label generated audio as synthetic. <br>
Risk: The skill handles emotionally sensitive memorial content and inferred persona responses. <br>
Mitigation: Keep generated responses framed as memory-based inferences and avoid using them as the person speaking for legal, financial, family, or medical decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terry-cyx/memorial) <br>
- [Publisher profile](https://clawhub.ai/user/terry-cyx) <br>
- [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) <br>
- [AgentSkills standard](https://agentskills.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, generated skill files, local shell command workflows, and optional synthesized audio artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local memorial folders, remembrance and persona files, parsed chat summaries, processed audio, voice model files, and synthetic speech outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
