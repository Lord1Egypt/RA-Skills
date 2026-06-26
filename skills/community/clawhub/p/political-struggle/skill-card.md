## Description: <br>
Explains political struggles in Chinese and Western European history, including coups, factional conflict, religious conflict, revolutions, and cross-civilizational comparisons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WD1993](https://clawhub.ai/user/WD1993) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to request concise Chinese-language explanations of historical political struggles, browse Chinese dynasties and Western European periods, or compare structurally similar events across civilizations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional web search sends the user's event or query to Tavily and depends on a Tavily API key. <br>
Mitigation: Use the search mode only for non-sensitive queries and keep Bash execution limited to the packaged search_views.py command. <br>
Risk: Historical summaries may be incomplete or reflect the limits of bundled reference material and retrieved search results. <br>
Mitigation: Review cited search results and the bundled references before relying on outputs for public or high-stakes use. <br>


## Reference(s): <br>
- [Chinese History Political Struggle Reference](reference.md) <br>
- [Western European Political Struggle Reference](western-europe-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/WD1993/political-struggle) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Chinese Markdown with optional search-result summaries and source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional Tavily search mode requires TAVILY_API_KEY and sends the requested event or query to Tavily.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
