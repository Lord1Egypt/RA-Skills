## Description: <br>
Configure OpenClaw to use Google Vertex AI Gemini models so normal OpenClaw startup, Gateway service startup, and TUI usage all work without manual shell setup, and keep the Gateway service aligned with the globally installed npm OpenClaw binary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bhrum](https://clawhub.ai/user/bhrum) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure or repair OpenClaw so Vertex AI Gemini models work through normal CLI, Gateway service, and TUI startup paths. It guides Google Cloud ADC setup, OpenClaw model defaults, shared environment wiring, auth profile repair, Gateway reinstall hygiene, and end-to-end verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to modify local OpenClaw config, shared environment, auth profile, and Gateway service files. <br>
Mitigation: Back up ~/.openclaw before applying changes and review proposed edits before execution. <br>
Risk: Credential setup can expose secrets if a real API key is written into local configuration. <br>
Mitigation: Prefer gcloud ADC and keep the <authenticated> placeholder instead of storing a plaintext secret unless the storage risk is understood. <br>
Risk: A Gateway service installed from a different OpenClaw binary can cause confusing TUI or service failures. <br>
Mitigation: Verify the active openclaw binary and reinstall or restart the Gateway service from that same binary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bhrum/openclaw-vertex-setup) <br>
- [Google Vertex AI generateContent endpoint](https://aiplatform.googleapis.com/v1/projects/{project}/locations/global/publishers/google/models/{model}:generateContent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, dotenv, and YAML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to local OpenClaw config, shared environment files, auth profile files, and Gateway service configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
