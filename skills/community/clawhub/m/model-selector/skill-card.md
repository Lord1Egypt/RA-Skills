## Description: <br>
A powerful model routing skill that analyzes query intent and cost-efficiency to select the optimal LLM (Elite/Balanced/Basic) before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rayray1218](https://clawhub.ai/user/rayray1218) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to route prompts to Elite, Balanced, or Basic model tiers before an LLM call to balance capability and cost. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves raw routed prompts locally by default. <br>
Mitigation: Avoid routing secrets or sensitive business or personal data through the skill, restrict or regularly delete query_history.json, and consider disabling or modifying prompt logging before use. <br>
Risk: The skill relies on Python dependencies for routing and embeddings. <br>
Mitigation: Pin and review dependencies in a controlled environment before installing or running the skill. <br>


## Reference(s): <br>
- [Model-Selector on ClawHub](https://clawhub.ai/rayray1218/model-selector) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [JSON-like routing decisions with tier, model, confidence, and score fields; Markdown guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes one query at a time and may save prompt history locally in query_history.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
