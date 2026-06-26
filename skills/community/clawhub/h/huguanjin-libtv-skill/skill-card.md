## Description: <br>
libtv-skill helps agents route AI image and video generation or editing requests through LibTV sessions and compatible Gemini, Sora, Veo, Grok, Doubao, and Vidu endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huguanjin](https://clawhub.ai/user/huguanjin) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create, edit, monitor, and download AI-generated images or videos from natural-language requests, with optional direct calls to supported image and video providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected media may be sent to external services. <br>
Mitigation: Use the skill only with trusted API endpoints and do not upload confidential or regulated media unless authorized. <br>
Risk: API credentials are required for normal operation. <br>
Mitigation: Use scoped or revocable API keys and avoid exposing secrets in shared command-line environments. <br>
Risk: Generated files may be saved locally. <br>
Mitigation: Confirm output directories before download and handle generated media according to local data handling requirements. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/huguanjin/huguanjin-libtv-skill) <br>
- [LibTV platform](https://www.liblib.tv) <br>
- [Configuration Guide](CONFIG.md) <br>
- [Usage Guide](references/usage-guide.md) <br>
- [Workflow Reference](references/workflows.md) <br>
- [Output Format Reference](references/output-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON script outputs; generated media may be returned as URLs or saved as local files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires API credentials and may produce local image or video downloads.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence; artifact metadata reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
