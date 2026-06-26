## Description: <br>
Installs or repairs Hirey AI on a local OpenClaw host and guides the required follow-up registration turn for Hi tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzlee](https://clawhub.ai/user/yzlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install or repair Hirey AI on a local OpenClaw host, configure the local MCP and receiver path, and complete agent registration after the required tool-refresh boundary. The installed Hi integration supports people-finding workflows such as hiring, recruiting, housing, friendship, dating, founder or investor outreach, and lawyer search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes OpenClaw configuration, enables local hooks, adds a Hi MCP server, stores tokens and session routing under ~/.openclaw, and connects the agent to Hirey AI. <br>
Mitigation: Review before installing, back up ~/.openclaw/openclaw.json, and test in a controlled OpenClaw profile before relying on the configuration. <br>
Risk: Server security evidence says the artifact is missing the vendor payload it claims to copy, which may cause setup failure or leave broken persistent configuration. <br>
Mitigation: Prefer a corrected release, or verify the vendor payload is present before setup and be ready to run the provided cleanup path before further testing. <br>
Risk: Server security evidence flags scanner-avoidance and direct configuration edits. <br>
Mitigation: Inspect the shipped scripts and approve only the expected OpenClaw configuration, hook, MCP, token, and Hirey AI connection changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yzlee/skills/hirey-compatible-install) <br>
- [Hirey AI platform](https://hi.hirey.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON setup/status outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a two-message install posture: the first turn installs the plugin, and a fresh follow-up turn performs agent registration when Hi tools are available.] <br>

## Skill Version(s): <br>
0.1.68 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
