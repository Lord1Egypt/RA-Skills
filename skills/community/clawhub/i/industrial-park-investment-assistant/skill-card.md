## Description: <br>
Helps industrial park leasing and investment teams manage property inventory, customer follow-up, channel relationships, proposal generation, policy lookup, and daily operating dashboards across local files, Tencent Docs, APIs, and SQLite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perrykono-debug](https://clawhub.ai/user/perrykono-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Industrial park leasing, investment, and operations teams use this agent to organize CRM-like customer, property, channel, pricing, and policy data; generate briefings, proposals, dashboards, and follow-up recommendations; and support day-to-day tenant acquisition workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store and sync customer, contact, property, and channel data. <br>
Mitigation: Review the data flow and automation settings before installation, and configure only approved local storage, Tencent Docs destinations, and credentials. <br>
Risk: Automatic voice, photo, or conversation-driven updates may write business records without enough review. <br>
Mitigation: Disable or avoid automatic updates unless the workflow accepts that risk, and require user confirmation before writing records. <br>
Risk: Generated enterprise, competitor, and policy intelligence may be incomplete or inaccurate. <br>
Mitigation: Verify generated intelligence against authoritative sources before using it in customer communications, investment decisions, or commitments. <br>
Risk: The security summary flags inconsistent local-only safety claims. <br>
Mitigation: Treat local-only statements as unverified and assume data may be synced whenever Tencent Docs integration or automation is enabled. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/perrykono-debug/industrial-park-investment-assistant) <br>
- [Knowledge Base Configuration](artifact/references/知识库配置.md) <br>
- [Property Inventory Reference](artifact/references/园区基础_房源信息.md) <br>
- [Rent Pricing Reference](artifact/references/园区基础_租金报价.md) <br>
- [Amenities Reference](artifact/references/园区基础_配套资源.md) <br>
- [Local Industry Policy Reference](artifact/references/政策文件_地方产业政策.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, structured tables, configuration snippets, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or update local SQLite/cache data and sync CRM-like records to Tencent Docs when configured.] <br>

## Skill Version(s): <br>
2.18.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
