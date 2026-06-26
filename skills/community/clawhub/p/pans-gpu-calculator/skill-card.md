## Description: <br>
Pans Gpu Calculator estimates GPU memory needs, recommends H100, A100, L40S, or A10G configurations, and estimates training or inference costs for AI models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashiming](https://clawhub.ai/user/dashiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, AI infrastructure engineers, and sales engineers use this skill to estimate GPU counts, monthly costs, latency, throughput, and training time for model deployment planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GPU sizing, throughput, latency, and cost estimates use simplified formulas and hard-coded GPU price/performance assumptions. <br>
Mitigation: Validate the formulas and replace price or performance assumptions with current provider data before making purchasing or deployment commitments. <br>
Risk: The skill may lead an agent to run the bundled calculator script with user-provided parameters. <br>
Mitigation: Review the command arguments and calculator output before applying the recommendation to production infrastructure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dashiming/pans-gpu-calculator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and tabular or JSON calculator output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports CLI arguments for model size, training or inference mode, GPU selection, batch size, latency target, token count, comparison mode, and JSON output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
