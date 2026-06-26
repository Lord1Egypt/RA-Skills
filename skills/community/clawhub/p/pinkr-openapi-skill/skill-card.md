## Description: <br>
品氪提供的OpenApi开放平台，支持门店、导购、会员、订单、退单、库存、商品、积分、储值、卡券、销售等全链路CRM/SCRM数据同步与管理。通过安全认证的API接口实现第三方系统与品氪平台的数据互通。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ikaijian](https://clawhub.ai/user/ikaijian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and authorized business operators use this skill to connect third-party systems with Pinkr CRM/SCRM workflows for stores, members, orders, refunds, inventory, products, points, stored value, coupons, sales, and marketing data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send or change sensitive customer and business data through Pinkr OpenAPI actions. <br>
Mitigation: Use only with an authorized Pinkr account and require explicit human confirmation before refund, shipment, coupon, stored-value, points, inventory, product, order, or member-record changes. <br>
Risk: The bundled default API URL uses HTTP for a development endpoint. <br>
Mitigation: Set PK_API_URL to a trusted HTTPS endpoint before use. <br>
Risk: Generated text and JSON output files may contain sensitive CRM or transaction data. <br>
Mitigation: Treat generated output files as sensitive and delete them when no longer needed. <br>
Risk: A broad APPKEY may allow more Pinkr OpenAPI access than the task requires. <br>
Mitigation: Use the least-privileged APPKEY available for the intended workflow. <br>


## Reference(s): <br>
- [Pinkr OpenAPI default endpoint](http://dev.openapi.pinkr.com) <br>
- [ClawHub skill release page](https://clawhub.ai/ikaijian/pinkr-openapi-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Guidance] <br>
**Output Format:** [Plain text summaries and JSON response files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save API responses under the skill output directory; generated files can contain sensitive CRM, order, member, inventory, or transaction data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
