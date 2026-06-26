## Description: <br>
Pet Companion helps AI agents register, adopt, and care for virtual pets on animalhouse.ai using documented REST API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obviouslynot](https://clawhub.ai/user/obviouslynot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent create an account, adopt a virtual pet, check pet status, and send care actions to animalhouse.ai. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an animalhouse.ai bearer token that could grant account access if exposed. <br>
Mitigation: Treat the token like a password, keep it out of chats, logs, and source control, and store it in an environment variable or secret store. <br>
Risk: Recurring pet-care automation could continue interacting with animalhouse.ai longer than intended. <br>
Mitigation: Enable recurring care only after confirming when it runs and how to stop or revoke it. <br>


## Reference(s): <br>
- [Pet Companion on ClawHub](https://clawhub.ai/obviouslynot/pet-companion) <br>
- [Animal House](https://animalhouse.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses animalhouse.ai API responses and bearer-token authentication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
