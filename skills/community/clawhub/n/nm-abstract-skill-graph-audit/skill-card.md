## Description: <br>
Audit Skill() refs; detect hubs, isolates, and dangling targets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to audit Skill() references across a skill marketplace, identify hubs, orchestrators, isolates, and dangling references, and plan composition maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrasing may activate the skill during unrelated skill-audit discussions. <br>
Mitigation: Invoke it explicitly for Skill() graph audits and narrow the review to relevant skill or repository files. <br>
Risk: Graph findings can include false positives from example Skill() references or miss free-text mentions that are outside the parser's scope. <br>
Mitigation: Review reported dangling references and limitations before renaming, retiring, or changing dependent skills. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-abstract-skill-graph-audit) <br>
- [Project homepage from metadata](https://github.com/athola/claude-night-market/tree/master/plugins/abstract) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize graph findings, suggest validation commands, and reference JSON report paths when applicable.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
