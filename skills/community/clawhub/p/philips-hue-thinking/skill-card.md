## Description: <br>
Visual AI activity indicator using Philips Hue lights. Pulse red when thinking, green when done. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JesseRod329](https://clawhub.ai/user/JesseRod329) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI assistant users use this skill to show assistant activity through Philips Hue lights, including red thinking or working states and a green done state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed artifact depends on a separate hue executable that was not included in the reviewed files. <br>
Mitigation: Verify the actual hue executable before installing or running the skill. <br>
Risk: The local Hue Bridge credential is stored in the user's home configuration directory. <br>
Mitigation: Keep ~/.config/philips-hue/config.json private and avoid sharing logs or screenshots that expose it. <br>
Risk: Pulse mode may keep running as a background process until stopped. <br>
Mitigation: Use the documented reset command or stop the hue-pulse-loop process when the indicator should end. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JesseRod329/philips-hue-thinking) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Hue CLI setup and status-control commands; pulse mode may start a background process until stopped.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
