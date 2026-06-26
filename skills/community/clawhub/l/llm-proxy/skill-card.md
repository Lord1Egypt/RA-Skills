## Description: <br>
AI守门人 helps agents manage a local LLM API proxy with multi-provider routing, content safety checks, health monitoring, and service control commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[394286006](https://clawhub.ai/user/394286006) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to start, stop, restart, inspect, and configure a local LLM proxy that forwards requests to multiple providers. It is intended for local service management, provider routing, basic content filtering, request logging, and health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Starting or stopping the proxy can forcibly terminate another local service that is using the configured proxy port. <br>
Mitigation: Before starting, stopping, or restarting the service, confirm that port 18888 or the configured replacement port is not used by an unrelated process. <br>
Risk: Provider API keys may incur cost or expose access if broad keys are used through the proxy. <br>
Mitigation: Use scoped provider API keys with billing limits and rotate or revoke keys if logs, configuration, or shell history may have exposed them. <br>
Risk: The streaming content filter may warn or log risky output without fully blocking every unsafe streamed response. <br>
Mitigation: Treat the content filter as an assistive control, review high-risk responses separately, and do not rely on it as the only safety boundary. <br>
Risk: Local request and service logs can contain sensitive prompts, responses, metadata, or operational details. <br>
Mitigation: Periodically review, protect, or delete logs under the configured log directory when handling sensitive prompts or responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/394286006/llm-proxy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and service status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Manages a local background proxy on the configured host and port; writes local JSONL request logs and service logs.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
