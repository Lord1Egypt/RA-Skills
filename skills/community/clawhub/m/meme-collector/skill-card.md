## Description:

自动搜集最新网络热梗并写入 Dify 知识库，用于定期更新热梗数据库并支持去重。

This skill is ready for commercial/non-commercial use.

## Publisher:

[c4chuan](https://clawhub.ai/user/c4chuan)

### License/Terms of Use:


## Use Case:

External users and content teams use this skill to collect recent Chinese internet memes, structure them as Dify knowledge-base entries, deduplicate against existing entries, and batch upload new entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a Dify API key and may expose it through command-line arguments, chat, shell history, or logs.

Mitigation: Use a dataset-scoped, least-privilege Dify token, avoid placing the API key directly in command lines or chat, and rotate any token that may have been exposed.

Risk: The skill can write generated meme entries to a remote Dify knowledge base in batch.

Mitigation: Review generated entries and the target dataset before upload, run deduplication first, and approve the batch JSON before executing the upload command.

Risk: Collected meme details may be inaccurate or unsupported.

Mitigation: Confirm uncertain meme descriptions against reliable sources and skip entries when the origin or meaning is not clear.

## Reference(s):

- [热梗文档格式](references/meme-format.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown entries, JSON batches, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Dify dataset ID, a Dify API key, and an optional HTTP proxy; batch uploads use a JSON file of meme entries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
