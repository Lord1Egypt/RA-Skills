## Description:

管理个人知识库，基于RAG和文本向量化技术，支持文件的保存、向量化、检索、问答、删除等功能

This skill is ready for commercial/non-commercial use.

## Publisher:

[nancyzhong2024](https://clawhub.ai/user/nancyzhong2024)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create and manage personal document knowledge bases, import files, vectorize text, retrieve relevant chunks, answer questions with RAG, and update or delete indexed files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted knowledge-base metadata or vector files may execute code when loaded through unsafe pickle deserialization.

Mitigation: Use only knowledge bases created in a trusted workspace, do not open shared or untrusted knowledge-base folders, and replace pickle storage with a safe serialized format before using sensitive documents.

Risk: Knowledge-base names or file names may write, update, or delete files outside the intended workspace if paths are not confined.

Mitigation: Validate names against a restrictive allowlist, resolve paths before file operations, require the final path to remain under the configured workspace root, and ask for explicit confirmation before update or delete actions.

Risk: Document text, retrieved chunks, and user questions may be sent to ZhipuAI for embeddings or answer generation.

Mitigation: Use a dedicated low-privilege workspace, configure the API key through an environment variable, and avoid indexing sensitive documents unless external processing has been approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nancyzhong2024/skills/personal-knowledge-base)
- [Artifact README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Natural-language responses, Python examples, shell commands, configuration snippets, and structured result dictionaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include answer text, related document chunks, source file names, relevance scores, file lists, and operation status messages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
