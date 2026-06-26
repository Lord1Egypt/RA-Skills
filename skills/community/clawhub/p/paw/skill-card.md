## Description: <br>
Paw.skill helps pet owners preserve owner-provided memories, habits, sounds, routines, and special moments as local pet profiles for living pets or pets who have passed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realteamprinz](https://clawhub.ai/user/realteamprinz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pet owners use this skill to build and revisit local profiles that capture a pet's personality, communication cues, routines, bonds, and remembered moments. It is intended for remembrance and personal memory preservation, not veterinary or medical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet memories may contain personal or sensitive information and are stored in readable local files. <br>
Mitigation: Use trusted local environments, confirm where ~/.paw-skill/pets/ lives on shared or synced systems, and delete the relevant pet folder when the memories should no longer be retained. <br>
Risk: Users may mistake remembrance responses for veterinary, medical, or health guidance. <br>
Mitigation: Use the skill only for owner-provided memories and personal remembrance; do not use it for veterinary or medical advice. <br>


## Reference(s): <br>
- [Species Guide](references/species-guide.md) <br>
- [Pet Profile Template](templates/PET-PROFILE.md) <br>
- [Paw.skill ClawHub Page](https://clawhub.ai/realteamprinz/paw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Conversational text plus local Markdown and JSONL pet memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates per-pet PROFILE.md, memories.jsonl, and moments.md files under ~/.paw-skill/pets/ when the host agent follows the skill instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
