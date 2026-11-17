## Description:

智能订单处理助手，帮助用户查询商品并创建单个或批量 WMS 发货单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerod9408](https://clawhub.ai/user/nerod9408)

### License/Terms of Use:

MIT

## Use Case:

External fulfillment users and operators use this skill to look up book inventory, review recipient and order details, and submit WMS shipment orders from a conversation or spreadsheet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit real shipment or order data that includes recipient PII.

Mitigation: Use it only in controlled fulfillment workflows, require human review of recipient data and order details before submission, and treat generated outputs as sensitive records.

Risk: Some scripts allow configurable API destinations and CLI-supplied tokens.

Mitigation: Verify the destination URL before use and avoid passing API keys directly on the command line.

Risk: Batch order creation can submit multiple shipments from spreadsheet input.

Mitigation: Validate spreadsheet rows and batch size before execution, then review success and failure results after the run.

## Reference(s):

- [WMS API 文档](references/wms_api.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Files]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write JSON result files when an output path is provided.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
