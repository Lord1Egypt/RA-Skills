## Description: <br>
Comprehensive memory management optimization for AI agents, including structured summaries, project tracking, daily maintenance, knowledge graph support, retrieval, consolidation, decay, and dashboard tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richardiitse](https://clawhub.ai/user/richardiitse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to build or improve long-running agent memory systems, recover context after compression, maintain structured project memory, and query or consolidate knowledge graph records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect prior agent sessions and persistent memory, which may include sensitive content. <br>
Mitigation: Review memory paths first, prefer dry-run or read-only modes where available, and avoid processing sessions containing secrets unless redaction and consent controls are in place. <br>
Risk: Some workflows may send selected memory or transcript content to configured model APIs. <br>
Mitigation: Use restricted API keys, confirm configured endpoints, and review or disable extraction and consolidation before using the skill on confidential data. <br>
Risk: Memory tools can persist, mutate, or infer durable preferences in local knowledge graph or cache files. <br>
Mitigation: Limit knowledge graph and cache paths, review generated records before relying on them, and periodically prune or delete stale or unwanted memory entries. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/richardiitse/memory-optimization) <br>
- [Skill definition](SKILL.md) <br>
- [README](README.md) <br>
- [Scripts README](scripts/README.md) <br>
- [Memory ontology integration](ontology/INTEGRATION.md) <br>
- [Memory ontology quick reference](ontology/QUICK_REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or maintenance of persistent memory files, knowledge graph data, local scripts, and configuration.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
