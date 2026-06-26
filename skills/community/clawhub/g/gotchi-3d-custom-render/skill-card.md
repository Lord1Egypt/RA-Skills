## Description: <br>
Render custom Aavegotchi 3D images from arbitrary trait and wearable combinations for synthetic or hypothetical gotchi looks, outfit previews, headshots, and full-body images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaigotchi](https://clawhub.ai/user/aaigotchi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn plain-language or structured Aavegotchi trait and wearable requests into custom 3D render artifacts for previews, portraits, and gallery generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Direct JSON render paths can overwrite or delete user-writable files outside the intended render folder. <br>
Mitigation: Prefer the main wrapper that generates paths under Renders, avoid direct hosted or Unity render scripts on untrusted JSON, and keep output and manifest paths allowlisted to a dedicated render directory. <br>
Risk: Local rendering depends on host tools and Unity availability, so missing prerequisites can cause failed or partial renders. <br>
Mitigation: Confirm Node, jq, npm dependencies, and Unity 2022.3.11f1 are installed before using hosted background compositing or Unity fallback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaigotchi/gotchi-3d-custom-render) <br>
- [Publisher profile](https://clawhub.ai/user/aaigotchi) <br>
- [Architecture](references/architecture.md) <br>
- [Request Schema](references/request-schema.md) <br>
- [Input Schema](references/input-schema.md) <br>
- [Presets And Aliases](references/presets.md) <br>
- [Oracle VM Setup](references/oracle-vm-setup.md) <br>
- [Aavegotchi](https://www.aavegotchi.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, JSON, Guidance] <br>
**Output Format:** [PNG image files and JSON manifest, with concise Markdown or shell-command guidance from the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces full-body PNG, headshot PNG, and manifest JSON under the configured render output path.] <br>

## Skill Version(s): <br>
1.1.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
