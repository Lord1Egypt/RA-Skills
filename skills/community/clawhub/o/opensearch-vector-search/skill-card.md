## Description: <br>
Amazon OpenSearch vector search knowledge base for k-NN configuration, cluster tuning, quantization, cost optimization, instance sizing, pricing estimation, and read-only cluster analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[norrishuang](https://clawhub.ai/user/norrishuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, search engineers, and platform teams use this skill to plan and tune Amazon OpenSearch vector search deployments, estimate capacity and cost, compare quantization options, and review existing k-NN cluster configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle live OpenSearch cluster URLs and credentials, and its examples show command-line password usage with SSL verification disabled by default. <br>
Mitigation: Review helper scripts before use, use least-privilege read-only accounts, avoid placing production passwords directly on command lines, and enable SSL verification or provide a trusted CA path. <br>
Risk: Reference material includes configuration examples that may use state-changing OpenSearch API methods if copied and executed. <br>
Mitigation: Treat PUT, POST, and DELETE snippets as reviewable examples only, and apply any cluster changes manually through an approved change process. <br>
Risk: The pricing workflow depends on AWS credentials and makes outbound requests to the AWS Pricing API. <br>
Mitigation: Run pricing lookups only when cost estimation is needed, use least-privilege AWS credentials or an appropriate IAM role, and do not share credential values in prompts or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/norrishuang/opensearch-vector-search) <br>
- [Vector search guide](references/vector-search.md) <br>
- [Quantization techniques](references/quantization-techniques.md) <br>
- [Cost optimization](references/cost-optimization.md) <br>
- [Cluster tuning](references/cluster-tuning.md) <br>
- [Performance benchmarks](references/performance-benchmarks.md) <br>
- [Indexing strategies](references/indexing-strategies.md) <br>
- [Query optimization](references/query-optimization.md) <br>
- [Optimized instances](references/optimized-instances.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON snippets, formulas, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include read-only JSON cluster analysis when the helper script is run with user-supplied connection details.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
