## Description: <br>
Helps developers extend, test, and contribute to Lobster AI, a multi-agent bioinformatics engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cewinharhar](https://clawhub.ai/user/cewinharhar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and bioinformatics engineers use this skill when working on the Lobster AI codebase, creating agents or services, fixing bugs, adding features, writing tests, or building plugin packages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys and provider credentials may be exposed during setup or command-line use. <br>
Mitigation: Use environment variables or a secret manager, avoid command-line API-key flags, and keep credential files out of version control. <br>
Risk: Persisted Lobster session or workspace files may contain sensitive bioinformatics data or derived analysis state. <br>
Mitigation: Review, protect, or delete persisted session and workspace files when they may contain sensitive data. <br>
Risk: Installing packages or scaffolding plugins can affect the active Python environment. <br>
Mitigation: Use a dedicated Python 3.12 virtual environment and review package contents before installation. <br>


## Reference(s): <br>
- [LobsterBio - Dev release page](https://clawhub.ai/cewinharhar/lobsterbio-dev) <br>
- [AQUADIF Tool Taxonomy Contract](references/aquadif-contract.md) <br>
- [AQUADIF Migration](references/aquadif-migration.md) <br>
- [Architecture](references/architecture.md) <br>
- [BioSkills Bridge](references/bioskills-bridge.md) <br>
- [CLI](references/cli.md) <br>
- [Code Layout](references/code-layout.md) <br>
- [Creating Agents](references/creating-agents.md) <br>
- [Creating Services](references/creating-services.md) <br>
- [Planning Workflow](references/planning-workflow.md) <br>
- [Plugin Architecture](references/plugin-architecture.md) <br>
- [Scaffold](references/scaffold.md) <br>
- [Testing](references/testing.md) <br>
- [Omics-OS Component Registry documentation](https://docs.omics-os.com/docs/core/component-registry) <br>
- [GPTomics bioSkills repository](https://github.com/GPTomics/bioSkills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, shell commands, checklists, and implementation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated or modified Python package code, plugin configuration, validation commands, and test instructions for Lobster AI development workflows.] <br>

## Skill Version(s): <br>
1.1.402 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
