## Description: <br>
妈妈网育儿知识爬虫（PC端）按分类或关键词爬取 www.mama.cn 育儿文章，并将标题、来源、日期、链接和正文保存为本地 Markdown 文件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zton100](https://clawhub.ai/user/zton100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to collect public mama.cn parenting articles by category or keyword and save them as local Markdown files for a personal knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The crawler disables TLS certificate verification when fetching mama.cn content. <br>
Mitigation: Run it only on trusted networks and review saved Markdown before relying on it. <br>
Risk: Fetched parenting articles are public web content and may include unverified medical or parenting advice. <br>
Mitigation: Treat saved Markdown as untrusted source material and verify important claims against authoritative sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zton100/mama-crawler) <br>
- [mama.cn parenting site](https://www.mama.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown files and command-line progress text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves fetched articles under ~/.yuzhi/crawls/mama_cn/ with title, source, date, URL, and body content.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
