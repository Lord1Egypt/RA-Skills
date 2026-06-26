## Description: <br>
OpenClaw 故障排查 - 常见问题解决方案。适合：遇到问题的用户、运维人员。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and operators use this skill to diagnose common installation, connection, model, runtime, database, and configuration issues. It provides Chinese-language troubleshooting guidance with commands and checklists for manual recovery workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manual recovery commands can terminate processes, reset configuration, or erase local OpenClaw data if copied without review. <br>
Mitigation: Confirm the target process before kill -9, back up OpenClaw data before database resets, and understand that configuration resets may remove local settings. <br>
Risk: Troubleshooting workflows can expose tokens, API keys, logs, or support details if shared carelessly. <br>
Mitigation: Protect credentials and verify the listed support contact before sharing logs, credentials, payments, or remote access. <br>


## Reference(s): <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [ClawHub release page](https://clawhub.ai/yang1002378395-cmyk/openclaw-troubleshoot-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and troubleshooting checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language troubleshooting guide; commands are intended for user review before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
