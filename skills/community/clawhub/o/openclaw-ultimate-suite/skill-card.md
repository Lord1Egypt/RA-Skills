## Description:

OpenClaw 晴晴终极套件 bundles 29 OpenClaw skills and 61 specialized agents for office productivity, life assistance, social media, information gathering, product development, and security review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wd041216-bit](https://clawhub.ai/user/wd041216-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this suite to activate coordinated skills for document work, research, social media workflows, product development, automation, and security-oriented review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic activation can trigger multiple bundled skills and change what work is performed.

Mitigation: Keep automatic activation disabled until the enabled scenarios are reviewed and confirm each high-impact action before execution.

Risk: Feishu delivery can send generated local files outside the local workspace.

Mitigation: Enable Feishu delivery only for approved chats and review file contents and destination before sending.

Risk: The guardian watchdog and rollback behavior can alter a workspace and may affect uncommitted work.

Mitigation: Use the watchdog only on a clean, backed-up workspace and avoid rollback setup where important uncommitted work or secrets are present.

Risk: The IronClaw audit path can submit full file contents to an external API.

Mitigation: Do not scan private or secret-bearing files unless external submission is acceptable; redact sensitive data first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wd041216-bit/skills/openclaw-ultimate-suite)
- [README](artifact/README.md)
- [Quickstart](artifact/docs/QUICKSTART.md)
- [Configuration checklist](artifact/docs/CONFIG_CHECKLIST.md)
- [Auto activation guide](artifact/docs/auto-activation.md)
- [Security guide](artifact/docs/security-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with optional code blocks, shell commands, configuration snippets, file paths, and task reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May activate bundled skills that create local files, run scripts, call external services, or send files to Feishu depending on configuration and user action.]

## Skill Version(s):

3.0.0 (source: evidence release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
