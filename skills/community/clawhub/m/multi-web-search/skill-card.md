## Description: <br>
Provides no-API-key multi-engine web search across international, Chinese, and professional sources with parallel search, time and site filters, and text, image, news, video, and book search modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzairong](https://clawhub.ai/user/wangzairong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent users use this skill to run real-time web searches, gather technical documentation or examples, and compare results across global and Chinese search engines without configuring an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and result fetching may contact external search engines, proxies, or package services. <br>
Mitigation: Use the skill only when external web access is intended, choose engines and proxies deliberately, and review installation behavior before running install.py. <br>
Risk: Sensitive prompts, private URLs, credentials, customer data, or regulated information could be exposed through search queries or local cache entries. <br>
Mitigation: Do not include sensitive data in queries, and use --no-cache for searches that should not be stored locally. <br>
Risk: Returned search results may be outdated, incomplete, duplicated, or misleading across engines. <br>
Mitigation: Review source links and compare results before using them for decisions or downstream agent actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangzairong/multi-web-search) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance and JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search result objects may include title, URL, snippet or media metadata, source engine, ranking score, engine status, cache/DHT flags, and proxy status.] <br>

## Skill Version(s): <br>
3.4.0 (source: frontmatter, metadata.json, CHANGELOG.md, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
