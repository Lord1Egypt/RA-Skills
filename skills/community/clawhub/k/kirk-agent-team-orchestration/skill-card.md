## Description: <br>
Orchestrate multi-agent teams by defining roles, task lifecycles, handoff protocols, and review workflows for sustained collaboration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate sustained multi-agent workflows with clear role boundaries, shared artifacts, task state transitions, and review gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may involve OAuth tokens, API keys, or other sensitive credentials when agents use external services. <br>
Mitigation: Use only trusted accounts, avoid placing secrets or unrelated private data in prompts or shared folders, and scope credentials to the minimum required access. <br>
Risk: The skill discusses model routing, purchases, and concurrent agent work that can create unexpected spend. <br>
Mitigation: Set spending and concurrency limits before running multi-agent workflows, and assign lower-cost models to mechanical operations work. <br>
Risk: External setup guidance and SkillBoss API Hub usage require separate trust decisions outside the Markdown playbook itself. <br>
Mitigation: Review the external setup guide and SkillBoss API Hub terms before use; install only if those dependencies are acceptable for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/kirk-agent-team-orchestration) <br>
- [Complete setup guide](https://skillboss.co/skill.md) <br>
- [Team Setup](references/team-setup.md) <br>
- [Task Lifecycle](references/task-lifecycle.md) <br>
- [Communication](references/communication.md) <br>
- [Patterns](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions, Shell commands] <br>
**Output Format:** [Markdown guidance with templates, checklists, tables, and inline shell/API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces coordination playbooks and handoff formats; it does not execute code by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
