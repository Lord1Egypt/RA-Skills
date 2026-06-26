## Description: <br>
Compare AI inference costs across providers, inventory current usage, query GPU-Bridge pricing, and benchmark alternatives for LLMs, embeddings, image generation, speech, vision, video, document parsing, and reranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fjnunezp75](https://clawhub.ai/user/fjnunezp75) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering teams, and infrastructure reviewers use this skill to audit AI inference spend, compare provider pricing, and decide whether to test or consolidate services through GPU-Bridge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill promotes a third-party inference service and may encourage benchmarking with real prompts or business data. <br>
Mitigation: Use sanitized or synthetic prompts by default, and send customer data, proprietary documents, regulated content, credentials, wallet data, or payment details only after organizational approval of the provider and data flow. <br>
Risk: Cost comparisons and benchmark results can be misleading if pricing, latency, quality, or reliability assumptions do not match the user's workload. <br>
Mitigation: Validate pricing against current provider terms, benchmark representative non-sensitive workloads, and present partial migration or no-migration recommendations when results do not justify a change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fjnunezp75/inference-audit) <br>
- [GPU-Bridge documentation](https://gpubridge.io) <br>
- [GPU-Bridge catalog](https://api.gpubridge.io/catalog) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cost estimates, benchmark steps, provider recommendations, latency and quality observations, and migration guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
