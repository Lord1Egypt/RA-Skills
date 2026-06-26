## Description: <br>
OpenProse VM skill pack that activates on `prose` commands, `.prose` files, or OpenProse mentions to orchestrate multi-agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy27725](https://clawhub.ai/user/andy27725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run, validate, author, and migrate OpenProse workflows that coordinate subagents, state, and reusable `.prose` programs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote `.prose` programs and imports can cause the agent to execute untrusted workflow instructions. <br>
Mitigation: Review remote program sources and imports before running them; avoid untrusted URLs or registry references. <br>
Risk: The skill can spawn subagents and persist project or user-level state, which may expose sensitive prompts, outputs, or regulated data. <br>
Mitigation: Keep secrets and regulated data out of prompts and persisted memory, prefer project-local state, and clear stored state when it is no longer needed. <br>
Risk: PostgreSQL state can expose database credentials to subagent sessions and logs. <br>
Mitigation: Use dedicated short-lived or limited-privilege PostgreSQL credentials when enabling the experimental database backend. <br>


## Reference(s): <br>
- [OpenProse Homepage](https://www.prose.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/andy27725/prose-andy27725) <br>
- [Publisher Profile](https://clawhub.ai/user/andy27725) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline commands, generated `.prose` code, and workflow execution results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify workspace files and persistent `.prose` state when executing or migrating workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
