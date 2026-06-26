## Description: <br>
酒店管家 Skill - 管理酒店 OTA 基础信息、房价库存及订单同步。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wolful](https://clawhub.ai/user/wolful) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Hotel operators and implementation teams use this skill to manage OTA hotel information, pricing, inventory, room status, and order synchronization through API or browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change live OTA booking prices. <br>
Mitigation: Use test OTA accounts first, add explicit approval and dry-run previews, and keep audit logs before enabling live price changes. <br>
Risk: Order synchronization can run continuously and push booking data to an internal PMS. <br>
Mitigation: Document a stop procedure, require rollback steps, and verify behavior with test PMS credentials before production use. <br>
Risk: OTA and PMS credentials are required for live operation. <br>
Mitigation: Prefer environment variables or a secret manager and avoid storing real keys in local JSON configuration files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wolful/hotel-manager) <br>
- [Update price example](examples/update_price.md) <br>
- [OTA configuration example](resources/ota_config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript scripts, JSON configuration examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit operational instructions for OTA browser automation and ongoing order synchronization.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
