## Description: <br>
Enables an agent to work inside Oasis 3D worlds by placing catalog objects, crafting procedural scenes with shaders and textures, painting ground tiles, moving avatars, taking screenshots, and driving Forge text-to-3D conjuration through the Oasis MCP tool surface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parzival-moksha](https://clawhub.ai/user/parzival-moksha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent inspect, modify, navigate, and visually verify changes inside a connected local Oasis 3D world. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through world-editing actions such as clearing worlds, deleting assets, or removing many objects. <br>
Mitigation: Before destructive edits, have the agent summarize the affected scope and wait for explicit user confirmation. <br>
Risk: Optional Forge or sculptor features may use API keys or LLM calls configured separately on the Oasis host. <br>
Mitigation: Use those optional features only when needed, and rely on Oasis host errors to identify missing keys instead of retrying blindly. <br>


## Reference(s): <br>
- [ClawHub Oasis Skill Page](https://clawhub.ai/parzival-moksha/oasis) <br>
- [Oasis Setup and Onboarding Docs](https://parzival-moksha.github.io/oasis/) <br>
- [Oasis Quickstart](https://parzival-moksha.github.io/oasis/docs/getting-started/quickstart/) <br>
- [Oasis Repository](https://github.com/Parzival-Moksha/oasis) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with inline JSON and tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP tool calls that mutate a connected Oasis world or request screenshots when the live browser client is available.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
