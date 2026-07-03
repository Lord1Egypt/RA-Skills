## Description: <br>
开箱即用的采购订单自动审核 Skill：读取本地订单或飞书邮箱附件，调用 Laiye ADP 识别跨国采购订单，初始化/写入飞书多维表格订单工作台，上传订单源文件，并给审核负责人发送结构化私信，让业务人员只盯未匹配到内部商品、价格异常、新客户、币种异常等异常。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laiye-adp](https://clawhub.ai/user/laiye-adp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations, supply chain, sales operations, and implementation teams use this skill to process purchase order attachments from local files or Feishu mail, extract structured order data with Laiye ADP, write records into Feishu Base, upload source files, and notify reviewers about exceptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process real order documents and Feishu mailbox attachments and upload them to Laiye ADP. <br>
Mitigation: Confirm user consent before sending real customer documents to ADP, and process only intended files or mailbox queries. <br>
Risk: The skill requires Feishu mailbox and workspace authority to read attachments, create or write Base records, upload files, and message reviewers. <br>
Mitigation: Use the least broad mailbox query that satisfies the task, verify Feishu authorization, and keep reviewer notifications limited to the configured reviewer by default. <br>
Risk: Server security guidance notes that referenced runtime scripts and config files are not included in this artifact. <br>
Mitigation: Install and run only the intended scripts from a trusted release source, and avoid similarly named scripts from unrelated workspaces. <br>


## Reference(s): <br>
- [Server-resolved GitHub provenance](https://github.com/Laiye-ADP/adp-skills/tree/main/order-auto-entry-skill-shareable/order-auto-entry) <br>
- [ClawHub skill page](https://clawhub.ai/laiye-adp/skills/order-auto-entry) <br>
- [Laiye ADP public cloud](https://adp.laiye.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent through setup checks, Feishu Base initialization, local or mailbox order processing, and reviewer notification workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
