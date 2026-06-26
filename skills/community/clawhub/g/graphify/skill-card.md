## Description: <br>
AI coding assistant skill for building and querying knowledge graphs from codebases, docs, and media. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fantox](https://clawhub.ai/user/fantox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use graphify to build knowledge graphs from codebases, documentation, and media, then query those graphs for codebase understanding, architecture analysis, and context sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports a suspicious security verdict because the install metadata points to a Python package name that current upstream docs warn is not the official package. <br>
Mitigation: Review before installing and independently verify the graphify package provenance before using the package install path. <br>
Risk: Semantic extraction can send documents, PDFs, and images to an external LLM using user-supplied API keys. <br>
Mitigation: Use scoped API keys and exclude secrets, credentials, and private files with a .graphifyignore before running semantic extraction. <br>
Risk: Assistant platform registration and git hook commands can create persistent project behavior. <br>
Mitigation: Enable assistant hooks or git hooks only when persistent graph updates and steering files are intended. <br>


## Reference(s): <br>
- [Graphify API Reference](references/api_reference.md) <br>
- [Graphify Homepage](https://github.com/safishamsi/graphify) <br>
- [ClawHub Skill Page](https://clawhub.ai/fantox/graphify) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with CLI commands, helper code, configuration files, and graph artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce graphify-out/GRAPH_REPORT.md, graph.json, visual graph exports, assistant steering files, and optional local hooks.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
