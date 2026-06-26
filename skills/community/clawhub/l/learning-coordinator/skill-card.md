## Description: <br>
Coordinates learning signals, pattern promotion, and stage management for self-improving memory by monitoring corrections and preferences to identify emerging patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whoisme007](https://clawhub.ai/user/whoisme007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate self-improving memory workflows, inspect learning stages, identify repeated correction patterns, and manage promotion or demotion of patterns across memory tiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read and create ~/self-improving/learning.md when automatic creation is enabled. <br>
Mitigation: Review the learning rules file before enabling the skill, and set auto_create to false if unexpected local writes are not acceptable. <br>
Risk: The skill imports local adapter code and can use correction or preference adapters to drive learning behavior. <br>
Mitigation: Use only trusted local adapters and review adapter configuration before relying on automatic learning signals. <br>
Risk: Automatic stage adjustment can promote or demote learned patterns based on feedback and configured thresholds. <br>
Mitigation: Review learning statistics and pattern reports before treating promoted patterns as confirmed behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whoisme007/learning-coordinator) <br>
- [Skill homepage](https://clawhub.com/skills/learning-coordinator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance, Python API examples, YAML configuration, and structured learning-status data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or create local learning-rule files under ~/self-improving/ and may query trusted local correction or preference adapters when available.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
