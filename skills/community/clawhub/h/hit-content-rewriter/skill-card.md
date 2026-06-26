## Description: <br>
Helps agents extract, analyze, store, query, and rewrite high-performing short-video and article content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pyzxs](https://clawhub.ai/user/pyzxs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and agents use this skill to extract copy from short-video links, analyze high-performing content patterns, store examples for retrieval, and draft adapted rewrites for target platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored or embedded content may include personal, confidential, or third-party material. <br>
Mitigation: Avoid personal or confidential text, verify rights to process source content, and understand how to manage or delete ChromaDB data before relying on it. <br>
Risk: The workflow depends on an external vector-store tool and embedding provider credentials. <br>
Mitigation: Install jl-vector-store only from a trusted source, use scoped API keys, and configure the embedding provider intentionally. <br>
Risk: Generated rewrites may be too similar to source material or conflict with platform rules. <br>
Mitigation: Review outputs for originality, rights, prohibited content, and target-platform policy compliance before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pyzxs/hit-content-rewriter) <br>
- [Content analyzer design](references/content-analyzer.md) <br>
- [Design philosophy](references/design-philosophy.md) <br>
- [Rewrite quick reference](references/rewrite-quick-reference.md) <br>
- [Rewrite strategies](references/rewrite_strategies.md) <br>
- [Analysis report template](templates/analysis-report.md) <br>
- [Rewrite result template](templates/rewrite-result.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, rewritten draft text, storage/query confirmations, and shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require jl-vector-store, optional downloader or rewriter skills, and embedding API configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
