## Description: <br>
A virtual pet skill for OpenAI agents that uses animalhouse.ai to adopt and care for model-agnostic digital pets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucasgeeksinthewood](https://clawhub.ai/user/lucasgeeksinthewood) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use the skill to register an animalhouse.ai account, adopt a virtual pet, check status, and perform care actions through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses animalhouse.ai account tokens for authenticated pet actions. <br>
Mitigation: Treat the token like a password and keep it out of prompts, logs, shared transcripts, and source-controlled files. <br>
Risk: Usernames, bios, image prompts, and care notes may be sent to a third-party service. <br>
Mitigation: Avoid submitting personal, confidential, or sensitive information in registration or pet-care fields. <br>


## Reference(s): <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [Creatures](https://animalhouse.ai/creatures) <br>
- [Graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses animalhouse.ai account tokens and pet data as part of the documented care workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
