## Description: <br>
Helps an agent build and maintain a persistent research wiki using the Karpathy LLM Wiki pattern. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyanbo2007](https://clawhub.ai/user/zhangyanbo2007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and knowledge workers use this skill to ingest papers and other sources, organize generated Markdown wiki pages, answer questions from the maintained wiki, and run wiki health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated wiki edits can introduce incorrect summaries, links, or synthesis into a persistent research knowledge base. <br>
Mitigation: Use git or backups before ingest and lint operations, review generated edits, and keep the append-only log available for audit. <br>
Risk: Downloaded arXiv PDFs are external files and should not be assumed trustworthy. <br>
Mitigation: Treat downloaded PDFs as untrusted inputs and review them before relying on extracted claims. <br>
Risk: The bundled shell wrapper has a packaging or syntax issue according to the security guidance. <br>
Mitigation: Run the Python helper directly when using the downloader. <br>


## Reference(s): <br>
- [Karpathy LLM Wiki Methodology](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) <br>
- [qmd Markdown Search Engine](https://github.com/tobi/qmd) <br>
- [Marp Markdown Presentation Tool](https://marp.app/) <br>
- [arXiv API Query Endpoint](https://export.arxiv.org/api/query) <br>
- [ClawHub Skill Page](https://clawhub.ai/zhangyanbo2007/karpathy-wiki-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Text and Markdown wiki pages, research summaries, maintenance reports, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local raw source folders, wiki pages, indexes, logs, and downloaded arXiv PDFs.] <br>

## Skill Version(s): <br>
1.1.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
