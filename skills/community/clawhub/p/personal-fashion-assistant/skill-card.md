## Description: <br>
Manages a personal fashion profile and digital wardrobe, then supports wardrobe search, clothing conflict checks, statistics dashboards, and daily outfit recommendations. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[yunaiikim](https://clawhub.ai/user/yunaiikim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to maintain a personal style profile, organize clothing photos and wardrobe records, check potential duplicate or conflicting purchases, analyze wardrobe balance, and receive weather- and scenario-aware outfit suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive body measurements, skin and style attributes, wardrobe records, and clothing photos. <br>
Mitigation: Use only trusted model endpoints, keep local profile and wardrobe files private, and periodically review USER.md and smart_wardrobe contents. <br>
Risk: Some workflows update or delete wardrobe records and related clothing photos. <br>
Mitigation: Keep backups before update or delete operations and confirm the target clothing ID before modifying inventory.md or image files. <br>
Risk: The bundled Python tool files include executable helper and test behavior. <br>
Mitigation: Avoid running tool files directly unless you understand the local file operations they perform. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yunaiikim/personal-fashion-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/yunaiikim) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Conversational guidance, Markdown wardrobe/profile records, clothing-photo file references, and generated HTML dashboard files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local USER.md and inventory.md records and may reference user-supplied clothing or outfit photos.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
