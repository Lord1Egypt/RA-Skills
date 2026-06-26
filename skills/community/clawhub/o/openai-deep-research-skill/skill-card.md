## Description: <br>
Executes multi-step deep research with the OpenAI Responses API, including question decomposition, web evidence gathering, contradiction tracking, and final cited report synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guanglechen](https://clawhub.ai/user/guanglechen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research-focused agents use this skill to run structured investigations on complex or high-stakes topics and produce auditable research plans, evidence summaries, and cited reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends research topics and prompts to the configured OpenAI-compatible provider. <br>
Mitigation: Use a scoped OpenAI API key, avoid untrusted custom OPENAI_BASE_URL gateways, and submit confidential topics only when they may be sent to that provider. <br>
Risk: Saved raw outputs may contain the full research prompts, evidence, and model responses. <br>
Mitigation: Review and protect the output directory according to local data-handling requirements before sharing, retaining, or deleting run artifacts. <br>
Risk: Generated research reports can include incomplete evidence, weak sources, or unresolved contradictions. <br>
Mitigation: Apply the included research-quality rubric, verify cited source links, and rerun with adjusted depth, model, or source constraints when gaps remain. <br>


## Reference(s): <br>
- [Research Quality Rubric](references/research-quality.md) <br>
- [ClawHub skill page](https://clawhub.ai/guanglechen/openai-deep-research-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Text, Shell commands, Guidance] <br>
**Output Format:** [Run artifacts including JSON plans and findings, raw text or JSON model outputs, and a final Markdown report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes one timestamped output directory per run; depth, model selection, web search, concurrency, and token ceilings are configurable.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
