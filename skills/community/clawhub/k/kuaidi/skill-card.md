## Description: <br>
查询中国常见快递公司的官方客服电话、常用联系渠道、投诉与催件路径，并给出延误、长时间不更新、显示签收但未收到、驿站代收、破损、丢件、拒收退回、疑似诈骗短信或电话等常见快递问题的处理建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvy](https://clawhub.ai/user/jvy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and support agents use this skill to answer Chinese courier-service questions, find official carrier contact channels, triage delivery exceptions, and produce concise next-step checklists for complaints, missing packages, damage, returns, and suspected scams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Carrier phone numbers, service hours, complaint portals, and compensation rules may change after release. <br>
Mitigation: Verify important or time-sensitive details through the carrier's official app, website, or hotline before acting. <br>
Risk: Delivery-dispute guidance could be mistaken for a legal or guaranteed compensation conclusion. <br>
Mitigation: Use the skill for practical triage and evidence preparation, and rely on current carrier, platform, regulator, or legal guidance for binding decisions. <br>
Risk: Suspicious courier messages or calls may contain phishing links or social-engineering requests. <br>
Mitigation: Use only official carrier channels for verification, avoid sharing verification codes or screen access, and escalate financial loss or credential exposure to the bank, platform, and authorities. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jvy/kuaidi) <br>
- [快递公司官方热线参考](references/carriers.md) <br>
- [快递异常件处理参考](references/issues.md) <br>
- [顺丰速运](https://www.sf-express.com/cn/sc/) <br>
- [京东物流帮助中心](https://help.jd.com/user/issue/270-314.html) <br>
- [中国邮政 EMS](https://www.ems.com.cn/) <br>
- [中通快递](https://www.zto.com/) <br>
- [圆通速递](https://www.yto.net.cn/) <br>
- [申通快递](https://www.sto.cn/) <br>
- [韵达速递](https://www.yundaex.com/) <br>
- [德邦快递](https://www.deppon.com/) <br>
- [极兔速递](https://www.jtexpress.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown answers with concise action checklists and optional inline Node.js helper commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses static local carrier and issue references; does not provide real-time tracking, live pricing, or definitive legal conclusions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
