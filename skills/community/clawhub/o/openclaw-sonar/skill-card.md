## Description: <br>
Local OpenRouter Sonar web search CLI using the user's OpenRouter API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iamjameskeane](https://clawhub.ai/user/iamjameskeane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run local OpenRouter-backed Sonar web search, cited research, model listing, and file output workflows from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries and optional system prompts are sent to OpenRouter and may include sensitive context. <br>
Mitigation: Use a dedicated or revocable OpenRouter API key, and avoid sending secrets, private documents, regulated data, or confidential business context unless that disclosure is approved. <br>
Risk: The CLI can write output to user-supplied file paths. <br>
Mitigation: Check --output paths before running commands to avoid overwriting or storing results in unintended locations. <br>
Risk: Local installation commonly symlinks the cloned script into PATH. <br>
Mitigation: Verify the cloned source before symlinking it into PATH. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/iamjameskeane/openclaw-sonar) <br>
- [OpenRouter API Reference](https://openrouter.ai/docs/api/reference/overview) <br>
- [Bun Runtime](https://bun.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text, Markdown, or JSON output with optional file writes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY and sends queries and optional system prompts to OpenRouter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
