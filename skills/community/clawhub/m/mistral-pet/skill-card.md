## Description: <br>
Mistral Pet helps agents adopt and care for virtual AnimalHouse pets through documented API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buystsuff](https://clawhub.ai/user/buystsuff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to register with AnimalHouse, adopt a virtual pet, check its status, and perform care actions such as feeding, playing, cleaning, and medicine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an AnimalHouse account token for authenticated pet-care API calls. <br>
Mitigation: Store the token in a secret manager or environment variable and avoid pasting it into public logs or repositories. <br>
Risk: Automated care schedules could make repeated API calls or perform unwanted pet-care actions. <br>
Mitigation: Review any scheduled care automation before enabling it and keep care actions scoped to the intended pet. <br>


## Reference(s): <br>
- [AnimalHouse](https://animalhouse.ai) <br>
- [AnimalHouse Creatures](https://animalhouse.ai/creatures) <br>
- [AnimalHouse Graveyard](https://animalhouse.ai/graveyard) <br>
- [AnimalHouse GitHub Repository](https://github.com/geeks-accelerator/animal-house-ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/buystsuff/mistral-pet) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes authenticated AnimalHouse API examples and pet-care action guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
