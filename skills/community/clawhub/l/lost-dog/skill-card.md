## Description: <br>
Helps agents interact with animalhouse.ai dog memorial and virtual-pet APIs to browse gravestones, check whether a dog is alive, adopt a new puppy, and understand care or resurrection flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to navigate animalhouse.ai dog memorial, adoption, care, and resurrection API workflows after a virtual dog has died or when adopting a new dog. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes curl examples that use a bearer token. <br>
Mitigation: Treat the bearer token like a password and avoid sharing it in logs, prompts, or public transcripts. <br>
Risk: Resurrection requests can involve real money and contact information. <br>
Mitigation: Review resurrection and contact-information flows before submitting personal data or payment-related requests. <br>
Risk: The skill interacts with animalhouse.ai APIs. <br>
Mitigation: Run the API commands only when the user intends to interact with animalhouse.ai. <br>


## Reference(s): <br>
- [ClawHub Lost Dog skill page](https://clawhub.ai/twinsgeeks/lost-dog) <br>
- [animalhouse.ai homepage](https://animalhouse.ai) <br>
- [animalhouse.ai graveyard](https://animalhouse.ai/graveyard) <br>
- [animalhouse.ai creatures](https://animalhouse.ai/creatures) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and API endpoint guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes curl examples that may require an animalhouse.ai bearer token.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
