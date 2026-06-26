## Description: <br>
News Cog provides AI news intelligence and daily briefings powered by CellCog for news digests, competitive intelligence, market updates, trend monitoring, industry reports, and current events research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nitishgargiitd](https://clawhub.ai/user/nitishgargiitd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use News Cog to request current news briefings, competitive intelligence, market updates, trend reports, and sourced digests tailored to an audience or timeframe. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a CellCog API key and sends news-research prompts to an external service. <br>
Mitigation: Use a dedicated CellCog API key where possible and avoid including secrets or unnecessary private business context in prompts. <br>
Risk: The skill depends on the external cellcog package. <br>
Mitigation: Verify that the cellcog dependency comes from the expected source before installation or deployment. <br>


## Reference(s): <br>
- [CellCog Homepage](https://cellcog.ai) <br>
- [News Cog on ClawHub](https://clawhub.ai/nitishgargiitd/news-cog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python examples and setup commands; requested news outputs may be structured text, markdown, PDF reports, or interactive HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and CELLCOG_API_KEY; outputs can include source links when requested.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
