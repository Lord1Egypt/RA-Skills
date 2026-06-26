## Description: <br>
Track orders locally. Use when creating orders, checking status, updating quantities, canceling, or generating sales reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create, list, inspect, update, cancel, and summarize local order records for lightweight order tracking workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Order records are stored locally as business data in ~/.orders/orders.json. <br>
Mitigation: Apply appropriate local file permissions, backups, and data handling practices for order records. <br>
Risk: Order notes can contain sensitive business or customer information. <br>
Mitigation: Avoid placing secrets or unnecessary sensitive details in order notes. <br>
Risk: Update and cancel commands can modify the wrong order if an incorrect ID is used. <br>
Mitigation: Confirm the order ID and intended action before running update or cancel commands. <br>


## Reference(s): <br>
- [ClawHub Orders Skill Page](https://clawhub.ai/xueyetianya/orders) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, CSV, Files, Shell commands] <br>
**Output Format:** [Plain text, JSON, or CSV stdout with persistent JSON records in ~/.orders/orders.json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local order records; order IDs are generated automatically.] <br>

## Skill Version(s): <br>
3.4.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
