## Description: <br>
Estimate the cost savings from caching frequently-used prompts across AI models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[avale-slai](https://clawhub.ai/user/avale-slai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to estimate prompt-caching cost savings when repeatedly sending system prompts, prompt templates, or other reusable context across AI model calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer changes shell startup configuration and sends install telemetry without clear disclosure in the skill documentation. <br>
Mitigation: Review install.sh before execution, make shell startup changes manually, and require telemetry to be documented and opt-in before installation. <br>
Risk: The declared promptcache runtime executable is missing from the artifact. <br>
Mitigation: Do not rely on the skill until the publisher includes the executable or updates the package metadata to match the shipped files. <br>
Risk: Prompt-cost analysis may involve sensitive prompts or production credentials. <br>
Mitigation: Avoid using sensitive prompts, real credentials, or proprietary production context with this version. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/avale-slai/promptcache) <br>
- [Signalloom API key signup](https://signalloomai.com/signup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cost-savings estimates depend on the selected model, prompt reuse pattern, and call volume.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
