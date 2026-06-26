## Description: <br>
OpenClaw AgentOS onboarding bootstrapper for initializing, diagnosing, upgrading, repairing, and health-checking OpenClaw setups; installing baseline skills; adding web search and skill discovery; setting up HOT/WARM/COLD memory; creating an Obsidian-friendly Markdown knowledge base; configuring Agent teams; establishing self-evolution workflows; and reducing context pollution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xb19960921](https://clawhub.ai/user/xb19960921) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to bootstrap or maintain a personal AgentOS, including safe setup planning, skill installation guidance, memory and knowledge-base structure, health checks, and repair workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose installs and create local setup files. <br>
Mitigation: Use plan-only mode when changes are not desired, and require explicit confirmation before writes, installs, paid actions, or unknown-source skill use. <br>
Risk: Recommended skills or tools may require sensitive credentials such as API keys. <br>
Mitigation: Mark API-key-dependent skills before configuration and do not write secrets into generated reports, templates, or public skill material. <br>
Risk: External npm, ClawHub, GitHub, or ZIP sources may not be appropriate for every environment. <br>
Mitigation: Review each source before approval, prefer allowlisted ClawHub packages, and manually confirm non-ClawHub installs. <br>


## Reference(s): <br>
- [OpenClaw Agent Onboarding on ClawHub](https://clawhub.ai/xb19960921/openclaw-agent-onboarding) <br>
- [Skill Baseline](references/skill-baseline.md) <br>
- [Memory Architecture](references/memory-architecture.md) <br>
- [Knowledge Base](references/knowledge-base.md) <br>
- [Agent Team Profiles](references/agent-team.md) <br>
- [Self-Evolution Workflow](references/self-evolution.md) <br>
- [Health Checks](references/health-checks.md) <br>
- [Context Hygiene](references/context-hygiene.md) <br>
- [Safety Policy](references/safety-policy.md) <br>
- [Obsidian](https://obsidian.md) <br>
- [nuwa-skill](https://github.com/alchaincyf/nuwa-skill) <br>
- [darwin-skill](https://github.com/alchaincyf/darwin-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown plans and reports with command snippets, JSON diagnostic output, and generated setup files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose installs or local file creation; risky writes, installs, paid actions, and unknown-source skills require explicit confirmation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
