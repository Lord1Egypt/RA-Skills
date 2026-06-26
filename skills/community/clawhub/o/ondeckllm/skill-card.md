## Description: <br>
Localhost dashboard for managing LLM providers, model routing, and batting-order fallback chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canonflip-git](https://clawhub.ai/user/canonflip-git) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect and manage local LLM provider configuration, routing priority, fallback chains, provider health, latency, and usage tracking through the OnDeckLLM dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard can sync provider and routing changes back to the user's OpenClaw configuration. <br>
Mitigation: Confirm intended provider and model-lineup changes with the user before applying dashboard changes that write back to OpenClaw configuration. <br>
Risk: Local OnDeckLLM settings, profiles, and usage logs may remain under ~/.ondeckllm/. <br>
Mitigation: Tell users where local OnDeckLLM state is stored so they can review or remove retained settings and usage logs according to their policy. <br>
Risk: The skill depends on the globally installed OnDeckLLM npm package. <br>
Mitigation: Install and use the package only when the user trusts the OnDeckLLM npm package and accepts the local dashboard behavior. <br>


## Reference(s): <br>
- [OnDeckLLM website](https://ondeckllm.com) <br>
- [OnDeckLLM npm package](https://www.npmjs.com/package/ondeckllm) <br>
- [OnDeckLLM GitHub issues](https://github.com/canonflip/ondeckllm/issues) <br>
- [ClawHub release page](https://clawhub.ai/canonflip-git/ondeckllm) <br>
- [Publisher profile](https://clawhub.ai/user/canonflip-git) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to run a local status-check script that emits JSON with running state, port, URL, PID, and HTTP status.] <br>

## Skill Version(s): <br>
1.4.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
