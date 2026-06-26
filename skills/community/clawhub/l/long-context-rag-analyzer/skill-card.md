## Description: <br>
AI-powered long-context document analysis and RAG optimization assistant for processing 100K-2M token documents, building hybrid search indexes, evaluating retrieval quality, handling multi-document reasoning, and generating structured reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gechengling](https://clawhub.ai/user/gechengling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Financial analysts, legal professionals, researchers, and developers use this skill to design, evaluate, and optimize long-context RAG workflows for large document sets. It guides document intake, chunking, hybrid retrieval, retrieval quality evaluation, and structured report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confidential financial, legal, or internal document chunks could be exposed if embeddings, indexes, or retrieval calls are sent to unapproved external providers. <br>
Mitigation: Decide whether embeddings and indexes must remain local before use, and send sensitive chunks to external providers only when approved. <br>
Risk: RAG outputs for financial and legal documents can contain incorrect retrievals, missing citations, or misleading synthesis. <br>
Mitigation: Require source citations, evaluate retrieval quality, and keep expert review in the workflow before relying on generated findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gechengling/long-context-rag-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/gechengling) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with tables, workflow steps, configuration snippets, and structured report examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces advisory RAG analysis plans and report templates; it does not execute code or access credentials by itself.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
