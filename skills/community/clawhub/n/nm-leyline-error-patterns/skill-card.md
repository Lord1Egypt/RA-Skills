## Description: <br>
Provides error classification, recovery, and graceful-degradation patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to classify service and agent errors, choose recovery paths such as retry, fallback, graceful degradation, or escalation, and produce actionable debugging guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logging examples may capture sensitive context if copied into production without controls. <br>
Mitigation: Add secret redaction or field allowlists before using the logging patterns in real systems. <br>
Risk: Broad error-handling triggers may surface the skill during ordinary debugging conversations. <br>
Mitigation: Use the skill when general resilience guidance is desired and narrow invocation in contexts where unrelated debugging guidance would be distracting. <br>


## Reference(s): <br>
- [Leyline homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with code and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes reusable error taxonomies, recovery strategies, and logging patterns for review before adoption.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
