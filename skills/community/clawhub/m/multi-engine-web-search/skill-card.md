## Description:

Search Google, Bing, DuckDuckGo, Brave, Startpage, Yahoo, Yandex, Baidu, Sogou, Qwant, Ecosia, Mojeek, and WolframAlpha from one skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, researchers, and other external users use this skill to run broader web lookups across multiple search engines, compare results, and verify current or high-impact claims with contradiction queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries can be sent to several third-party search, knowledge, and developer engines per lookup.

Mitigation: Use explicit or on-request activation for sensitive topics and avoid including secrets, private personal data, or confidential material in search terms.

Risk: The skill stores cross-session activation and engine preferences, which can cause future searches to run more often than intended.

Mitigation: Review the saved memory profile periodically, keep blocked engines current, and remove or revise the memory if activation behavior is too broad.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/multi-engine-web-search)
- [Skill homepage](https://clawic.com/skills/multi-engine-web-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance]

**Output Format:** [Markdown search summaries with links, confidence notes, and optional web_fetch call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist activation mode, preferred engine order, blocked engines, and output style in a local memory file.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
