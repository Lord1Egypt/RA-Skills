## Description: <br>
Pixel Lobster Skill provides a bundled Electron desktop overlay with a pixel art lobster that lip-syncs to OpenClaw TTS speech and guides users through install, configuration, and launch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JoeProAI](https://clawhub.ai/user/JoeProAI) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to set up a local desktop avatar that visually reacts to agent TTS speech. It is useful when a user wants installation, configuration, launch, or tuning guidance for the bundled Pixel Lobster Electron app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional system audio mode can listen to all desktop audio while the app is running, including private calls, media, and notifications. <br>
Mitigation: Keep audioMode set to tts unless broad desktop-audio reaction is intentional, and enable system mode only for sessions where that capture behavior is acceptable. <br>
Risk: The skill runs a local Electron app and fetches its npm dependency on first launch. <br>
Mitigation: Install and launch it only in an environment where running a local Electron application and npm dependency install is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JoeProAI/pixel-lobster) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is centered on a local Electron desktop overlay and its bundled configuration files.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
