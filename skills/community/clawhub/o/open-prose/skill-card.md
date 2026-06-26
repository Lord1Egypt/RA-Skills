## Description: <br>
OpenProse VM skill pack. Activate on any `prose` command, .prose files, or OpenProse mentions; orchestrates multi-agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simbabuddy](https://clawhub.ai/user/simbabuddy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical users use OpenProse to run, compile, and author `.prose` programs that coordinate multi-agent workflows, spawn subagents, manage workflow state, and produce task artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote `.prose` programs can direct powerful multi-agent workflow execution. <br>
Mitigation: Review remote `.prose` files before running them and install the skill only when this workflow-runner capability is intended. <br>
Risk: Persistent memory can retain information across runs or projects when user-scoped memory is used. <br>
Mitigation: Avoid user-scoped memory unless cross-project persistence is required, and do not place secrets in prompts or persisted memory. <br>
Risk: PostgreSQL mode can expose database credentials to spawned sessions and logs. <br>
Mitigation: Use PostgreSQL mode only with a dedicated low-privilege database and throwaway credentials. <br>


## Reference(s): <br>
- [ClawHub OpenProse Listing](https://clawhub.ai/simbabuddy/open-prose) <br>
- [OpenProse Homepage](https://www.prose.md) <br>
- [Publisher Profile](https://clawhub.ai/user/simbabuddy) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [OpenProse VM Specification](artifact/prose.md) <br>
- [OpenProse Compiler and Validator](artifact/compiler.md) <br>
- [State Management: Filesystem](artifact/state/filesystem.md) <br>
- [State Management: PostgreSQL](artifact/state/postgres.md) <br>
- [OpenProse Help](artifact/help.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown and plain text with optional code blocks, shell commands, configuration snippets, and generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the executed `.prose` program and the agent tools available in the host environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
