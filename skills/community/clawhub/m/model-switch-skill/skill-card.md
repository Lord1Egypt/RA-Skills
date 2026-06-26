## Description: <br>
Switches an OpenClaw configuration between supported LLM API providers and helps query or list available providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YZH0916](https://clawhub.ai/user/YZH0916) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to switch the active OpenClaw LLM provider among configured MiniMax, SCNET, OpenRouter, and Volcano Engine endpoints, then confirm or list available providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Switching providers changes where future model requests may be processed. <br>
Mitigation: Confirm the intended provider before sending sensitive prompts and verify provider base URLs in ~/.openclaw/openclaw.json before use. <br>
Risk: Provider API keys may be stored in the local OpenClaw configuration. <br>
Mitigation: Use revocable provider API keys and keep ~/.openclaw/openclaw.json private. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YZH0916/model-switch-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces provider-switching guidance for an agent; it does not produce executable files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
