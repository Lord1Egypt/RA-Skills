## Description:

Extract semantic relationships from long narratives, architectures, or complex discussions using RDF-style triple notation and generate adjacency matrices to reveal narrative structure, dependency graphs, and critical paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turinfohlen](https://clawhub.ai/user/turinfohlen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and writers use this skill to mark semantic relationships in markdown with RDF-style triples, run a local scanner, and inspect compressed adjacency matrices for dependencies, causal chains, bottlenecks, and cycles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the scanner from a broad directory can recursively read supported text-like files and print extracted node names and graph data.

Mitigation: Run it from a small, intentional working folder and review output before sharing it.

Risk: Very large or untrusted documents may produce noisy, oversized, or unreliable graph output.

Mitigation: Use curated input documents and inspect triples before relying on graph statistics.

Risk: Predicates are not preserved in the generated adjacency matrix, which can hide the type of relationship between nodes.

Mitigation: Keep the source triples available for interpretation or extend the scanner when predicate-level analysis is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/turinfohlen/skills/narrative-topology)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Text]

**Output Format:** [Markdown guidance with Python code and shell commands; scanner output is plain text with compressed adjacency matrices and summary statistics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The adjacency matrix omits predicate labels and reports source-to-target edges over supported local text-like files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
