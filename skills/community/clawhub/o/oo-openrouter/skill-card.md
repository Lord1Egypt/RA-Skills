## Description: <br>
OpenRouter lets agents operate OpenRouter through an OOMOL-connected account for model discovery, account lookups, usage details, and completion requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when they want an agent to inspect OpenRouter account data, list models and providers, or create OpenRouter chat and message requests through the oo CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an OOMOL-connected OpenRouter account, so actions may access account, key, credit, and routing information. <br>
Mitigation: Install it only if OOMOL is an acceptable intermediary for the account and review account-scope expectations before use. <br>
Risk: Write actions can create model usage or credits-related charge records. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running write actions. <br>
Risk: First-time setup may involve remote oo CLI installer commands. <br>
Mitigation: Prefer the official oo CLI installation guide and inspect remote installer scripts before running shell or PowerShell install commands. <br>


## Reference(s): <br>
- [OpenRouter homepage](https://openrouter.ai) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-openrouter) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads; connector responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the oo CLI, OOMOL sign-in, and a connected OpenRouter account; action schemas should be inspected before payload construction.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
