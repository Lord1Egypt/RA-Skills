## Description:

Amazon OpenSearch vector search expert knowledge base for vector search configuration, cluster tuning, quantization, cost optimization, instance sizing, pricing estimation, live cluster analysis, and benchmark planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[norrishuang](https://clawhub.ai/user/norrishuang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, tune, size, benchmark, and cost Amazon OpenSearch vector search deployments. It can also guide read-only cluster analysis when users explicitly provide OpenSearch connection details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live cluster analysis may expose real OpenSearch credentials and the security evidence reports unsafe password handling plus TLS certificate verification disabled by default.

Mitigation: Use a dedicated least-privilege read-only OpenSearch account, avoid putting passwords in chat or shell history, require HTTPS with certificate verification, and run analysis only after explicit user approval.

Risk: Benchmark workflows can create, load, force-merge, or delete benchmark indices and may incur cloud, storage, network, or dataset costs.

Mitigation: Run benchmarks only on dedicated non-production targets after explicit confirmation, estimate costs first, and keep backups for any environment that contains important data.

Risk: Generated pricing or benchmark commands can depend on current AWS pricing, installed package versions, and OpenSearch deployment semantics.

Mitigation: Refresh pricing before quoting current totals, pin installer and benchmark dependency versions, inspect dry-run commands, and verify CLI flags against the installed tool version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/norrishuang/skills/opensearch-vector-search)
- [README](README.md)
- [Vector search guide](references/vector-search.md)
- [Cost optimization guide](references/cost-optimization.md)
- [Cluster tuning guide](references/cluster-tuning.md)
- [Quantization techniques guide](references/quantization-techniques.md)
- [1-bit scalar quantization guide](references/quantization-1bit-32x.md)
- [Indexing strategies guide](references/indexing-strategies.md)
- [Query optimization guide](references/query-optimization.md)
- [Performance benchmarks guide](references/performance-benchmarks.md)
- [Optimized instances guide](references/optimized-instances.md)
- [Benchmark scenario matrix](opensearch-vector-benchmark/references/scenario-matrix.md)
- [Benchmark runbook](opensearch-vector-benchmark/references/runbook.md)
- [Benchmark result analysis](opensearch-vector-benchmark/references/result-analysis.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON, configuration, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce read-only analysis recommendations, cost calculations, benchmark plans, and example commands for user review.]

## Skill Version(s):

1.3.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
