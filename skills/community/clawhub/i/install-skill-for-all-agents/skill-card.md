## Description: <br>
Install or upgrade a ClawHub skill, then make the global copy under the machine's OpenClaw home `skills/` directory the final source of truth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kadbbz](https://clawhub.ai/user/kadbbz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install or upgrade one ClawHub skill and promote the staged copy into the machine-wide OpenClaw skills directory. It is intended for keeping a global skill installation synchronized across agents while preserving backups and installation provenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently replace global agent skills. <br>
Mitigation: Review the target slug before installation, keep backups enabled, and require explicit approval for destructive replacement or cleanup. <br>
Risk: Unchecked slug values may affect recursive file operations. <br>
Mitigation: Use only exact trusted ClawHub slugs without slashes or dot segments, and add strict slug validation plus path containment checks before treating the skill as low risk. <br>


## Reference(s): <br>
- [Script Notes](references/scripts.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kadbbz/install-skill-for-all-agents) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports the target slug, final global path, installed version, install or update method, backup path, staging cleanup status, and blockers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
