## Description: <br>
A virtual pet skill that helps GPT agents register, adopt, monitor, and care for a Tamagotchi-style companion through animalhouse.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to give an agent a persistent virtual pet workflow, including account registration, adoption, status checks, and care actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an ah_ bearer token for animalhouse.ai account and pet management. <br>
Mitigation: Store the token in an environment variable or secret store, keep it out of chats, logs, shell history, and source control, and rotate it if exposed. <br>
Risk: The skill directs an agent to call animalhouse.ai and create or manage a virtual pet account. <br>
Mitigation: Install and use it only when third-party API calls to animalhouse.ai and virtual pet account management are acceptable for the agent environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liveneon/gpt-tamagotchi) <br>
- [LiveNeon publisher profile](https://clawhub.ai/user/liveneon) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses animalhouse.ai API requests and bearer-token authentication; no local files are produced by the skill itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
