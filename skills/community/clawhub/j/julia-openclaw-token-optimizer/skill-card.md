## Description: <br>
Scans LLM pricing, benchmarks models, and recommends or patches OpenClaw model-selection settings to reduce token spend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronmda](https://clawhub.ai/user/aaronmda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to review current model costs, compare cheaper model options, and update OpenClaw default model routing for cost optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change an agent's default model routing, which may affect future cost, privacy, and reliability behavior. <br>
Mitigation: Review a preview or diff before any config.patch, require rollback instructions, and verify proposed providers and models against current cost, privacy, and reliability requirements. <br>


## Reference(s): <br>
- [LLM Providers Price Sheet](providers.md) <br>
- [OpenAI API Pricing](https://openai.com/api/pricing) <br>
- [xAI Pricing](https://x.ai/pricing) <br>
- [ClawHub skill page](https://clawhub.ai/aaronmda/julia-openclaw-token-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with pricing comparisons, benchmark summaries, and configuration patch examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent model-routing changes for future agent sessions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
