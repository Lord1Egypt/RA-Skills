## Description: <br>
Test skills via TDD in fresh subagents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to test agent skills in fresh subagent conversations, compare baseline and with-skill behavior, and document rationalization or regression results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Test logs may include complete prompts and model responses, which can expose secrets or private production data if such data is used in scenarios. <br>
Mitigation: Use synthetic or sanitized scenarios for testing and review logs before storing or sharing them. <br>
Risk: Optional automation templates may be adapted into runnable scripts that generate or analyze test artifacts. <br>
Mitigation: Review any automation derived from the templates before execution and keep it scoped to non-sensitive test data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/nm-abstract-subagent-testing) <br>
- [Metadata Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract) <br>
- [Testing Patterns](modules/testing-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with example prompts, test logs, shell snippets, and optional code templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces testing plans, scoring templates, and documentation guidance; it does not execute tests by itself.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
