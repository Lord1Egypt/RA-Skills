## Description: <br>
Organizes IMA knowledge bases by scanning content, applying configurable logical categories, generating Word and Markdown index documents, and supporting category-based RAG document generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yugaohe](https://clawhub.ai/user/yugaohe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and knowledge workers use this skill to organize IMA knowledge-base content into logical categories, keep local index documents current, and retrieve categorized source material for RAG-assisted writing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package bundles unnecessary dated workspace artifacts. <br>
Mitigation: Review the package before installation and remove the bundled dated workspace snapshot when it is not needed. <br>
Risk: The skill can store IMA knowledge-base metadata, fetched content, tracker files, reports, and cache files locally. <br>
Mitigation: Use it only with knowledge bases whose content may be stored locally, and choose the output and tracker directories deliberately. <br>
Risk: The skill can create a recurring automation task that scans and updates local index data. <br>
Mitigation: Review the generated automation prompt, schedule, and configured directories before enabling recurring execution. <br>
Risk: Server security evidence notes an old script with a hardcoded export path. <br>
Mitigation: Prefer the configurable root skill script and verify output_directory in config.json before running any bundled scripts. <br>


## Reference(s): <br>
- [IMA MCP tool capability reference](references/ima_api_reference.md) <br>
- [Category rules guide](references/category_rules.md) <br>
- [RAG workflow guide](references/rag_workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese guidance with JSON configuration, Markdown reports, shell commands, and generated Word or Markdown index files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local tracker, report, and optional content-cache files under the configured workspace path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
