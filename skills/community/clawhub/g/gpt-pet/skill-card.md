## Description: <br>
Virtual pets for GPT agents that work with any model, supporting 73+ species, real-time hunger, permanent death, pixel art portraits, and care actions through animalhouse.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to register for animalhouse.ai, adopt a virtual pet, check its status, and send care actions through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends pet names, prompts, and care notes to animalhouse.ai. <br>
Mitigation: Use only non-sensitive pet names, prompts, and notes when interacting with the service. <br>
Risk: The animalhouse.ai token grants account access. <br>
Mitigation: Treat the returned token like a password and avoid exposing it in shared logs, prompts, or repositories. <br>
Risk: The virtual pet is time-based and may be permanently lost if neglected. <br>
Mitigation: Check status and perform care actions on an appropriate schedule before using the skill for a persistent pet. <br>


## Reference(s): <br>
- [Gpt Pet on ClawHub](https://clawhub.ai/liveneon/gpt-pet) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls] <br>
**Output Format:** [Markdown with inline bash code blocks and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token API requests; users should treat the returned token like a password.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
