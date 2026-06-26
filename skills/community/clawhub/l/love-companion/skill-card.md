## Description: <br>
Love Companion is a general AI agent skill for romantic roleplay companionship with configurable personas, preset templates, emotional conversation, local memory, and JSON import/export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moyan1638](https://clawhub.ai/user/moyan1638) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI agent users use this skill to create and manage a configurable romantic roleplay companion, including persona setup, preset switching, memory review, and persona configuration import or export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store intimate preferences, emotional states, dates, and relationship-style history in local memory. <br>
Mitigation: Use a dedicated storage directory, avoid saving unnecessary sensitive details, and regularly review or clear memories. <br>
Risk: Configurable storage paths and persona imports can expose users to unwanted local file writes or untrusted imported configuration. <br>
Mitigation: Keep storage in a dedicated directory, avoid path-like scheme names, and import only reviewed JSON configurations. <br>
Risk: Romantic companion roleplay may be mistaken for real relationship support or mental-health support. <br>
Mitigation: Treat outputs as AI-generated roleplay and seek qualified professional help for mental-health concerns. <br>


## Reference(s): <br>
- [Complete command reference](references/commands.md) <br>
- [Detailed usage guide](references/instructions.md) <br>
- [Preset persona templates](references/personas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown conversation with JSON configuration snippets and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local persona, scheme, settings, and memory JSON files under the configured storage directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
