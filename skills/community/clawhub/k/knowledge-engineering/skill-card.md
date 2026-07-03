## Description: <br>
Knowledge Engineering turns long RAG knowledge-base documents into semantically complete, retrieval-ready Markdown slices with validation, audit, and retrieval-evaluation gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ebandao777-oss](https://clawhub.ai/user/ebandao777-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge engineers, and RAG operators use this skill to plan, generate, validate, audit, and evaluate Markdown knowledge slices from long source documents before importing them into a RAG knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write, rewrite, or overwrite files in user-provided paths. <br>
Mitigation: Run it in a dedicated workspace, avoid important directories, and review planned output paths plus --fix or --renumber changes before applying them. <br>
Risk: Retrieval evaluation can install packages and download local embedding models. <br>
Mitigation: Preinstall dependencies manually in controlled environments or use the documented PurePythonEmbedder fallback when network or package installation is restricted. <br>
Risk: Generated slices can degrade retrieval quality or preserve source meaning incorrectly if review gates are skipped. <br>
Mitigation: Review generated Markdown slices, audit reports, and retrieval metrics before importing output into a production RAG index. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ebandao777-oss/knowledge-engineering) <br>
- [README.md](artifact/README.md) <br>
- [QUICKSTART.md](artifact/QUICKSTART.md) <br>
- [REFERENCE.md](artifact/REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML-frontmatter slice files, JSON reports, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write or rewrite files in user-provided output directories; retrieval evaluation may install or download local embedding dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 5.19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
