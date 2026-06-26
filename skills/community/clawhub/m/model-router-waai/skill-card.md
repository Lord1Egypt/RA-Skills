## Description: <br>
Model Router helps an agent compare multiple LLM responses in parallel and merge successful results into a final answer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HuaiBuer](https://clawhub.ai/user/HuaiBuer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to compare outputs from several language models and synthesize a combined answer for tasks where a single model response may be insufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Future real provider integrations could send prompts, private code, or regulated data to external model APIs. <br>
Mitigation: Review provider integrations before deployment and add explicit provider allowlists, user consent, and redaction controls. <br>
Risk: Merged model output may combine inaccurate or low-quality source responses into a misleading final answer. <br>
Mitigation: Use the skill for comparison and synthesis workflows that include human review for important decisions. <br>


## Reference(s): <br>
- [Model Router on ClawHub](https://clawhub.ai/HuaiBuer/model-router-waai) <br>
- [HuaiBuer ClawHub Profile](https://clawhub.ai/user/HuaiBuer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Text or structured Python objects containing a final answer, source model results, merge model, and timing metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included Python router currently simulates provider calls; real provider integrations require review before use with sensitive data.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
