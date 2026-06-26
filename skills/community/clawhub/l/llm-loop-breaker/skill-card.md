## Description: <br>
Two-layer defense for the OpenClaw gateway that aborts hallucinating LLM streams using entropy analysis and monitors host CPU, memory, and disk exhaustion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hehkcaspar](https://clawhub.ai/user/hehkcaspar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of OpenClaw gateways use this skill to deploy runtime loop detection for LLM streams and host resource monitoring for gateway stability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill modifies the OpenClaw gateway and injects runtime stream-abortion behavior. <br>
Mitigation: Review the injected gateway block and keep the generated backup and uninstall procedure available before restarting the gateway. <br>
Risk: The persistent watchdog can terminate process trees after resource or process-health heuristics fire. <br>
Mitigation: Install only on a dedicated gateway host where false-positive process termination is acceptable and monitor incidents after deployment. <br>
Risk: Incident handling captures host logs and resource metrics. <br>
Mitigation: Confirm workspace permissions, log retention expectations, and sensitivity of retained host logs before installation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hehkcaspar/llm-loop-breaker) <br>
- [OpenClaw ClawHub homepage](https://github.com/openclaw/clawhub) <br>
- [Publisher profile](https://clawhub.ai/user/hehkcaspar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment guidance for a Linux OpenClaw gateway requiring node, python3, bash, psutil, and OPENCLAW_APP_DIR.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
