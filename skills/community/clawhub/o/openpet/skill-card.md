## Description: <br>
OpenPet is a Tamagotchi-style virtual pet skill for chat platforms where each user can create, care for, and evolve a pet through chat commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mdealiaga](https://clawhub.ai/user/mdealiaga) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External chat users and community operators use OpenPet to add a lightweight virtual pet game to OpenClaw channels, with per-user pets that respond to care commands and evolve over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores per-user pet records locally, including platform and user identifiers. <br>
Mitigation: Operators should document where pet records are stored, how users can delete their records, and how retention is handled. <br>
Risk: The scheduled decay and reminder behavior can send proactive alerts to users. <br>
Mitigation: Operators should disclose reminder behavior before deployment and provide an opt-out path for proactive pet alerts. <br>


## Reference(s): <br>
- [OpenPet release page](https://clawhub.ai/mdealiaga/openpet) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Configuration reference](references/config.json) <br>
- [Sprites reference](references/sprites.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown and chat-response text with JSON configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces chat command responses, pet status displays, setup guidance for local pet records, and scheduled decay behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
