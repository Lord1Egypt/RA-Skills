## Description: <br>
Manages multiple OpenAI OAuth accounts in OpenClaw, including account snapshots, switching, quota checks, auto-rotation near exhaustion, and fallback model selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tutouguai1933](https://clawhub.ai/user/tutouguai1933) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to manage several OpenAI Codex OAuth accounts, inspect cached or probed quota state, switch accounts, and fall back to a backup model when OpenAI accounts are unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Quota probing can send OAuth tokens to the URL configured by OPENCLAW_CODEX_USAGE_URL. <br>
Mitigation: Before enabling probing or automation, leave OPENCLAW_CODEX_USAGE_URL unset or set it only to the intended official endpoint. <br>
Risk: The skill stores and propagates OAuth tokens in local OpenClaw account snapshots. <br>
Mitigation: Use it only on trusted machines, back up ~/.openclaw before switching accounts, and treat ~/.openclaw/openai-codex-accounts/ as credential material. <br>
Risk: Automated switching can change active OpenClaw accounts or fallback models during unattended checks. <br>
Mitigation: Validate account status with list --verbose or status first, then use conservative thresholds and an inactivity guard for scheduled automation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tutouguai1933/openclaw-openai-multi-account) <br>
- [ChatGPT usage endpoint used for quota checks](https://chatgpt.com/backend-api/wham/usage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run commands that update local OpenClaw account state and OAuth account snapshots.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
