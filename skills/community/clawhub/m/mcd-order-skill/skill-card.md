## Description: <br>
通过麦当劳官方 MCP 服务点麦乐送外卖，支持菜单浏览、价格计算、创建订单、订单跟踪、营养信息查询和活动日历查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjn161](https://clawhub.ai/user/wjn161) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to browse McDonald's delivery menus, choose items, calculate prices, create orders, generate payment QR codes, track orders, and query nutrition or campaign information through the McDonald's MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles account-linked ordering through a McDonald's MCP token. <br>
Mitigation: Install only when the publisher is trusted, protect MCD_MCP_TOKEN, and avoid using the skill on shared machines. <br>
Risk: The skill can create real orders and payment QR artifacts. <br>
Mitigation: Confirm delivery address, cart items, and final price before order creation; delete /tmp/mcd_pay_*.png payment QR files after use. <br>
Risk: The skill writes local mcporter and personalized meal configuration. <br>
Mitigation: Review changes to ~/.mcporter/mcporter.json and the skill config before relying on the configured MCP server or default meals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wjn161/mcd-order-skill) <br>
- [Publisher profile](https://clawhub.ai/user/wjn161) <br>
- [McDonald's MCP service endpoint](https://mcp.mcd.cn) <br>
- [McDonald's developer portal](https://open.mcd.cn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, order summaries, and QR-code file paths or ASCII QR output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and MCD_MCP_TOKEN; may read and write local mcporter and skill configuration files and create temporary payment QR images under /tmp.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
