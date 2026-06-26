## Description: <br>
This skill operates TextCortex through an OOMOL-connected account to create non-streaming chat completions and inspect available models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to operate TextCortex through an OOMOL-connected account for chat completions and model lookup tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a connected TextCortex account and may incur API usage when creating chat completions. <br>
Mitigation: Install and run it only when TextCortex access is intended, and confirm cost-sensitive completion requests before execution. <br>
Risk: The create_chat_completion action changes TextCortex state by submitting a completion request with user-provided payload data. <br>
Mitigation: Review the exact payload and expected effect with the user before approving the write action. <br>
Risk: First-time setup may require installing the oo CLI or connecting an OOMOL account. <br>
Mitigation: Run installer and account connection steps only from trusted OOMOL sources and only after an authentication or connection failure requires setup. <br>


## Reference(s): <br>
- [TextCortex homepage](https://textcortex.com/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [TextCortex connection page](https://console.oomol.com/app-connections?provider=textcortex) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the oo CLI; action responses are JSON when commands run with --json.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
