## Description: <br>
Handles persona lifecycle management for OpenClaw by initializing or reinitializing a persona after an interview, or by incrementally updating persona profile data when explicitly triggered. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tower1229](https://clawhub.ai/user/tower1229) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent developers use this skill to conduct a structured persona interview, generate runtime persona files, and keep persona profile state aligned through controlled updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persona initialization and update flows can persistently rewrite OpenClaw persona, memory, identity, and user-profile files. <br>
Mitigation: Review the requested operation and keep backups of SOUL.md, MEMORY.md, IDENTITY.md, USER.md, and persona/PERSONA_PROFILE.md before use. <br>
Risk: Included smoke and sync scripts can copy live OpenClaw auth/config state or overwrite the locally installed copy of the skill. <br>
Mitigation: Inspect scripts before running them and avoid running smoke or sync scripts against sensitive or production OpenClaw profiles. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tower1229/persona-skill) <br>
- [Project Homepage](https://github.com/tower1229/Zhuang-Yan) <br>
- [Initialization Flow](references/protocols/initialization-flow.md) <br>
- [Drafting Spec](references/protocols/drafting-spec.md) <br>
- [Persona Update Protocol](references/protocols/persona-update.md) <br>
- [Runtime Context Template Pack](references/runtime-context/template-pack.md) <br>
- [SOUL Template](references/runtime-context/SOUL.template.md) <br>
- [Persona Profile Consumption Guide](references/runtime-context/persona-profile-consumption-guide.md) <br>
- [MBTI Index](assets/mbti/mbti-index.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown files, JSON lookup output, and concise text confirmations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can update SOUL.md, MEMORY.md, IDENTITY.md, USER.md, and persona/PERSONA_PROFILE.md during persona initialization or profile update flows.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
