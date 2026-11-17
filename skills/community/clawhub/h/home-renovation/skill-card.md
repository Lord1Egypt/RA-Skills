## Description:

Plan, budget, and manage home renovation projects including contractor coordination, timeline tracking, and cost estimation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Homeowners and renovation planners use this skill to organize remodel budgets, timelines, contractor evaluation, scope changes, and project decisions. The agent can provide planning guidance and maintain local markdown records for ongoing renovation projects when the user wants tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store renovation budgets, project notes, timelines, and contractor contact details locally.

Mitigation: Use the on-request or declined integration preference if persistent tracking is not wanted, and avoid adding sensitive contractor or financial details that do not need to be retained.

Risk: Renovation costs, permits, contractor requirements, and code obligations vary by location and project scope.

Mitigation: Treat cost ranges and sequencing advice as planning guidance, verify local requirements, and obtain written local quotes before committing funds or work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/home-renovation)
- [Skill homepage](https://clawic.com/skills/home-renovation)
- [Setup guide](setup.md)
- [Memory template](memory-template.md)
- [Project types](projects.md)
- [Contractor evaluation](contractors.md)
- [Renovation phases](phases.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance and local markdown project records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update renovation memory under ~/home-renovation/ when the user opts into tracking.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
