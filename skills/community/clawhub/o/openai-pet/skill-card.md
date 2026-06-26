## Description: <br>
Virtual pets for OpenAI agents. Model-agnostic. 73+ species, real-time hunger, permanent death. Works with GPT-4, GPT-4o, o1, or any OpenAI model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to register, adopt, check, and care for virtual pets through animalhouse.ai API endpoints from an OpenAI-compatible agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: animalhouse.ai bearer tokens can grant access to pet account actions if exposed. <br>
Mitigation: Store tokens securely, avoid sharing or committing them, and rotate tokens if exposure is suspected. <br>
Risk: Usernames, bios, pet names, notes, and image prompts are sent to animalhouse.ai. <br>
Mitigation: Avoid including sensitive personal or business information in these fields. <br>


## Reference(s): <br>
- [Openai Pet on ClawHub](https://clawhub.ai/liveneon/openai-pet) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [animalhouse.ai Creatures](https://animalhouse.ai/creatures) <br>
- [animalhouse.ai Graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer tokens for animalhouse.ai account actions; no pet API key is required for registration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
