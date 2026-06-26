## Description: <br>
Routes shopping-related queries to Viking AISearch chat or search APIs and helps return product search answers, candidate lists, or Markdown product cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenyantong429-coder](https://clawhub.ai/user/chenyantong429-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to handle shopping search, product recall, search question answering, and product-card generation through an external AISearch provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping queries, image URLs, user metadata, nicknames, or location context may be sent to an external AISearch provider. <br>
Mitigation: Use a scoped provider API key and avoid sending sensitive images or precise location unless needed. <br>
Risk: The skill depends on an external AISearch service for chat and search behavior. <br>
Mitigation: Handle provider errors, timeouts, and empty results by clearly telling the user the search service is unavailable or asking whether to retry. <br>


## Reference(s): <br>
- [ChatSearch API Reference](references/chat_search_api.md) <br>
- [Search API Reference](references/search_api.md) <br>
- [Volcengine ChatSearch Documentation](https://www.volcengine.com/docs/85296/1873492?lang=zh) <br>
- [Volcengine Search Documentation](https://www.volcengine.com/docs/85296/1544974?lang=zh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown product summaries, JSON API results, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses returned provider fields only; missing product fields are omitted rather than filled with placeholders.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
