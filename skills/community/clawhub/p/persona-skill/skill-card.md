## Description: <br>
Explicitly invoked OpenClaw persona lifecycle management for persona initialization, rebuilds, and authorized PERSONA_PROFILE updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tower1229](https://clawhub.ai/user/tower1229) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users install this skill when they want an agent to initialize or rebuild persistent persona files, or to apply explicitly authorized structured updates to PERSONA_PROFILE and managed identity fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persona initialization can persistently rewrite SOUL.md, MEMORY.md, USER.md, and persona/PERSONA_PROFILE.md, and can patch managed IDENTITY.md fields. <br>
Mitigation: Install and invoke the skill only when persistent persona management is intended, and review the named files before confirming any overwrite. <br>
Risk: Persona files can shape future agent behavior after they are written. <br>
Mitigation: Review generated persona files for expected identity, memory, language, and boundary settings before relying on the updated persona. <br>
Risk: Incremental profile updates could be misapplied if an update trigger is treated too broadly. <br>
Mitigation: The artifact requires the current user message to start with the exact PERSONA_PROFILE update trigger and include persona_update_data JSON, and limits incremental writes to IDENTITY.md and persona/PERSONA_PROFILE.md. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tower1229/skills/persona-skill) <br>
- [Project Homepage](https://github.com/tower1229/Zhuang-Yan) <br>
- [Initialization Flow](references/protocols/initialization-flow.md) <br>
- [Drafting Specification](references/protocols/drafting-spec.md) <br>
- [Persona Update Protocol](references/protocols/persona-update.md) <br>
- [Template Pack](references/runtime-context/template-pack.md) <br>
- [SOUL Template](references/runtime-context/SOUL.template.md) <br>
- [Persona Profile Consumption Guide](references/runtime-context/persona-profile-consumption-guide.md) <br>
- [MBTI Lookup Index](assets/mbti/mbti-index.json) <br>
- [MBTI Lookup Script](scripts/mbti-lookup.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, JSON lookup output, and concise text confirmations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js for deterministic MBTI lookup; persistent writes are limited by the skill contract to SOUL.md, MEMORY.md, USER.md, IDENTITY.md, and persona/PERSONA_PROFILE.md.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
