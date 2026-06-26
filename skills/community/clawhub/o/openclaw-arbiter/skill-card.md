## Description: <br>
Audits installed agent skills and reports resource access such as network use, subprocess execution, file I/O, environment variables, and unsafe operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtlasPA](https://clawhub.ai/user/AtlasPA) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent workspace maintainers use this skill to review installed skills, inspect permission categories, and identify skills that may need manual review or removal before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has authority over a local skills workspace and includes commands that can quarantine or remove installed skills. <br>
Mitigation: Use audit, report, or status first for read-only review, and back up the skills directory before running quarantine, revoke, or protect. <br>
Risk: Policy and protection commands can disable skills when configured or invoked against the wrong workspace. <br>
Mitigation: Pass an explicit --workspace path, review the policy file before enforcement, and verify reported findings before applying destructive actions. <br>


## Reference(s): <br>
- [Openclaw Arbiter on ClawHub](https://clawhub.ai/AtlasPA/openclaw-arbiter) <br>
- [AtlasPA publisher profile](https://clawhub.ai/user/AtlasPA) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Terminal text reports, compact permission tables, status summaries, JSON policy files, and Markdown instructions with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Python 3 and no external package dependencies; commands can target a workspace path.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
