## Description: <br>
Interactive deployment guide for OpenClaw local capabilities that walks through installing the memory stack, vid2md, WeChat plugin, and maintenance cron jobs with confirmation gates between phases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ottoprua](https://clawhub.ai/user/ottoprua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to set up or expand a local OpenClaw instance by selecting components, reviewing prerequisites, applying configuration, and verifying each phase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide proposes local installation commands, repository clones, OpenClaw configuration changes, and gateway restarts. <br>
Mitigation: Review each command before approval and deploy only the selected components that are needed for the local OpenClaw setup. <br>
Risk: qmd memory collections could index unintended folders or sensitive files if pointed at broad paths. <br>
Mitigation: Keep qmd collections pointed only at intended non-secret workspace folders and review collection patterns before indexing. <br>
Risk: Cron jobs, shell startup edits, and WeChat permissions can create persistent automation or access paths. <br>
Mitigation: Record enabled cron jobs, shell rc edits, OpenClaw config changes, and WeChat permissions; restrict WeChat allowed groups and review third-party packages before enabling them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ottoprua/oc-deploy-guide) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Memory Architecture](https://github.com/OttoPrua/openclaw-memory-manager) <br>
- [vid2md](https://github.com/OttoPrua/vid2md) <br>
- [WeChat Plugin](https://github.com/OttoPrua/openclaw-wechat-bot) <br>
- [Memory Manager Skill](https://clawhub.ai/OttoPrua/agent-memory-protocol) <br>
- [Cron Reference Configs](https://github.com/OttoPrua/openclaw-memory-manager/tree/main/cron) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interactive confirmation gates before each selected deployment phase.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
