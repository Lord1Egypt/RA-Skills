## Description:

按关键词检索周公解梦释义，支持分页。当用户说：梦见蛇是什么意思？梦到飞代表什么？或类似解梦问题时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up Duke of Zhou dream interpretations by keyword and summarize the most relevant results in conversation. It is intended for entertainment and learning reference, not medical, financial, or real-world decision guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the API key and user-provided dream keyword to JisuAPI.

Mitigation: Use a dedicated JisuAPI key, keep it in the JISU_API_KEY environment variable, and avoid sharing the key in chat or logs.

Risk: Dream descriptions can contain personal or sensitive details.

Mitigation: Submit short, necessary keywords instead of detailed personal dream narratives when possible.

Risk: Dream interpretations may be mistaken for decision, health, or predictive guidance.

Mitigation: Present results as entertainment and learning reference only, and avoid using them for medical or real-world decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/jisu-dream)
- [JisuAPI website](https://www.jisuapi.com/)
- [JisuAPI dream API documentation](https://www.jisuapi.com/api/dream)
- [JisuAPI dream search endpoint](https://api.jisuapi.com/dream/search)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON results and concise natural-language dream interpretation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; keyword is required, with optional pagenum and pagesize.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
