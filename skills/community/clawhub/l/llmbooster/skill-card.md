## Description: <br>
LLMBooster is a four-step thinking framework that guides an agent through Plan, Draft, Self-Critique, and Refine stages to improve analysis, writing, code review, and decision-support responses without requiring an external LLM endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danlct27](https://clawhub.ai/user/danlct27) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and agent users use LLMBooster to structure complex analysis, technical documentation, code review, comparisons, and decision-support tasks. The skill helps an agent plan, draft, critique, and refine an answer before returning the final response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad natural-language triggers may activate the structured workflow more often than intended. <br>
Mitigation: Use explicit /booster commands or adjust the enabled state and thinking depth when the workflow is not needed. <br>
Risk: The skill keeps simple local usage statistics in its skill directory. <br>
Mitigation: Review or clear booster_stats.json if local usage tracking is not desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/danlct27/llmbooster) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [Plan Prompt Template](prompts/plan.md) <br>
- [Draft Prompt Template](prompts/draft.md) <br>
- [Self-Critique Prompt Template](prompts/self_critique.md) <br>
- [Refine Prompt Template](prompts/refine.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell command snippets and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Four-step pipeline with configurable thinking depth from 1 to 4; no external LLM endpoint required.] <br>

## Skill Version(s): <br>
1.7.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
