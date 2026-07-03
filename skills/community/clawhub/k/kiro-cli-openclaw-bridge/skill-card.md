## Description: <br>
Connects OpenClaw or other OpenAI-compatible clients to Kiro CLI's ACP backend through a local bridge with streaming responses and tool calls. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[luoshixi](https://clawhub.ai/user/luoshixi) <br>

### License/Terms of Use: <br>
CC BY-NC 4.0 <br>


## Use Case: <br>
Developers use this skill to run a local ACP-to-OpenAI bridge so OpenClaw or another OpenAI-compatible client can send requests to Kiro CLI. It is suited to local development workflows where the user controls the project directory and Kiro account being used. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local bridge can give a Kiro agent broad ability to read and write project files and run shell commands as the current user. <br>
Mitigation: Use it only when that authority is intended, run it in a disposable or tightly scoped project directory, and review auto-approval behavior before using it on private repositories or credentialed systems. <br>
Risk: Connecting untrusted clients or channels to the bridge could expose local agent capabilities beyond the intended workflow. <br>
Mitigation: Keep the service bound to 127.0.0.1 and avoid connecting untrusted chat channels or network-accessible clients. <br>
Risk: Prompts, responses, and logs may contain sensitive project or account information. <br>
Mitigation: Treat prompts and logs as sensitive, avoid submitting secrets, and review outputs before relying on or sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luoshixi/skills/kiro-cli-openclaw-bridge) <br>
- [Project homepage](https://github.com/LuoShiXi/kiro-cli-openclaw-bridge) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Kiro](https://kiro.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local bridge guidance assumes kiro-cli is installed, authenticated, and available to the user.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
