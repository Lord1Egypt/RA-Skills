## Description: <br>
Enables openai-codex/gpt-5.4 in OpenClaw through a config-layer patch with verification and rollback guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youxitianguo](https://clawhub.ai/user/youxitianguo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to enable a Codex GPT-5.4 model route when the base GPT-5.4 route is already visible but openai-codex/gpt-5.4 is blocked or missing. It guides them through backing up configuration, merging provider/model/alias/fallback settings, verifying registration, and rolling back if needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow changes local OpenClaw model routing and fallback configuration. <br>
Mitigation: Back up ~/.openclaw/openclaw.json first, merge only the needed fields, and verify the model route with openclaw models list and session_status before relying on it. <br>
Risk: Incorrect endpoint, API, or credential behavior can make model calls fail. <br>
Mitigation: Review the baseUrl, api value, and API key behavior before testing, and roll back the configuration if validation fails. <br>
Risk: OpenClaw configuration field names may vary by version. <br>
Mitigation: Merge the example into the existing openclaw.json structure instead of replacing the whole file. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/youxitianguo/openclaw-codex-gpt54-enable) <br>
- [Publisher profile](https://clawhub.ai/user/youxitianguo) <br>
- [Project homepage](https://github.com/youxitianguo/openclaw-skill-openclaw-codex-gpt54-enable) <br>
- [English documentation](artifact/README.md) <br>
- [Chinese documentation](artifact/README.zh-CN.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for editing ~/.openclaw/openclaw.json and verifying OpenClaw model registration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
