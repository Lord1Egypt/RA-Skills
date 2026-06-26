## Description: <br>
Control Philips Hue lights/scenes via the OpenHue CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to have an agent inspect and control Philips Hue lights, rooms, and scenes through the OpenHue CLI after pairing with their Hue Bridge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can issue commands that change Philips Hue light or scene state through a paired Hue Bridge. <br>
Mitigation: Pair only with the user's own bridge and confirm the specific lights, rooms, or scenes before making changes. <br>
Risk: The skill depends on an installed OpenHue Homebrew package and CLI binary. <br>
Mitigation: Install only if the user trusts the OpenHue Homebrew package and intends the agent to control the Hue Bridge. <br>


## Reference(s): <br>
- [OpenHue CLI](https://www.openhue.io/cli) <br>
- [ClawHub Skill Page](https://clawhub.ai/steipete/openhue) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the OpenHue CLI and may produce commands for discovering bridges, setup, reading lights, rooms, and scenes, and changing light or scene state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
