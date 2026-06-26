## Description: <br>
Memic helps agents integrate a managed context engineering platform for document ingestion, semantic and structured search, RAG, Text2SQL, hybrid search, metadata filtering, and grounded prompt context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[punithg](https://clawhub.ai/user/punithg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to configure Memic, upload documents, search document and database content, and inject retrieved context into LLM prompts for grounded RAG or Text2SQL workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install and use the Memic Python package. <br>
Mitigation: Verify the package source and pin package versions before production use. <br>
Risk: The skill relies on MEMIC_API_KEY and may access managed context data. <br>
Mitigation: Use scoped API keys, store them outside prompts and source files, and rotate them when access changes. <br>
Risk: Document uploads or database connectors could expose secrets, regulated data, or overbroad database access. <br>
Mitigation: Avoid uploading sensitive data without approval, and use read-only least-privilege database credentials or non-production replicas for connectors. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/punithg/memic) <br>
- [Memic Dashboard](https://app.memic.ai) <br>
- [Memic Python Package](https://pypi.org/project/memic/) <br>
- [Memic Python SDK](https://github.com/memic-ai/memic-python) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Memic API key and pip for SDK installation.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter reports 0.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
