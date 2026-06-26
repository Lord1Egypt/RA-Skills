## Description: <br>
The Mossfrog is a common-tier Buddy that maps to the animalhouse.ai Snail and guides care for a virtual pet with hunger, evolution, and permanent death. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to register with animalhouse.ai, adopt a Mossfrog-named Snail, check pet status, and send care actions through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill sends registration details and care notes to an external persistent pet service. <br>
Mitigation: Use non-sensitive registration details and care notes. <br>
Risk: The animalhouse.ai API returns an ah_ bearer token that grants access to the pet account. <br>
Mitigation: Keep the returned token private and avoid pasting it into shared logs, prompts, or public files. <br>


## Reference(s): <br>
- [Animal House](https://animalhouse.ai) <br>
- [Mossfrog on ClawHub](https://clawhub.ai/leegitw/mossfrog) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls] <br>
**Output Format:** [Markdown with bash code blocks and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an external persistent pet service and returns an ah_ bearer token that should be kept private.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
