## Description: <br>
Mushroom Mushroom guides an agent through adopting and caring for a real-time virtual mushroom pet at animalhouse.ai, including hunger, health, life-stage evolution, and public graveyard endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buystsuff](https://clawhub.ai/user/buystsuff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an assistant interact with AnimalHouse on their behalf: register an account, adopt a Mushroom pet, check status and history, and send care actions through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AnimalHouse account tokens authorize pet-care API calls and are shown once during registration. <br>
Mitigation: Treat the AnimalHouse token as a secret, use placeholders or environment variables where possible, and avoid committing it in prompts, logs, or skill files. <br>
Risk: Automated or recurring care can perform AnimalHouse API calls on the user's behalf. <br>
Mitigation: Enable recurring care only when the user is comfortable with automated pet-care actions and their effect on the virtual pet. <br>


## Reference(s): <br>
- [Mushroom Mushroom on ClawHub](https://clawhub.ai/buystsuff/mushroom-mushroom) <br>
- [AnimalHouse homepage](https://animalhouse.ai) <br>
- [AnimalHouse creatures](https://animalhouse.ai/creatures) <br>
- [AnimalHouse graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash curl commands and endpoint/action tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses placeholder Bearer tokens and AnimalHouse endpoint paths; does not produce local files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
