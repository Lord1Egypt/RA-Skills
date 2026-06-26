## Description: <br>
Turns a vague reporting clue, observation, or topic hunch into a deeper news pitch by extracting entities, retrieving 1-2 hop context from a city knowledge graph, and generating an editor-style planning memo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangzuomin2019](https://clawhub.ai/user/huangzuomin2019) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Journalists, editors, and reporting teams use this skill to turn rough local-news clues into graph-grounded pitch planning memos with issue clusters, angles, contradictions, and interview targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reporting clues, source names, allegations, or local graph context may be sent to an external LLM when API keys are present. <br>
Mitigation: Review inputs before running, avoid sensitive reporting material with external API keys enabled, or unset OPENAI_API_KEY and GLM_API_KEY to use offline fallback behavior. <br>
Risk: The skill depends on a referenced local city-knowledge-graph project and database. <br>
Mitigation: Verify the local graph project and data source before running the script, and treat weak graph coverage as a reporting gap. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/huangzuomin2019/pitch-amplifier) <br>
- [OpenAI-compatible GLM API endpoint](https://open.bigmodel.cn/api/coding/paas/v4) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Shell commands, Guidance] <br>
**Output Format:** [Markdown pitch memo with extracted entities and graph context] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run with an external LLM when OPENAI_API_KEY or GLM_API_KEY is set; otherwise uses offline fallback behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
