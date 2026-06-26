## Description: <br>
库存监控与补货提醒用于读取指定 Excel 库存台账，计算库存可用月数，并在库存低于阈值时生成企微补货提醒。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perrykono-debug](https://clawhub.ai/user/perrykono-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
园区运营、仓储或采购人员使用该技能监控 Excel 库存台账、识别缺货和低库存物资，并生成补货建议或出入库更新反馈。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and update the named inventory spreadsheet through stock-in and stock-out commands. <br>
Mitigation: Install only for agents allowed to access that ledger, keep backups, and use confirmations or audit logs for inventory-changing actions. <br>
Risk: Shortage details may be sent to configured WeCom recipients. <br>
Mitigation: Use a restricted webhook and limit recipients and message content to the operational stock details needed for replenishment. <br>
Risk: Replenishment recommendations depend on current stock counts and monthly usage values in the spreadsheet. <br>
Mitigation: Keep transaction records and monthly usage values current, and review suggested purchase quantities before procurement. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/perrykono-debug/inventory-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Chinese-language text or Markdown inventory reports, replenishment alerts, transaction confirmations, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference configured Excel worksheet paths, inventory thresholds, WeCom recipients, scheduled checks, and stock transaction inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
