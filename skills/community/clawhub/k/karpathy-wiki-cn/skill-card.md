## Description:

基于 Karpathy LLM Wiki 模式，为科研工作建立和维护持久化知识库。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyanbo2007](https://clawhub.ai/user/zhangyanbo2007)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to create, query, and maintain a persistent Markdown research wiki from papers, articles, notes, and related sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or update persistent local research-wiki files, so incorrect summaries, cross-references, or logs could become durable knowledge-base content.

Mitigation: Review generated diffs, keep raw sources immutable, and use version control before accepting wiki changes.

Risk: The bundled arXiv downloader can retrieve PDFs from the network and save them locally.

Mitigation: Run the downloader only when recent arXiv PDFs are expected, choose an explicit output directory, and review downloaded files before ingesting them.

## Reference(s):

- [Karpathy LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [qmd local Markdown search engine](https://github.com/tobi/qmd)
- [Marp Markdown presentation tool](https://marp.app/)
- [Karpathy Wiki ClawHub page](https://clawhub.ai/zhangyanbo2007/skills/karpathy-wiki-cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, shell commands, and local file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local raw/ and wiki/ files when the user asks the agent to ingest sources, answer durable research questions, or run wiki maintenance.]

## Skill Version(s):

1.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
