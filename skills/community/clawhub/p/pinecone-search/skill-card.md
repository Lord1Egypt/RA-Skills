## Description: <br>
Pinecone vector search and document upload tool for knowledge base management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deki18](https://clawhub.ai/user/deki18) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to upload TXT and Markdown knowledge-base content to Pinecone, then query it with vector and hybrid keyword search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents and search queries are sent to configured external embedding and Pinecone services. <br>
Mitigation: Install only for workflows where that data transfer is intended, and use scoped API keys for the embedding provider and Pinecone. <br>
Risk: Recursive uploads can include private or unintended TXT and Markdown files. <br>
Mitigation: Run uploads with --dry-run first, avoid recursive uploads of private folders, and manage retention or deletion directly in Pinecone. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deki18/pinecone-search) <br>
- [Project homepage](https://github.com/deki18/pinecone-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; runtime commands return text search results or JSON upload statistics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Pinecone and embedding-provider API keys; supports TXT and Markdown inputs, namespaces, filters, dry-run upload previews, and optional JSON output.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
