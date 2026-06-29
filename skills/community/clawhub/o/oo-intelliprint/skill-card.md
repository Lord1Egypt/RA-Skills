## Description: <br>
Intelliprint enables agents to search and read Intelliprint print jobs, reusable backgrounds, mailing lists, and mailing list recipients through the OOMOL-connected Intelliprint connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to retrieve Intelliprint operational data from an OOMOL-connected account, including print jobs, reusable backgrounds, mailing lists, and recipients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad routing language may lead the skill to be used for unsupported or state-changing Intelliprint work. <br>
Mitigation: Use the skill for requested Intelliprint read and search tasks, and require explicit confirmation before any unsupported, write, or destructive action. <br>


## Reference(s): <br>
- [ClawHub Intelliprint skill page](https://clawhub.ai/oomol/skills/oo-intelliprint) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Intelliprint homepage](https://www.intelliprint.net) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown with inline bash commands and JSON response details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs agents to inspect live connector schemas before running actions; connector responses include data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
