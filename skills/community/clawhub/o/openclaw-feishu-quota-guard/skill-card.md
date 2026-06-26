## Description: <br>
Use when a user wants OpenClaw itself to diagnose or fix Feishu/Lark quota burn caused by heartbeats, health checks, webhook probes, or overly expensive background runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HerbertWYT](https://clawhub.ai/user/HerbertWYT) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose and reduce unexpected Feishu/Lark quota burn in OpenClaw deployments by reviewing heartbeat settings, webhook or gateway probes, and safe configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The candidate scanner can search broad personal folders and print matching file contents that may include tokens, URLs, or private content. <br>
Mitigation: Run the scanner only with a narrow explicit workspace path and review its output before sharing it. <br>
Risk: The fixer updates the active OpenClaw configuration when run without dry-run mode. <br>
Mitigation: Run with --dry-run first, pass explicit --config and --workspace paths, and keep the generated backup before restarting OpenClaw. <br>
Risk: The installer can replace an existing same-named local skill directory. <br>
Mitigation: Back up any existing openclaw-feishu-quota-guard skill directory before using the installer. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/HerbertWYT/openclaw-feishu-quota-guard) <br>
- [Source Notes](references/source-notes.md) <br>
- [OpenClaw Heartbeat](https://docs.openclaw.ai/heartbeat) <br>
- [OpenClaw Gateway Heartbeat](https://docs.openclaw.ai/gateway/heartbeat) <br>
- [OpenClaw Feishu Channel](https://docs.openclaw.ai/channels/feishu) <br>
- [OpenClaw Skills](https://docs.openclaw.ai/skills) <br>
- [Bilibili quota-burn background video](https://www.bilibili.com/video/BV1fvcuzVEsc/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill recommends dry-run execution first and may produce candidate file paths, matching lines, planned configuration changes, and verification steps.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
