## Description: <br>
Record browser and local-file actions once, then replay them without the LLM to reduce AI browsing cost, improve speed, and avoid hallucinated steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laziobird](https://clawhub.ai/user/laziobird) <br>

### License/Terms of Use: <br>
Apache License 2.0 <br>


## Use Case: <br>
Developers and operators use OpenClaw RPA to record browser, HTTP API, Excel, and Word workflows once, then replay them as deterministic local Python and Playwright automation without repeated LLM calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved sessions, cookies, API keys, and generated scripts can contain sensitive credentials. <br>
Mitigation: Use only on trusted single-user machines; treat saved cookie files and generated rpa/*.py files as secrets; prefer environment variables or a secret manager where possible. <br>
Risk: Generated Python can control a browser, call APIs, write files, and carry out recorded purchase-capable workflows with broad local authority. <br>
Mitigation: Review generated rpa/*.py files and intended targets before replay; avoid high-value accounts and shared or untrusted machines. <br>
Risk: Recorded automation can persist and reuse login sessions. <br>
Mitigation: Avoid recording sensitive accounts, keep humans in the loop for 2FA and recovery flows, and rotate or revoke saved sessions when they are no longer needed. <br>


## Reference(s): <br>
- [OpenClaw RPA ClawHub listing](https://clawhub.ai/laziobird/openclaw-rpa) <br>
- [OpenClaw RPA project](https://github.com/laziobird/openclaw-rpa) <br>
- [README](README.md) <br>
- [English skill instructions](SKILL.en-US.md) <br>
- [Playwright templates](playwright-templates.md) <br>
- [API call guide](articles/api-call-guide.md) <br>
- [Auto-login tutorial](articles/autologin-tutorial.en-US.md) <br>
- [Advanced setup](articles/advanced-setup.md) <br>
- [Qwen3-VL](https://github.com/QwenLM/Qwen3-VL) <br>
- [Alpha Vantage daily API documentation](https://www.alphavantage.co/documentation/#daily) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with JSON snippets, shell commands, and generated Python/Playwright scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce and run local Python files, browser automation steps, API requests, screenshots, JSON, Excel, Word, and registry entries.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
