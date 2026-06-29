## Description: <br>
Helps text-only agents answer image questions by calling a configured BYOK multimodal API when native image input is unavailable or the user requests a configured vision model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzfly256](https://clawhub.ai/user/zzfly256) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route image description, analysis, extraction, and OCR-style questions from text-only models to a configured multimodal provider. It is intended for BYOK workflows where the user controls the upstream Anthropic or OpenAI-compatible endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images and prompts are sent to the configured upstream multimodal API provider. <br>
Mitigation: Use the skill only with intended providers, and avoid private or sensitive images unless sharing them with that provider is acceptable. <br>
Risk: API keys may be exposed if stored directly in the configuration file. <br>
Mitigation: Prefer environment-variable references for credentials and restrict configuration file permissions when secrets are stored on disk. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zzfly256/multimodal-image-understanding) <br>
- [Configuration schema reference](references/config-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text model response on stdout; JSON-formatted errors on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided image input, prompt text, and BYOK provider configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
