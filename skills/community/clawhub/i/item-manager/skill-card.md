## Description: <br>
Recognizes natural-language item storage statements, records locations and expiry dates, categorizes items, and confirms suspected name corrections before changing them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adderwar-bot](https://clawhub.ai/user/adderwar-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents use this skill to record, query, list, and receive expiry reminders for personal item storage locations through natural-language Chinese prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Chinese trigger phrases can cause normal conversation to be interpreted as item-management input, saving private item or location details. <br>
Mitigation: Use the skill in a dedicated item-management context or with explicit item-management phrasing, and review or delete stored records after use. <br>
Risk: The skill stores item names, storage locations, categories, and expiry dates that may be sensitive. <br>
Mitigation: Install only where that data retention is acceptable and avoid recording sensitive items or locations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adderwar-bot/item-manager) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Natural-language responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include item locations, category lists, and expiry reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
