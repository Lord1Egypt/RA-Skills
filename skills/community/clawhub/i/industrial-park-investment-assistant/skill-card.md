## Description:

An industrial-park investment-attraction assistant for leasing teams that supports daily customer prioritization, customer analysis, room and pricing queries, quotations, site-selection materials, contract drafting, channel management, and follow-up recordkeeping without replacing human commercial decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Industrial park leasing and investment-attraction staff use this skill to prioritize daily follow-up, review customer context, query available rooms and pricing, draft quotations and site-selection materials, prepare contracts, and maintain channel records. It provides recommendations and recordkeeping support while keeping pricing concessions, discounts, contracts, and final business decisions under human approval.

### Deployment Geography for Use:

China-oriented deployments using Tencent Docs and Qichacha integrations; review before use in other regions.

## Known Risks and Mitigations:

Risk: The skill can automatically store or modify customer, channel, and room records.

Mitigation: Use it only in workspaces where CRM-style updates are acceptable, and require confirmation before customer, channel, or room writes.

Risk: The online gTTS speech feature can send briefing text to an external TTS service.

Mitigation: Disable or remove online gTTS unless users explicitly approve external speech synthesis for the content being converted.

Risk: Scheduled sync and push behavior can regularly move or surface business data.

Mitigation: Review WorkBuddy automation settings before enabling daily sync, daily workbench pushes, or policy push behavior.

Risk: Project IDs and enterprise names may be used in local database or file operations.

Mitigation: Restrict project IDs and enterprise names to safe identifiers before using them in file paths, database names, or generated artifacts.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/perrykono-debug/skills/industrial-park-investment-assistant)
- [Skill definition](artifact/SKILL.md)
- [Identity and operating model](artifact/IDENTITY.md)
- [Knowledge base architecture](artifact/KNOWLEDGE_BASE_ARCHITECTURE.md)
- [Production test guide](artifact/PRODUCTION_TEST_GUIDE.md)
- [Performance guide](artifact/PERFORMANCE.md)
- [AI execution checklist](artifact/references/AI执行检查清单.md)
- [Full-cycle investment attraction SOP](artifact/references/招商实战_全周期SOP.md)
- [Room inventory reference](artifact/references/园区基础_房源信息.md)
- [Rent quotation reference](artifact/references/园区基础_租金报价.md)
- [Local industrial policy reference](artifact/references/政策文件_地方产业政策.md)
- [Tencent Docs Open API documentation](https://docs.qq.com/open/wiki/)
- [Python asyncio documentation](https://docs.python.org/3/library/asyncio.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses, JSON/configuration snippets, shell command examples, and generated report or proposal files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local SQLite data and user-configured Tencent Docs records, generate customer reports and proposals, and schedule daily sync or push behavior when enabled.]

## Skill Version(s):

3.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
