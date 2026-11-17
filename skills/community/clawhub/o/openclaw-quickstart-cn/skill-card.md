## Description:

Guides Chinese OpenClaw users through installation, domestic AI provider configuration, connection testing, and follow-up troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese users, developers, and operators use this skill to set up OpenClaw, configure DeepSeek, Zhipu, or Qwen API keys, verify connectivity, and identify common setup issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quickstart asks users to run internet-delivered installer code.

Mitigation: Install only from a trusted OpenClaw distribution source and prefer a pinned, versioned package or a download-and-verify flow before execution.

Risk: The quickstart includes an unpinned global package install.

Mitigation: Prefer a pinned OpenClaw package version and review package provenance before installing globally.

Risk: Provider API keys may be exposed during setup.

Mitigation: Treat API keys as secrets, avoid shared terminals, keep configuration files out of version control, and rotate any exposed key.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/yang1002378395-cmyk/skills/openclaw-quickstart-cn)
- [OpenClaw installer endpoint](https://get.openclaw.ai)
- [OpenClaw skills homepage](https://github.com/openclaw-cn/skills)
- [DeepSeek platform](https://platform.deepseek.com/)
- [Zhipu AI platform](https://open.bigmodel.cn/)
- [DashScope console](https://dashscope.console.aliyun.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command blocks, tables, and short troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes provider API key configuration examples; users must substitute their own secrets.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
