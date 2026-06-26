## Description: <br>
OpenProse VM skill pack. Activate on any `prose` command, .prose files, or OpenProse mentions; orchestrates multi-agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mondilo1](https://clawhub.ai/user/mondilo1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to run, compile, update, and author OpenProse programs that coordinate multi-agent workflows, persistent state, and reusable agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch and run remote .prose workflows that spawn agents. <br>
Mitigation: Review local, URL, registry, and imported .prose programs before execution, and avoid running untrusted remote programs. <br>
Risk: Workflow prompts, .prose state, persistent memory, and PostgreSQL configuration can expose sensitive information. <br>
Mitigation: Keep secrets out of prompts and persistent state; if PostgreSQL state is enabled, use a dedicated database with limited-privilege credentials. <br>
Risk: The skill can persist local or database state across runs. <br>
Mitigation: Periodically inspect or clean .prose/ and ~/.prose/ state, especially after running third-party workflows. <br>


## Reference(s): <br>
- [Prose homepage](https://www.prose.md) <br>
- [ClawHub skill page](https://clawhub.ai/mondilo1/prose) <br>
- [Publisher profile](https://clawhub.ai/user/mondilo1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline code, command examples, and generated or updated workflow files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .prose workspace state, agent memory, run records, and optional database-backed state when the user selects those modes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
