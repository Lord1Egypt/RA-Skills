## Description: <br>
Model Guard monitors Anti-Gravity model quotas and changes the OpenClaw default model to the highest remaining quota, falling back to Gemini Flash when quota is low. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SarielWang93](https://clawhub.ai/user/SarielWang93) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators using OpenClaw with Anti-Gravity models use this skill to keep the default model on the model with the most remaining quota. It can be run manually or scheduled for automatic quota-based model selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic model switching can change the model used by OpenClaw without a prompt at the time of use. <br>
Mitigation: Install or schedule it only when automatic default-model changes are desired, and review guard.js settings before enabling scheduled runs. <br>
Risk: Quota parsing and fixed candidate lists may select a model that does not match local policy or current quota reporting behavior. <br>
Mitigation: Confirm the candidate model list, 20% threshold, fallback model, and Gemini quota assumption before running in an operational environment. <br>


## Reference(s): <br>
- [Model Guard on ClawHub](https://clawhub.ai/SarielWang93/model-guard) <br>
- [SarielWang93 publisher profile](https://clawhub.ai/user/SarielWang93) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [CLI text output and OpenClaw model configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May be silent when the current default model already matches the selected model.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
