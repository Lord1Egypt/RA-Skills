## Description: <br>
MiroFish Predict helps agents run MiroFish multi-agent simulations to explore future scenarios and produce simulation reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ImL1s](https://clawhub.ai/user/ImL1s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to launch MiroFish simulations, manage the Docker-backed service, and ask follow-up questions about generated reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the MiroFish CLI, a Docker backend, and a Docker image outside this artifact. <br>
Mitigation: Install and run it only when those components are trusted, and stop the Docker backend when finished. <br>
Risk: Simulations require an LLM API key and can consume many tokens. <br>
Mitigation: Use a limited or budget-capped key and start with low simulation rounds before increasing workload. <br>
Risk: Prompts and simulation topics may be sent to the configured LLM provider. <br>
Mitigation: Avoid sensitive prompts or confidential data unless the selected provider and deployment meet the user's requirements. <br>


## Reference(s): <br>
- [MiroFish Predict on ClawHub](https://clawhub.ai/ImL1s/mirofish-predict) <br>
- [MiroFish Project Homepage](https://github.com/666ghj/MiroFish) <br>
- [mirofish-cli npm package](https://www.npmjs.com/package/mirofish-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and narrative guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the mirofish CLI, Docker, and LLM_API_KEY; simulations may consume substantial LLM tokens.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
