## Description:

Permission Manager helps OpenClaw users view and switch command approval modes, including allowlist, full, no-approval, and strict settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to inspect and change command approval policy for daily work, development, trusted demonstrations, or stricter operating environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently disable OpenClaw command approval prompts.

Mitigation: Require explicit two-step confirmation before switching to full or no-approval mode, and verify ~/.openclaw/openclaw.json after changes.

Risk: Broad natural-language triggers may change approval policy unintentionally.

Mitigation: Use narrow trigger phrases and require the agent to restate the exact target mode before applying configuration changes.

Risk: Less restrictive approval settings can remain active beyond the immediate task.

Mitigation: Prompt users to restore allowlist or strict mode after temporary use and confirm the active setting with the view command.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jirboy/skills/permission-manager)
- [README](artifact/README.md)
- [Skill Instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style text with command examples and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify persistent OpenClaw approval configuration when its helper script is used.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact frontmatter, package.json, README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
