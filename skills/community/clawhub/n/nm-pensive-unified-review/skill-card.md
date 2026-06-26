## Description: <br>
Orchestrates multi-domain review (code, architecture, tests, security) in a single pass. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to run a unified review across code, architecture, tests, security, and related domains, then consolidate findings into summaries, domain reports, and prioritized action plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may automatically run a local deferred-capture script that stores review-derived details from the reviewed workspace. <br>
Mitigation: Inspect or disable that script path before use, invoke the skill explicitly, and avoid using it on repositories with secrets or sensitive internal findings unless backlog storage is controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-pensive-unified-review) <br>
- [Pensive plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown review reports with findings, evidence, summaries, and prioritized action items.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May coordinate multiple review domains and include evidence appendices; backlog capture behavior should be reviewed before use.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
