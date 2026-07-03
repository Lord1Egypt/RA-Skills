## Description: <br>
Sling (getsling.com) skill for searching and reading Sling data through the OOMOL oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect Sling schedules, shifts, users, groups, tasks, and calendar events through an already connected OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sling responses can expose sensitive schedule, user, group, task, and calendar data from the connected OOMOL account. <br>
Mitigation: Install and use the skill only when those Sling queries are intended, and avoid invoking it for ambiguous Sling mentions. <br>
Risk: Authentication, connection, scope, credential, or billing failures can interrupt connector access. <br>
Mitigation: Use the documented setup and recovery steps only after a matching command failure, rather than proactively opening login or connection flows. <br>


## Reference(s): <br>
- [ClawHub Sling skill page](https://clawhub.ai/oomol/skills/oo-sling) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Sling homepage](https://getsling.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live Sling connector schemas before actions; current artifact actions are read-only get and list operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
