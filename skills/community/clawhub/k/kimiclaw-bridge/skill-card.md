## Description: <br>
KimiClaw Bridge helps configure OpenClaw, Claude Code, and coding agents to use Kimi K2.5 through an Anthropic-compatible API backend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jack-yang-ai](https://clawhub.ai/user/jack-yang-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure OpenClaw, Claude Code CLI, or spawned coding agents so requests are routed to Kimi K2.5 using Anthropic-compatible settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Routing OpenClaw or Claude Code traffic to Kimi sends prompts, code, and generated outputs to an external provider. <br>
Mitigation: Install only when that routing is intended, and prefer per-task configuration unless Kimi should be the default backend. <br>
Risk: Kimi API keys may be exposed through committed configuration files, shell history, or logs. <br>
Mitigation: Use a dedicated API key, keep secrets out of openclaw.json when possible, and avoid recording keys in shell history or logs. <br>


## Reference(s): <br>
- [Kimi Code Console](https://www.kimi.com/code/console) <br>
- [Kimi Coding API Base URL](https://api.kimi.com/coding) <br>
- [Kimi Coding Messages Endpoint](https://api.kimi.com/coding/v1/messages) <br>
- [ClawHub Skill Page](https://clawhub.ai/jack-yang-ai/kimiclaw-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [Configuration instructions, Shell commands, Code, API Calls, Guidance] <br>
**Output Format:** [Markdown with JSON, bash, curl, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes provider configuration examples, environment variable setup, API endpoint details, and setup cautions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
