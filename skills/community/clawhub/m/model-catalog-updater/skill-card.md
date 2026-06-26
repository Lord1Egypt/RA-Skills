## Description: <br>
Query available models from your configured providers and add them to OpenClaw config. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Da-Kaine](https://clawhub.ai/user/Da-Kaine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to fetch model lists from configured OpenClaw providers and add selected models to their OpenClaw configuration with default model metadata and aliases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read OpenClaw provider configuration and use configured credentials to contact provider model-list endpoints. <br>
Mitigation: Install only when that access is intended, prefer the slash command, and review the selected provider before fetching models. <br>
Risk: The skill edits OpenClaw model settings. <br>
Mitigation: Verify the config path and keep the generated openclawworking.json backup so changes can be reversed. <br>
Risk: Fetched provider model IDs may not represent the cost, context window, or modality metadata a user expects. <br>
Mitigation: Review added model entries after the update and adjust aliases, limits, costs, or input capabilities before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Da-Kaine/model-catalog-updater) <br>
- [Project homepage](https://github.com/openclaw/skills/model-catalog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Interactive terminal text and JSON configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates an openclawworking.json backup before writing selected model entries.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
