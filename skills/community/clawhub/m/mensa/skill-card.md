## Description: <br>
Returns today's lunch menu of a German university canteen via the public OpenMensa API with no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rifatdevelopment](https://clawhub.ai/user/rifatdevelopment) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw agents use this skill to look up current or dated German university canteen menus, including student prices and vegan or vegetarian tags, after a one-time city and canteen setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: City, selected canteen, and menu date lookups are sent to OpenMensa. <br>
Mitigation: Use the skill only when this lookup disclosure is acceptable, and keep the user-facing response clear that menu data comes from OpenMensa. <br>
Risk: The release is tagged as requiring sensitive credentials even though the evidence says no credentials or API key are used. <br>
Mitigation: Do not provide credentials to this skill; publisher should remove the unsupported sensitive-credentials tag for clarity. <br>


## Reference(s): <br>
- [OpenMensa](https://openmensa.org) <br>
- [OpenMensa canteens API](https://openmensa.org/api/v2/canteens?page=N) <br>
- [OpenMensa meals API](https://openmensa.org/api/v2/canteens/{id}/days/{date}/meals) <br>
- [Mensa on ClawHub](https://clawhub.ai/rifatdevelopment/mensa) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text menu output rendered by the agent as Markdown bullet lists, with setup and debugging shell commands when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a local config.json during setup and queries OpenMensa over outbound HTTPS.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter and script report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
