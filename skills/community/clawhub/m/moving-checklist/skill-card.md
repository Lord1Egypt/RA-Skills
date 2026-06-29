## Description: <br>
Generate a personalized moving timeline & checklist based on your home info, timeline, and moving distance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and household planners use this skill to turn moving details into a countdown checklist, role assignment plan, budget estimate, and printable moving handbook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Moving profiles can contain personal location and household details. <br>
Mitigation: Use city and district-level addresses only, and use nicknames or pseudonyms for household members when privacy matters. <br>
Risk: Budget output is an estimate and is not a mover quote or financial record. <br>
Mitigation: Confirm costs, insurance, deposit terms, and booking details directly with service providers before relying on the estimate. <br>
Risk: Administrative checklist items may vary by city, landlord, utility provider, or residence status. <br>
Mitigation: Verify local requirements for utilities, address updates, residence permits, and rental handover before acting. <br>


## Reference(s): <br>
- [Task Templates](references/task_templates.json) <br>
- [Budget Tiers](references/budget_tiers.json) <br>
- [Input Schema](schemas/input.schema.json) <br>
- [Output Schema](schemas/output.schema.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/moving-checklist) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown handbook or JSON object with profile, timeline, categorized tasks, role assignment, budget, and handbook fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local CLI output; budget estimates are generic ranges and moving profile data may include personal details.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
