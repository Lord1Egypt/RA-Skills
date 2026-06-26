## Description: <br>
Semantic search over local files using all-MiniLM-L6-v2 embeddings, ms-marco-MiniLM-L-6-v2 reranking, ChromaDB, and parent-child chunking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lookupmark](https://clawhub.ai/user/lookupmark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and local knowledge workers use this skill to index approved local document folders and answer natural-language questions against their own PDFs, text files, notes, and office documents without sending the corpus to a remote search service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local index may contain sensitive document text, embeddings, file paths, and query history. <br>
Mitigation: Review allowed indexing roots before use and protect or delete the ChromaDB directory and queries.log on shared, synced, or backed-up machines. <br>
Risk: Search queries can reveal sensitive intent or document contents through the query history log. <br>
Mitigation: Avoid entering secrets or confidential strings as search queries and periodically remove queries.log when retention is not required. <br>
Risk: Indexing broad local folders can include unintended files. <br>
Mitigation: Use explicit --paths values inside the documented allowed roots and keep blocked patterns for credentials, tokens, and private configuration directories in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lookupmark/lookupmark-local-rag) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include file paths, relevance scores, matched snippets, and parent-chunk context; indexing stores document text, embeddings, file paths, and query history locally under ~/.local/share/local-rag.] <br>

## Skill Version(s): <br>
1.9.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
