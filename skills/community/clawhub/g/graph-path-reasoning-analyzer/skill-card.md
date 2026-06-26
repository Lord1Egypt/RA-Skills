## Description: <br>
Analyze and discover paths between entities in knowledge graphs to explain relationships, identify indirect connections, and reason over traversal patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to inspect paths, shortest connections, relationship chains, ranking, filtering, and explanations in user-provided knowledge graphs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided graph data can contain sensitive social, business, fraud-investigation, or relationship information. <br>
Mitigation: Treat graph inputs and generated path explanations as sensitive; avoid exposing them outside the intended workspace or review channel. <br>
Risk: All-path enumeration can grow quickly on dense or large graphs. <br>
Mitigation: Use maximum depth, result limits, relationship filters, and shortest-path or K-shortest modes when analyzing large graphs. <br>
Risk: Optional third-party graph libraries may introduce separate dependency or security considerations. <br>
Mitigation: Review and scan any added libraries before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fisa712/graph-path-reasoning-analyzer) <br>
- [Publisher Profile](https://clawhub.ai/user/fisa712) <br>
- [ClawHub Homepage](https://clawhub.com) <br>
- [README](artifact/README.md) <br>
- [Graph Path Patterns](artifact/references/graph-path-patterns.md) <br>
- [Graph Path Examples](artifact/examples/graph-path-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance with optional Python code examples and structured path-analysis outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include path lists, hop counts, relationship sequences, rankings, graph statistics, and natural language explanations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
