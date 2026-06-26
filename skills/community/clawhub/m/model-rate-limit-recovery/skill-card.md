## Description: <br>
Diagnose and recover from model rate limit errors in cron jobs or agent sessions, including ChatGPT usage limits, 429 errors, API key rotation, model fallback, and manual recovery procedures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stefanferreira](https://clawhub.ai/user/stefanferreira) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose OpenClaw cron or agent-session failures caused by model provider rate limits, then apply recovery steps such as model fallback, API key rotation, or manual reruns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys or environment secrets may be exposed while checking provider configuration. <br>
Mitigation: Use a secrets manager or protected environment file, avoid pasting real keys into shell history or shared terminals, and redact environment output before sharing logs. <br>
Risk: Cron patches or recovery reruns may duplicate external actions or incur provider costs. <br>
Mitigation: Review each cron patch and failed-run target before applying updates or rerunning scheduled jobs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/stefanferreira/model-rate-limit-recovery) <br>
- [OpenClaw Model Providers Docs](/concepts/model-providers) <br>
- [API Key Rotation Documentation](/concepts/model-providers#api-key-rotation) <br>
- [Cron Job Management](/tools/cron) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash, JSON5, and shell-script code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes diagnostic checks, cron patch examples, fallback configuration snippets, and recovery script templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
