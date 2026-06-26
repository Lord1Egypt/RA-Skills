## Description: <br>
First-run setup wizard for new OpenClaw agents that interviews the user, generates tailored workspace files, scaffolds memory, installs recommended crons, and recommends companion skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zurbrick](https://clawhub.ai/user/zurbrick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to initialize or reset an agent workspace through an interactive setup flow. It helps create identity, memory, safety, cron, and companion-skill guidance for a new agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes local setup changes and recommends persistent agent crons, including a daily backup cron that commits workspace changes to git. <br>
Mitigation: Install only for workspaces intended to become OpenClaw agent workspaces, review generated permissions, and approve each cron individually before installation. <br>
Risk: The install script creates memory files and initializes a git repository with an initial commit when the target workspace is not already a repository. <br>
Mitigation: Confirm the target workspace path before running setup and review generated files before approving writes. <br>
Risk: The prompt-injection rule may be overly broad if it prevents the agent from briefly acknowledging security concerns. <br>
Mitigation: Consider editing the rule so the agent can provide brief, safe explanations without revealing protected internal details. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/zurbrick/openclaw-startup) <br>
- [Interview Guide](references/interview-guide.md) <br>
- [Cron Recipes](references/cron-recipes.md) <br>
- [Security Baseline](references/security-baseline.md) <br>
- [Placeholder Map](references/placeholder-map.md) <br>
- [cognition companion skill](https://clawhub.com/skills/cognition) <br>
- [summarize companion skill](https://clawhub.com/skills/summarize) <br>
- [agent-hardening companion skill](https://clawhub.com/skills/agent-hardening) <br>
- [openclaw-backup companion skill](https://clawhub.com/skills/openclaw-backup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, generated workspace Markdown files, shell commands, and JSON-like cron configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces proposed files and setup actions for user approval; install and cron actions should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
