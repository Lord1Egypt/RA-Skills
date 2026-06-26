## Description: <br>
Animated pixel-art office where agents appear as characters that walk, sit, and interact with furniture in real time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xmanrui](https://clawhub.ai/user/xmanrui) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to launch a local web dashboard and pixel-office view for monitoring agents and sessions. The skill manages setup, updates, server startup, and returns local and LAN access URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install, update, and run a broader OpenClaw dashboard rather than only a pixel-office view. <br>
Mitigation: Install it only when you intentionally want the full dashboard launcher, and review the linked project and npm dependencies before use. <br>
Risk: The workflow can stop processes on port 3000, read local OpenClaw configuration, run a background server, and expose a LAN URL. <br>
Mitigation: Run it in an environment where port 3000 is reserved for this dashboard, local OpenClaw configuration access is acceptable, and LAN exposure is expected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xmanrui/pixel-office) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration, Text] <br>
**Output Format:** [Markdown with inline shell commands and access URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns both local and LAN URLs after starting a background development server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
