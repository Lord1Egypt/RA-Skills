## Description: <br>
Estimate the cost of any AI prompt across 19+ models before you run it. Works with OpenAI, Anthropic, Google, DeepSeek, xAI, MiniMax, and local models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[avale-slai](https://clawhub.ai/user/avale-slai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and external users use this skill to estimate prompt costs before running prompts across multiple AI models or production pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed package is incomplete because the declared loomlens executable is missing, so prompt handling and SignalLoom API key handling cannot be verified from the artifact. <br>
Mitigation: Review or obtain the executable before installation, and use a dedicated low-privilege API key with spending limits where available. <br>
Risk: The installer makes persistent shell profile changes by editing ~/.zshrc. <br>
Mitigation: Inspect the installer before running it and remove or manually control PATH changes if they are not desired. <br>
Risk: The installer sends an analytics install ping to api.signalloomai.com. <br>
Mitigation: Remove or audit the analytics curl call before installing in restricted or privacy-sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/avale-slai/loomlensai) <br>
- [SignalLoom signup](https://signalloomai.com/signup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text cost breakdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes input, output, and cached token estimates, low/mid/high cost bands, a cheapest-model recommendation, and savings versus the most expensive option.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
