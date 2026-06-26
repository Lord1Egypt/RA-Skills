## Description: <br>
Virtual pets for Llama agents that helps an agent register with animalhouse.ai, adopt a pet, check status, and send pet-care API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through creating an Animal House account, adopting a virtual pet, checking pet status, and issuing care actions through the disclosed third-party API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Account details, pet names, prompts, and care notes are sent to animalhouse.ai. <br>
Mitigation: Review shared content before use and avoid sending sensitive personal, customer, or confidential information. <br>
Risk: The ah_ bearer token can grant access to the user's Animal House account if exposed. <br>
Mitigation: Store the token securely, keep it out of public chats, logs, and source files, and rotate or revoke it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leegitw/llama-pet) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House Creatures](https://animalhouse.ai/creatures) <br>
- [Animal House Graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with bash curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
