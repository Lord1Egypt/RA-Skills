## Description:

Lingxi-MindVault scans OpenClaw session files, uses an agent to extract useful memories, and writes task, project, and knowledge entries to user-configured Feishu resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuxiaolong1988](https://clawhub.ai/user/liuxiaolong1988)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users can use this skill to automate memory extraction from completed conversations into their own Feishu task board and documents. It is suited to personal or internal workflows where users intentionally allow session content to be analyzed by an agent and stored in Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill continuously reads unprocessed private OpenClaw conversations for memory extraction.

Mitigation: Install only when this data flow is intentional; avoid sensitive sessions, use fixed session scoping, and add review or redaction before enabling unattended runs.

Risk: Extracted content is written by the main agent to user-configured Feishu resources without tight controls.

Mitigation: Verify all Feishu IDs before enabling cron, use least-privilege Feishu authorization, and review the destination resources regularly.

Risk: The automation is intended to run on a schedule and may process conversations without further prompts.

Mitigation: Run it under an unprivileged account, enable it only for approved workspaces, and monitor failures or unexpected writes through the provided notifications.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/liuxiaolong1988/skills/lingxi-memory)
- [OpenClaw Project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Plain text extraction records and Markdown notification summaries, with shell scripts and environment-variable configuration for execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes extracted L2 task, L3 project, and L4 knowledge items to user-configured Feishu resources; requires OpenClaw, Feishu OAuth, bash, and python3.]

## Skill Version(s):

1.1.15 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
