## Description: <br>
Control a GeekMagic holocube display as an AI emote system, generate holographic sprite kits with Gemini, upload them to the device, and swap expressions based on agent state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thrive-spencerj](https://clawhub.ai/user/thrive-spencerj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators with a GeekMagic HelloCubic-Lite or compatible display use this skill to create emote sprites, upload them to the device, and drive the display from agent session state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scan the local subnet for holocube devices. <br>
Mitigation: Prefer passing a known --ip and run discovery only on trusted local networks. <br>
Risk: The skill can control and clear images on a GeekMagic holocube. <br>
Mitigation: Back up device images before setup and verify the target device before running onboarding or setup. <br>
Risk: The skill can reuse a Gemini API key from OpenClaw config. <br>
Mitigation: Use a dedicated Gemini API key where possible and avoid sharing the config with untrusted workspaces. <br>
Risk: Onboarding can delete existing device images without a clear final confirmation. <br>
Mitigation: Avoid running onboarding against an untrusted or wrong device, and review destructive setup steps before continuing. <br>


## Reference(s): <br>
- [Holocube TOOLS.md Example](references/tools-example.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/thrive-spencerj/holocube-emotes) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Code] <br>
**Output Format:** [Markdown guidance with inline bash commands and Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can generate local sprite image files and send HTTP requests to a configured holocube device.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
