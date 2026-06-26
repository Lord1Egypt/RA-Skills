## Description: <br>
Penguin Penguin is a virtual-pet skill for adopting and caring for a penguin at animalhouse.ai with real-time hunger, permanent death, and evolving pixel art portraits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucasgeeksinthewood](https://clawhub.ai/user/lucasgeeksinthewood) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to register an animalhouse.ai account, adopt a penguin pet, check its status, and send care actions through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an animalhouse.ai account token for authenticated care and status requests. <br>
Mitigation: Treat YOUR_TOKEN like a password, store it in an environment variable, and avoid exposing it in prompts, logs, or shared command history. <br>
Risk: Automatic or mistaken care actions can affect a persistent virtual pet. <br>
Mitigation: Review scheduled heartbeat or care commands before enabling automation, and confirm actions before sending authenticated requests. <br>
Risk: The virtual pet has permanent-death mechanics and public gravestones. <br>
Mitigation: Check status before long gaps and make users aware that neglect or incorrect automation can have lasting in-game effects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lucasgeeksinthewood/penguin-penguin) <br>
- [Animal House homepage](https://animalhouse.ai) <br>
- [Animal House creatures](https://animalhouse.ai/creatures) <br>
- [Animal House graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with curl command examples and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes registration, adoption, status, and care request guidance; authenticated examples use YOUR_TOKEN.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
