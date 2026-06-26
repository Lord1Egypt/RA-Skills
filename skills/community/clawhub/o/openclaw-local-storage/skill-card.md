## Description: <br>
Openclaw Local Storage lets an agent store, query, update, and delete structured records in a local JSON file using natural-language commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anbangzhiguo](https://clawhub.ai/user/anbangzhiguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to add lightweight local record storage to an OpenClaw-style agent without connecting to an external database. It is suited to small, non-sensitive datasets that need simple create, read, update, and delete operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package metadata includes an unnecessary filesystem npm dependency flagged as a supply-chain risk. <br>
Mitigation: Remove the unnecessary fs dependency and regenerate dependencies from a trusted environment before installation. <br>
Risk: Update and delete commands can permanently change local JSON data. <br>
Mitigation: Use the skill only for non-sensitive local data and keep backups before allowing write operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anbangzhiguo/openclaw-local-storage) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/anbangzhiguo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [Plain text status messages and JSON-formatted query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores records in a local data.json file; update and delete commands can permanently change stored records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
