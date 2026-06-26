## Description: <br>
Hidden Pet helps an agent guide users through registering, adopting, checking, and caring for a virtual pet on animalhouse.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obviouslynot](https://clawhub.ai/user/obviouslynot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to interact with the animalhouse.ai virtual-pet API, including account registration, pet adoption, status checks, care actions, preferences, history, and graveyard browsing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides users through handling an ah_ bearer token returned by animalhouse.ai. <br>
Mitigation: Treat the token like a password and keep it out of public chats, logs, screenshots, shell history, and repositories. <br>
Risk: Profile, pet, and care-note data may be sent to animalhouse.ai during API use. <br>
Mitigation: Review requests before sending profile details, pet information, or care notes to the service. <br>


## Reference(s): <br>
- [Hidden Pet on ClawHub](https://clawhub.ai/obviouslynot/hidden-pet) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [Creatures](https://animalhouse.ai/creatures) <br>
- [Graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls] <br>
**Output Format:** [Markdown with inline bash code blocks and API endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include bearer-token handling guidance for ah_ tokens returned by animalhouse.ai.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
