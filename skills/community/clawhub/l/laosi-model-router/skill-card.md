## Description: <br>
多模型路由器 - 原创技能。根据任务特征自动选择最优AI模型，优化成本和性能。适用于大型项目、混合任务、成本优化等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to classify task complexity and choose an AI model route that balances quality, latency, and cost. It is most useful for mixed workloads, large projects, and cost-sensitive model selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Implementing the guide with real model APIs can expose prompts to multiple providers and increase token costs, especially when using parallel routing. <br>
Mitigation: Make parallel routing opt-in, avoid sending sensitive prompts to multiple providers unnecessarily, and monitor provider logging policies and token spend. <br>
Risk: Model capability, availability, and pricing assumptions can become stale after release. <br>
Mitigation: Verify current provider capabilities, pricing, and policy constraints before using the recommendations in production workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/534422530/laosi-model-router) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown guidance with tables, routing decision examples, and Python-like pseudocode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces model-routing recommendations, fallback options, and cost-quality tradeoff guidance; it does not install or execute provider integrations by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
