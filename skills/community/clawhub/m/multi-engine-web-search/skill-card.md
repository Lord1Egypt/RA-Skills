## Description: <br>
Search Google, Bing, DuckDuckGo, Brave, Startpage, Yahoo, Yandex, Baidu, Sogou, Qwant, Ecosia, Mojeek, and WolframAlpha from one skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and other agents use this skill to broaden web lookup coverage, cross-check claims across multiple search engines, and prioritize primary sources for current or high-impact topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may be sent to multiple public search and knowledge providers. <br>
Mitigation: Avoid including secrets, internal URLs, private identifiers, or sensitive personal information in search queries. <br>
Risk: The skill can save activation mode, engine priority, blocked engines, and output-style preferences. <br>
Mitigation: Use explicit-only activation when automatic web lookups are not desired, and review or delete ~/multi-engine-web-search/memory.md if preferences change. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/multi-engine-web-search) <br>
- [Skill Homepage](https://clawic.com/skills/multi-engine-web-search) <br>
- [Setup Guide](setup.md) <br>
- [Memory Template](memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Concise Markdown with links, confidence notes, and preference guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save minimal user preferences in ~/multi-engine-web-search/memory.md when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
