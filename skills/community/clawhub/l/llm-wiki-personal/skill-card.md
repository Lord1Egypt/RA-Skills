## Description: <br>
LLM Wiki helps an agent initialize, ingest into, query, lint, and visualize a local Markdown personal knowledge base from URLs, files, PDFs, YouTube transcripts, and pasted text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vlalamoon](https://clawhub.ai/user/vlalamoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to build and maintain an Obsidian-compatible local knowledge base. It guides the agent through initialization, source ingestion, linked Markdown page generation, wiki querying, health checks, status reporting, and knowledge graph output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL ingestion may use browser-debugging capture or a hosted defuddle.md fallback, which can expose private, authenticated, internal, or secret-bearing page content. <br>
Mitigation: Use a dedicated browser profile, avoid private or secret-bearing URLs, and review or disable the hosted fallback before ingesting sensitive material. <br>
Risk: The skill writes and updates local wiki files and may store raw captured HTML or source material locally. <br>
Mitigation: Run it only in an intended knowledge-base directory, review generated raw and wiki files, and keep backups for important local notes. <br>
Risk: The installer can overwrite local skill directories and custom --target-dir values can point outside the intended destination. <br>
Mitigation: Verify the install target before running installation, prefer default platform paths, and avoid custom target directories unless the destination has been checked. <br>
Risk: Automatic source extraction depends on optional tools, Chrome debugging mode, and external site availability, so ingestion can fail or return incomplete content. <br>
Mitigation: Treat extraction results as draft material, inspect important captures, and use the documented manual paste fallback when adapters are unavailable or incomplete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vlalamoon/llm-wiki-personal) <br>
- [Artifact README](artifact/README.md) <br>
- [Karpathy llm-wiki methodology](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) <br>
- [baoyu-url-to-markdown](https://github.com/JimLiu/baoyu-skills#baoyu-url-to-markdown) <br>
- [wechat-article-to-markdown](https://github.com/jackwener/wechat-article-to-markdown) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and generated local Markdown wiki files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local wiki files, raw source copies, indexes, logs, health-check summaries, and optional Mermaid graph output.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
