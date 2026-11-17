## Description:

OpenClaw Model Switch helps agents switch between configured OpenClaw AI models and add new provider configurations using local scripts and guided prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamwg2025](https://clawhub.ai/user/williamwg2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to view, switch, and add local AI model configurations for providers such as Gemini, GPT, Claude, Qwen, Kimi, MiniMax, GLM, DeepSeek, and custom endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change local OpenClaw model configuration.

Mitigation: Back up ~/.openclaw/openclaw.json before use and review the resulting configuration after switching or adding a model.

Risk: Provider API keys may be saved in plaintext in ~/.openclaw/openclaw.json.

Mitigation: Use this only where local plaintext config storage is acceptable, keep the file out of version control, and set owner-only permissions such as chmod 600.

Risk: Restarting the OpenClaw gateway can briefly interrupt active service.

Mitigation: Run model switches during an acceptable maintenance window or after confirming no critical sessions are active.

Risk: Optional README recommendations include unpinned npx installs for other skills.

Mitigation: Review and pin external install commands before running them.

## Reference(s):

- [Openclaw Model Switch on ClawHub](https://clawhub.ai/williamwg2025/skills/openclaw-model-switch-2)
- [README_EN.md](artifact/README_EN.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify local OpenClaw configuration files and restart the OpenClaw gateway when the user runs the scripts.]

## Skill Version(s):

0.1.3 (source: server release metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
