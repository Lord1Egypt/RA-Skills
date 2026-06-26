## Description: <br>
LoomLens Live opens an OpenClaw sidebar that estimates prompt costs, recommends models across optimized clusters, and can dispatch the next prompt with a selected model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[avale-slai](https://clawhub.ai/user/avale-slai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to estimate LLM prompt costs, compare model fit across clusters, and select an override model before running a prompt. It is especially relevant for teams managing paid model usage or Signal Loom estimate quotas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt contents and API keys may be sent to or stored for use with the Signal Loom estimate flow. <br>
Mitigation: Use a revocable or low-scope Signal Loom API key and avoid running estimates on sensitive prompts unless the provider and endpoint have been reviewed. <br>
Risk: The model override route can affect the next prompt's model selection. <br>
Mitigation: Enable the override route only when it is declared, authenticated, model-allowlisted, and cleared after a single prompt. <br>
Risk: Per-call billing or quota deductions may occur when using API-backed estimates. <br>
Mitigation: Confirm expected billing behavior with users before connecting an API key and monitor quota or billing metadata after estimate calls. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/avale-slai/loomlens-live) <br>
- [Publisher Profile](https://clawhub.ai/user/avale-slai) <br>
- [Signal Loom AI](https://signalloomai.com) <br>
- [Signal Loom Signup](https://signallloomai.com/signup.html) <br>
- [Signal Loom Pricing](https://signallloomai.com/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [OpenClaw sidebar UI, command output text, route JSON, and installation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local cost estimates, model recommendations, quota and billing status, and optional next-prompt model override state.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
