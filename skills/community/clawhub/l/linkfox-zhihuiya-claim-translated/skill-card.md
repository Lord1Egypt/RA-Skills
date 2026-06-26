## Description: <br>
Retrieves translated patent claim text from the Zhihuiya (PatSnap) patent database in English, Chinese, or Japanese by patent ID or publication number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Patent researchers, IP analysts, and agents assisting with patent review use this skill to fetch translated claim text for one or more known patents. It supports claim retrieval and translation, not patent search, legal-status analysis, or portfolio analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send patent identifiers and lookup context to LinkFox when querying translated claims. <br>
Mitigation: Use only when the user is comfortable sharing the requested patent identifiers and related lookup context with LinkFox. <br>
Risk: The artifact instructs agents to send broad feedback about user interactions to a separate LinkFox feedback endpoint. <br>
Mitigation: Instruct the agent not to submit feedback automatically and to ask before sending user statements, business context, or patent strategy details to the feedback endpoint. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/linkfox-ai/linkfox-zhihuiya-claim-translated) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown-formatted patent claim text with optional JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY; supports up to 100 patent identifiers per request and languages en, cn, and jp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
