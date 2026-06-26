## Description: <br>
车辆信息查询技能，支持查询车辆位置、车况信息（车锁、车门、车窗、空调、引擎状态等）。当用户查询车辆位置、询问车辆在哪里、查询车况信息时自动调用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouzidan](https://clawhub.ai/user/zhouzidan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with valid Nokey vehicle credentials use this skill to retrieve vehicle location and vehicle status details, including lock, door, window, air conditioner, engine, SN, VIN, gear, and power state fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles vehicle access tokens and caches them locally in ~/.nokey_vehicle_info_cache.json. <br>
Mitigation: Do not paste real tokens into shared chats, screenshots, or logs; avoid commands that print the cache; restrict or remove the cache file when not needed; and rotate any exposed token. <br>
Risk: The skill can return sensitive vehicle location, vehicle identifiers, and vehicle status data. <br>
Mitigation: Install only if the publisher and listed vehicle API endpoints are trusted, and share returned vehicle data only with authorized users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouzidan/nokey-vehicle-info) <br>
- [Production vehicle condition endpoint](https://openapi.nokeeu.com/iot/v1/condition) <br>
- [UAT vehicle condition endpoint](https://uat-openapi.ingeek.com/iot/v1/condition) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell command examples and JSON-derived vehicle status fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive vehicle location, vehicle identifiers, and token-handling guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
