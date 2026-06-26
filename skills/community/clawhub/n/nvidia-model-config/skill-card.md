## Description: <br>
Adds NVIDIA model provider configuration to OpenClaw with SecretRef-based API key handling and bundled model entries for Mixtral, Kimi, Nemotron, and MiniMax. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xli](https://clawhub.ai/user/0xli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add NVIDIA provider and model entries to OpenClaw configs and set up the NVIDIA_API_KEY where the OpenClaw gateway can read it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper can modify OpenClaw configuration and optional user environment or systemd files. <br>
Mitigation: Run with --dry-run first, use --backup before writing, and review generated config or service override changes before enabling them. <br>
Risk: API keys can be exposed if passed on the command line or written inline into shared configuration. <br>
Mitigation: Prefer NVIDIA_API_KEY or a protected gateway environment file, keep env files mode 600, and avoid --inline-key except for short-lived local testing. <br>
Risk: Bundled model entries may not match the user's NVIDIA account entitlements. <br>
Mitigation: Select models that are available to the account and remove or replace entries that return entitlement errors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xli/nvidia-model-config) <br>
- [NVIDIA API endpoint](https://integrate.api.nvidia.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and a Python configuration script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update openclaw.json, write an optional protected environment file, create a systemd user override, and create backup files when the script is executed.] <br>

## Skill Version(s): <br>
1.0.5 (source: server evidence release.version and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
