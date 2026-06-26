## Description: <br>
Search Israeli restaurants, check table availability, view menus, and get booking links on Ontopo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexpolonsky](https://clawhub.ai/user/alexpolonsky) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to search Israeli restaurants, compare availability across dates and cities, inspect menus, and generate Ontopo booking links for manual reservation confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes live network requests to an unofficial Ontopo integration, so service behavior, terms, rate limits, or availability data may change outside the skill owner's control. <br>
Mitigation: Treat results as informational, avoid heavy automated use without checking Ontopo terms or rate limits, and verify important details on Ontopo directly. <br>
Risk: The skill generates booking links but does not place reservations, and availability data may be delayed or inaccurate. <br>
Mitigation: Complete and confirm any reservation manually on Ontopo before relying on the booking. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexpolonsky/ontopo) <br>
- [Skill homepage](https://github.com/alexpolonsky/agent-skill-ontopo) <br>
- [Ontopo website](https://ontopo.com) <br>
- [Ontopo API endpoint](https://ontopo.com/api) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs restaurant search results, availability checks, menu details, venue information, and booking URLs; live Ontopo availability should be treated as informational.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
