## Description: <br>
Test-driven behavioral verification for AI agents. Catches silent degradation when agent loads memory but doesn't apply learned behaviors. Use when building agent with persistent memory, testing after updates, or ensuring behavioral consistency across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IvanMMM](https://clawhub.ai/user/IvanMMM) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to create behavioral checks and expected answers that verify an AI agent applies its memory and operating rules consistently across sessions, updates, and restarts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup scripts create or update workspace files for behavioral checklists. <br>
Mitigation: Run setup only from the intended workspace and review the generated PRE-FLIGHT files and AGENTS.md changes before relying on them. <br>
Risk: Behavioral check answers can encode sensitive retained content or permissive agent behaviors. <br>
Mitigation: Exclude credentials and sensitive data unless explicitly approved, and require confirmation for public posts, third-party messages, and ambiguous retained content. <br>
Risk: Persistent behavioral checks may encourage agents to follow stale or incorrect rules. <br>
Mitigation: Review and update checks after memory changes, agent updates, or failed preflight results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/IvanMMM/preflight-checks) <br>
- [README](README.md) <br>
- [Skill Documentation](SKILL.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and generated checklist files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workspace checklist and answer files for agent self-checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: CHANGELOG, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
