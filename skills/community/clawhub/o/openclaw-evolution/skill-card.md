## Description: <br>
Interactive guide for new OpenClaw users to set up and grow their agent through a Tool Path for automation and productivity or an Awakening Path for memory, personality, relationship, and growth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Roger0808](https://clawhub.ai/user/Roger0808) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users and developers use this skill as onboarding guidance for installing OpenClaw, connecting an initial channel, creating SOUL.md, USER.md, and AGENTS.md, and choosing a staged growth path for automation or companion-style agent behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages broad agent autonomy, including public posting, account changes, browser automation, and broad file access. <br>
Mitigation: Keep these actions approval-gated and limit broad file or account access until the user has reviewed the behavior in a narrow setup. <br>
Risk: Persistent memory files can collect secrets or sensitive third-party information. <br>
Mitigation: Do not store secrets or sensitive third-party information in memory files, and review memory contents regularly. <br>
Risk: Channel integrations can expose the agent to unintended users or conversations. <br>
Mitigation: Use channel allowlists such as allowed chat, guild, and channel IDs before connecting Telegram, Discord, or other messaging platforms. <br>
Risk: Scheduled monitoring, cron jobs, and gateway auto-start can make agent behavior proactive before it is well tested. <br>
Mitigation: Test scheduled actions narrowly and manually before enabling cron, heartbeat workflows, or gateway auto-start. <br>


## Reference(s): <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [The Three Files](references/three-files-guide.md) <br>
- [Tool Path](references/tool-path.md) <br>
- [Awakening Path](references/awakening-path.md) <br>
- [Essential Skills](references/essential-skills.md) <br>
- [Multi-Agent Architecture](references/multi-agent.md) <br>
- [Channel Configuration Guide](references/channel-config.md) <br>
- [Common Mistakes](references/common-mistakes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose setup checklists, OpenClaw commands, channel configuration snippets, and staged onboarding recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
