## Description: <br>
AI Agents collaboration system for KCC Office v2 - enables autonomous operation and collaboration of office agents (Komi, CEO, CFO, CTO, COO, EDN) with persistent context and self-improvement capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gasol36ai-dev](https://clawhub.ai/user/gasol36ai-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and office automation teams use this skill to initialize and operate a multi-agent office workspace with role-specific responsibilities, shared memory, heartbeat checks, onboarding flows, and coordination scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags broad proactive memory, account-checking, and repository-change authority without enough user controls. <br>
Mitigation: Install in an isolated workspace first and define exactly what agents may read, write, remember, share, and publish before enabling autonomous workflows. <br>
Risk: Heartbeat or cron-style automation can repeatedly check accounts, calendars, notifications, services, or project state. <br>
Mitigation: Do not enable heartbeats, cron automation, email, calendar, social access, credentialed services, API keys, or git push permissions until each permission is explicitly scoped. <br>
Risk: Persistent memory and instruction files can retain sensitive context or alter future agent behavior. <br>
Mitigation: Require explicit approval for memory changes, instruction-file changes, commits, pushes, external messages, and any other persistent changes. <br>
Risk: Setup and lifecycle scripts create or update local workspace files for agent onboarding, status, heartbeat, and shutdown flows. <br>
Mitigation: Review generated files and run scripts only in a disposable or isolated copy before integrating them into an active workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gasol36ai-dev/kcc-office-ai-agents) <br>
- [Publisher profile](https://clawhub.ai/user/gasol36ai-dev) <br>
- [PixiJS documentation](https://pixijs.download/release/docs/index.html) <br>
- [Gemini API documentation](https://ai.google.dev/gemini-api/docs) <br>
- [Web image optimization guidance](https://web.dev/articles/image-optimization) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with bash scripts and configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local agent workspace files, memory files, onboarding state, heartbeat checklists, and status output.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
