## Description: <br>
Provides a safe OpenClaw configuration preset that reduces token and resource use by changing heartbeat, plugin, sub-agent archive, and inactive-session cleanup settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elontools](https://clawhub.ai/user/elontools) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when setting up or tuning OpenClaw instances to lower heartbeat cost, disable unused communication plugins, archive sub-agent sessions, and prune inactive sessions while avoiding context-pruning and compaction changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The preset persistently changes session maintenance and prunes inactive sessions after 7 days. <br>
Mitigation: Review references/preset-safe.json and back up the current OpenClaw configuration before applying it. <br>
Risk: The preset disables WhatsApp, Discord, Slack, Nostr, Google Chat, iMessage, and Signal plugins. <br>
Mitigation: Keep or re-enable any communication plugins that the OpenClaw instance actively uses. <br>


## Reference(s): <br>
- [OpenClaw ElonTools Optimizer v3 - Safe Edition release](https://clawhub.ai/elontools/openclaw-elontools-optimizer-v3) <br>
- [preset-safe.json](references/preset-safe.json) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, guidance, shell commands] <br>
**Output Format:** [Markdown guidance with JSON configuration preset and gateway command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent OpenClaw configuration changes; review the preset before applying.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
