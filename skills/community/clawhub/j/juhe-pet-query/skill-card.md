## Description: <br>
查询猫、狗、水族、小宠、爬虫等各类宠物品种信息，包括基本信息、详细介绍和饲养知识，并通过聚合数据 API 实时检索结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search pet breeds by name or category and retrieve pet details such as aliases, origin, traits, care knowledge, common diseases, and fur care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Juhe API key for live pet lookups, and command-line or .env handling can expose credentials through shared logs, shell history, or committed files. <br>
Mitigation: Use a dedicated quota-limited key, prefer environment-variable storage, avoid sensitive personal context in search terms, and do not commit scripts/.env or paste keys into shared logs. <br>


## Reference(s): <br>
- [聚合数据宠物大全 API 文档](https://www.juhe.cn/docs/api/id/755) <br>
- [聚合数据官网](https://www.juhe.cn) <br>
- [ClawHub skill page](https://clawhub.ai/juhemcp/juhe-pet-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and formatted pet lookup results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JUHE_PET_QUERY_KEY API key for live Juhe API lookups.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
