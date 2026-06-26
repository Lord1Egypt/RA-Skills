## Description: <br>
Lobster Buddy adds a deterministic RPG-style virtual pet based on the user's ID, including species, rarity, stats, shiny variants, naming, and occasional pet-style comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users use this skill to view and personalize a lightweight virtual pet, including pet attributes, a custom name, and occasional buddy-style comments during conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store a local buddy state file containing the user ID and pet details. <br>
Mitigation: Install only when local buddy-state storage is acceptable, and review or remove that state according to the user's data-retention preferences. <br>
Risk: The skill may add occasional pet-style comments to agent replies. <br>
Mitigation: Disable or avoid the skill in workflows where extra conversational comments would be distracting or inappropriate. <br>


## Reference(s): <br>
- [Lobster Buddy on ClawHub](https://clawhub.ai/wangxiaofei860208-source/lobster-buddy) <br>
- [Publisher profile](https://clawhub.ai/user/wangxiaofei860208-source) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [Markdown text with optional local JSON-style buddy state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist a local buddy-state file containing the user ID and pet details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
