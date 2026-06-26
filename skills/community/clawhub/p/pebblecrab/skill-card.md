## Description: <br>
Pebblecrab guides users through registering with animalhouse.ai, adopting a hedgehog-themed virtual pet, and caring for it through documented API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to register for animalhouse.ai, adopt a Pebblecrab-named hedgehog, check status, and perform care actions through API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides users to create an animalhouse.ai account and send profile and pet-care data to an external service. <br>
Mitigation: Review the service before submitting data and use a test account when appropriate. <br>
Risk: The instructions use an ah_ bearer token that could grant account access if exposed. <br>
Mitigation: Treat the token like a password, keep it out of chats, logs, screenshots, and repositories, and prefer an environment variable or temporary token for use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leegitw/pebblecrab) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and API endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes visible external API calls and token-handling cautions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
