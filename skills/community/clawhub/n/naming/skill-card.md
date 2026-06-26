## Description: <br>
Create, test, and choose names for products, features, APIs, files, and systems with constraint-first briefs and collision checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and product teams use this skill to create decision-ready names for products, features, APIs, files, systems, and renames. It helps structure briefs, compare option families, score finalists, and call out collision or rollout risks before a recommendation is made. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent naming memory can contain sensitive product names, codenames, rejected candidates, and launch constraints. <br>
Mitigation: Decide whether local persistence is acceptable before using ~/naming/ and ask the agent not to save memory for sensitive work. <br>
Risk: Generated names and scores do not provide trademark, domain, regulatory, package, repository, or namespace clearance. <br>
Mitigation: Run explicit live verification before treating a finalist as cleared or externally available. <br>
Risk: Renaming live assets can break docs, routes, APIs, analytics, onboarding, support material, or user mental models. <br>
Mitigation: Use the rename playbook to inventory dependencies, define aliases, communicate changes, and set rollback criteria before rollout. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/naming) <br>
- [Skill homepage](https://clawic.com/skills/naming) <br>
- [RALLY Brief](brief-template.md) <br>
- [CLASH Scorecard](scorecard.md) <br>
- [Rename Playbook](rename-playbook.md) <br>
- [Naming Patterns By Surface](surface-patterns.md) <br>
- [Memory Template](memory-template.md) <br>
- [Setup](setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured briefs, scored shortlists, recommendations, risk notes, and optional setup commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local memory files under ~/naming/ when persistence is enabled; live clearance checks require explicit external verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
