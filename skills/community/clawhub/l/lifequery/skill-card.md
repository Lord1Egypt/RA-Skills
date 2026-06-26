## Description: <br>
Query your Telegram chat history using a LifeQuery instance to search past conversations, find shared links, or ask about specific people and events from Telegram messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ngtwolf](https://clawhub.ai/user/ngtwolf) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent query their Telegram chat history through a configured LifeQuery instance and return relevant answers with citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram history queries and results may contain private message data that could be exposed to or logged by the configured LifeQuery service. <br>
Mitigation: Use a LifeQuery endpoint you control and trust, prefer localhost, and treat all query inputs and outputs as private Telegram data. <br>
Risk: A remote or untrusted LifeQuery endpoint could receive the user's API key and Telegram search queries. <br>
Mitigation: Use HTTPS and authentication for remote servers, and avoid setting LIFEQUERY_API_KEY for any endpoint you do not trust. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ngtwolf/lifequery) <br>
- [LifeQuery project](https://github.com/nikira-studio/lifequery) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Configuration] <br>
**Output Format:** [Plain text or Markdown answers with citations from Telegram history] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LIFEQUERY_BASE_URL and can optionally use LIFEQUERY_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: skill.yaml and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
