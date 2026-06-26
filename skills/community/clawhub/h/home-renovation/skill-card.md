## Description: <br>
Plan, budget, and manage home renovation projects including contractor coordination, timeline tracking, and cost estimation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Homeowners and household project managers use this skill to plan renovations, compare quotes, track budgets and timelines, coordinate contractors, document decisions, and manage change orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Renovation tracking can store sensitive budget, contractor contact, home details, and timeline information in local files. <br>
Mitigation: Use detailed tracking only when the user opts in; keep files under ~/home-renovation/ and avoid reusing renovation context when the user chooses on-request or declined tracking. <br>
Risk: Cost estimates and contractor guidance may be inaccurate for a specific location, code regime, or project scope. <br>
Mitigation: Treat ranges as rough planning aids, ask for local scope details, recommend local quotes, written contracts, license and insurance verification, and permit checks before decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/home-renovation) <br>
- [Skill homepage](https://clawic.com/skills/home-renovation) <br>
- [Setup guide](artifact/setup.md) <br>
- [Project types](artifact/projects.md) <br>
- [Contractor evaluation](artifact/contractors.md) <br>
- [Renovation phases](artifact/phases.md) <br>
- [Memory template](artifact/memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with project tracking templates and local file-structure recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local Markdown project files under ~/home-renovation/ when the user opts into tracking.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
