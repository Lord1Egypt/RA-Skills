## Description: <br>
Evaluate Claude skill quality through auditing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to audit Claude skills for structure, quality, activation reliability, token efficiency, and tool integration, then prioritize improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit and benchmarking examples may execute tools discovered from skills without clear trust boundaries. <br>
Mitigation: Run examples only against trusted skills and repositories, or use a sandbox with no secrets after reviewing discovered tool paths and commands. <br>
Risk: Audit findings and improvement plans may be incomplete or misleading if accepted without review. <br>
Mitigation: Review proposed changes, scan skills before deployment, and verify fixes with the relevant audit or compliance checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-abstract-skills-eval) <br>
- [Source homepage from metadata.openclaw](https://github.com/athola/claude-night-market/tree/master/plugins/abstract) <br>
- [Evaluation criteria](modules/evaluation-criteria.md) <br>
- [Evaluation framework](modules/evaluation-framework.md) <br>
- [Evaluation workflows](modules/evaluation-workflows.md) <br>
- [Troubleshooting](modules/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask the agent to read skill files and propose audit or improvement steps.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release evidence; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
