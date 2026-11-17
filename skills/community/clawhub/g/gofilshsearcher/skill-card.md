## Description:

闲鱼商品自动搜索技能，支持严格筛选（个人闲置/单一价格/排除商家），输出 TOP10 价格升序列表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxxzhuo](https://clawhub.ai/user/xxxzhuo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search Xianyu/Goofish listings, filter for personal second-hand items, remove merchant or ambiguous-price listings, and return ranked product results with price statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically records search history, including marketplace searches, price interests, and listing links, to local memory without clear opt-in, retention, or deletion controls.

Mitigation: Disable or remove automatic history writing before deployment, or add explicit opt-in, retention, and deletion controls.

Risk: Broad activation phrases may trigger marketplace searches from casual Xianyu-related questions.

Mitigation: Confirm user intent before launching browser searches when the request is ambiguous.

Risk: The skill depends on browser automation against a marketplace website whose page structure and access controls may change.

Mitigation: Handle selector failures and network timeouts by surfacing partial or failed results clearly and requiring user review before purchase decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xxxzhuo/skills/gofilshsearcher)
- [Publisher Profile](https://clawhub.ai/user/xxxzhuo)
- [Goofish Marketplace](https://www.goofish.com)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown tables and short status messages with listing links, price statistics, troubleshooting guidance, and optional configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are normally capped at TOP10, sorted by ascending price, and may be split into one listing per message for enterprise chat workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
