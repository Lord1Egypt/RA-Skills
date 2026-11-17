## Description:

宠物大全查询。查询猫、狗、水族、小宠、爬虫等各类宠物品种信息，包括基本信息、详细介绍、饲养知识等。使用场景：用户说"查一下哈士奇"、"想知道金毛的特点"、"推荐适合新手养的宠物"、"猫咪品种大全"、"狗狗饲养知识"等。通过聚合数据（juhe.cn）API 实时查询，免费注册每天免费调用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search pet breeds and retrieve pet details from Juhe, including basic traits, origin, lifespan, care knowledge, and common disease information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pet search terms and the Juhe API key are sent to Juhe when the skill calls the pet lookup API.

Mitigation: Use the skill only when that data sharing is acceptable for the user and deployment context.

Risk: Passing the API key with --key or storing it in scripts/.env can expose credentials through shell history, process listings, or version control.

Mitigation: Prefer JUHE_PET_QUERY_KEY, avoid command-line keys, keep .env out of version control, and restrict file permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-pet-query)
- [Juhe Pet API documentation](https://www.juhe.cn/docs/api/id/755)
- [Juhe platform](https://www.juhe.cn)
- [Juhe pet search API endpoint](https://apis.juhe.cn/fapigx/pet/search)
- [Juhe pet detail API endpoint](https://apis.juhe.cn/fapigx/pet/detail)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown or plain text with optional shell command examples and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JUHE_PET_QUERY_KEY; sends pet search terms and the Juhe API key to Juhe.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
