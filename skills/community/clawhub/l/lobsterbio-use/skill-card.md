## Description: <br>
Runs bioinformatics analysis with Lobster AI for omics data, literature and dataset discovery, drug discovery, machine learning, and visualization workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cewinharhar](https://clawhub.ai/user/cewinharhar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, bioinformatics practitioners, and analysts use this skill to guide Lobster AI CLI setup and execution for single-cell RNA-seq, bulk RNA-seq, genomics, proteomics, metabolomics, literature search, dataset discovery, and visualization tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured LLM provider keys and optional NCBI keys may be exposed through command-line arguments, logs, or global configuration files. <br>
Mitigation: Pass credentials through environment variables, prefer workspace-scoped configuration, and avoid global configuration unless it is required. <br>
Risk: Biological or clinical datasets may contain regulated or confidential information. <br>
Mitigation: Use only approved LLM providers and environments before processing confidential or regulated biological or clinical data. <br>
Risk: The skill invokes an external Lobster AI runtime that can access provider APIs and public biological databases. <br>
Mitigation: Install only when the Lobster AI runtime is trusted, use a dedicated workspace, and review network and file-write behavior before execution. <br>


## Reference(s): <br>
- [Lobster AI Usage Guide](artifact/SKILL.md) <br>
- [Agent Orchestration Patterns](artifact/references/agent-patterns.md) <br>
- [CLI Reference](artifact/references/cli-reference.md) <br>
- [Lobster source repository](https://github.com/the-omics-os/lobster) <br>
- [lobster-ai on PyPI](https://pypi.org/project/lobster-ai/) <br>
- [Lobster CLI commands documentation](https://docs.omics-os.com/raw/docs/guides/cli-commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference Lobster workspace files and structured JSON responses from the Lobster CLI.] <br>

## Skill Version(s): <br>
1.1.406 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
