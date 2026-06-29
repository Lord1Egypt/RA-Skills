## Description: <br>
Audits Makefiles for build correctness, portability, and recipe duplication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Makefile changes, build automation, CI/CD updates, and portability improvements before committing or releasing them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Makefile and build automation triggers may activate the skill outside an intended audit. <br>
Mitigation: Use the skill only for explicit Makefile review requests or narrowly scoped build automation audits. <br>
Risk: The artifact documents an apply mode that can modify executable build automation. <br>
Mitigation: Inspect proposed diffs before applying changes and avoid apply mode unless the reviewer is comfortable changing Makefile behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-pensive-makefile-review) <br>
- [Pensive plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with findings, file references, command snippets, and approval recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are organized by context, dependency analysis, duplication candidates, portability issues, missing targets, and recommendation.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
