## Description: <br>
Manage and synchronize global and agent-specific SOUL definitions using a two-layer template system with automated rebuild scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canonxu](https://clawhub.ai/user/canonxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and administrators who manage OpenClaw agents use this skill to update shared and per-agent SOUL templates and keep generated agent instruction files synchronized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can change persistent SOUL instruction files, including global changes across agents. <br>
Mitigation: Install only when this administrative behavior is intended, back up SOUL and template files first, and review diffs after rebuilding. <br>
Risk: Running the rebuild script may regenerate all affected agent SOUL files. <br>
Mitigation: Inspect the local rebuild script before use and avoid global rebuilds unless broad agent changes are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/canonxu/my-soul-upgrade-skill) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [package.json](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and file path references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may lead users to regenerate persistent SOUL instruction files across one or more agents.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
