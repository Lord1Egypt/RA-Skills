## Description: <br>
Searches Chinese A-share financial news and research report summaries by keyword, source, and date range so agents can retrieve current market, company, and industry information from JRJ-backed endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haomanjia](https://clawhub.ai/user/haomanjia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search recent A-share market news, company updates, industry coverage, and brokerage research summaries. It is useful for financial question answering, market review, and information checking, but returned material should be treated as reference information rather than investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JRJ API key and sends it as a request header to JRJ endpoints. <br>
Mitigation: Store JRJ_API_KEY as an environment secret and do not paste real keys into prompts, logs, or client-side code. <br>
Risk: Financial news and research report results may be incomplete, time-sensitive, or unsuitable as direct investment advice. <br>
Mitigation: Treat returned financial information as reference material, verify important claims against authoritative sources, and avoid presenting results as investment recommendations. <br>


## Reference(s): <br>
- [JRJ Claw homepage](https://ai.jrj.com.cn/claw) <br>
- [API reference](references/api-reference.md) <br>
- [ClawHub release page](https://clawhub.ai/haomanjia/jrj-fin-search-skill) <br>
- [Publisher profile](https://clawhub.ai/user/haomanjia) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Markdown, Guidance] <br>
**Output Format:** [JSON or Markdown search results returned by a Node.js command-line tool] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JRJ_API_KEY and supports keyword, start time, optional end time, source, limit, and format arguments.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
