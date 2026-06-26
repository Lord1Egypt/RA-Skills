## Description: <br>
查询指定型号的库存和补货计划，按用户要求调用本地脚本并原样返回结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[logandx314](https://clawhub.ai/user/logandx314) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or support agents use this skill to answer inventory and restock questions for a supplied product model. It runs the packaged query script against a local inventory workbook and returns the script output without reformatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local inventory workbook may expose matching inventory or restock details to whoever asks the agent. <br>
Mitigation: Install and use the skill only in an environment where access to inventory.xlsx and returned stock details is appropriate. <br>
Risk: The query script depends on local files and the openpyxl package. <br>
Mitigation: Confirm inventory.xlsx, inventory_date.txt when used, and openpyxl are present before relying on responses. <br>
Risk: Unsafe command construction could alter how user-supplied model text is passed to the script. <br>
Mitigation: Pass the model text safely as one argument to the fixed script command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/logandx314/inventory-query) <br>
- [Publisher profile](https://clawhub.ai/user/logandx314) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text returned from the local Python query script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill requires an inventory.xlsx workbook and openpyxl; the model query is passed as a script argument.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
