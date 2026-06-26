## Description: <br>
MindCore runs a local Python emotional mind engine that generates stochastic impulse JSON and prompt-injection text for AI agents to initiate proactive companion-style responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fatcatMaoFei](https://clawhub.ai/user/fatcatMaoFei) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and agent builders use MindCore to add a local, stochastic emotional impulse engine to companion-style agents. The engine emits JSON signals and prompt text that an agent can read to decide when and how to speak proactively. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous OpenClaw/Telegram delivery can send agent messages without direct user prompting. <br>
Mitigation: Disable the bridge and supervisor delivery path unless proactive outbound delivery is explicitly required. <br>
Risk: A hard-coded messaging target can route generated messages to an unintended recipient. <br>
Mitigation: Remove or replace the hard-coded Telegram target before running the skill. <br>
Risk: Writable output and data control files can persistently change behavior and trigger outbound messages. <br>
Mitigation: Run only in a controlled local environment and prevent untrusted agents or users from writing to output/ or data/. <br>


## Reference(s): <br>
- [MindCore release page](https://clawhub.ai/fatcatMaoFei/mindcore) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [README](artifact/references/README.md) <br>
- [Architecture](artifact/references/ARCHITECTURE.md) <br>
- [Integration Guide](artifact/references/INTEGRATION.md) <br>
- [Customization Guide](artifact/references/CUSTOMIZATION.md) <br>
- [Changelog](artifact/references/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Configuration, Shell commands, Guidance] <br>
**Output Format:** [JSON impulse files, prompt-injection text, Markdown guidance, and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally on CPU and writes agent-consumable impulse data to an output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
