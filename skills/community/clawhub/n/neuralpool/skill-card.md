## Description: <br>
Monetize idle LLM API capacity or access 100+ models through a unified OpenAI-compatible API. No GPU required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neuralpool](https://clawhub.ai/user/neuralpool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, API consumers, and node operators use this skill to set up NeuralPool Node, configure upstream LLM providers, and access or provide LLM API capacity through an OpenAI-compatible marketplace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install path runs remote code and installs an unverified executable on the user's machine. <br>
Mitigation: Download the script and binary separately, inspect them, and verify a published checksum or signature before running; avoid piping remote scripts directly into a shell. <br>
Risk: The skill requires sensitive credentials such as a NeuralPool auth token and upstream provider keys. <br>
Mitigation: Use least-privilege credentials where possible, store them locally, and rotate them if the local machine or configuration is exposed. <br>
Risk: The workflow can involve paid usage, settlement, and wallet-based withdrawals. <br>
Mitigation: Confirm pricing, token limits, settlement timing, and wallet details before enabling a node or depositing funds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neuralpool/neuralpool) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/neuralpool) <br>
- [NeuralPool website](https://neuralpool.ai) <br>
- [NeuralPool documentation](https://neuralpool.ai/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a NeuralPool authentication token and local configuration of upstream provider credentials.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
