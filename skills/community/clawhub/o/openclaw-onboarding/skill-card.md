## Description:

Guide new users to quickly learn and use OpenClaw features, including setup, skill discovery, memory, self-learning, and group chat summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binson1994](https://clawhub.ai/user/binson1994)

### License/Terms of Use:

MIT-0

## Use Case:

New OpenClaw users use this skill to complete a short onboarding flow, learn core commands, configure preferences, discover available skills, use persistent memory, and try group chat summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory guidance can lead users to save secrets, regulated personal data, or confidential company information.

Mitigation: Keep sensitive information out of memory files and review saved memory entries before relying on or sharing them.

Risk: Group chat summarization can expose private or unauthorized conversations.

Mitigation: Summarize only chats the user is authorized to process and limit summaries to the requested group and time window.

Risk: Skill discovery and installation guidance can encourage unattended installation of additional capabilities.

Mitigation: Review each skill source, version, and requested permissions before installation, especially for global installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/binson1994/skills/openclaw-onboarding)
- [README.md](artifact/README.md)
- [OpenClaw quickstart training](artifact/references/training/quickstart.md)
- [Bundled find-skills reference](artifact/references/find-skills/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and onboarding prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language onboarding flow; may propose local configuration, persistent memory files, skill installation, and group chat summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
