## Description: <br>
自动搜集最新网络热梗并写入 Dify 知识库，支持与已有文档去重，用于定期更新热梗数据库。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c4chuan](https://clawhub.ai/user/c4chuan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content operators and developers use this skill to search Chinese web sources for recent memes, structure entries in Markdown, deduplicate them against an existing Dify dataset, and upload new entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes new documents to a selected Dify dataset. <br>
Mitigation: Use it only with the intended dataset and review generated meme JSON before upload when the knowledge base is production or customer-facing. <br>
Risk: The workflow requires a Dify API key and can use a proxy. <br>
Mitigation: Use a least-privileged Dify API key, keep credentials out of prompts and logs, and avoid untrusted proxies. <br>
Risk: Shell commands receive dataset, API key, proxy, and JSON file arguments. <br>
Mitigation: Quote or safely pass command arguments and verify generated file paths before execution. <br>


## Reference(s): <br>
- [Meme format reference](references/meme-format.md) <br>
- [Dify API endpoint](https://api.dify.ai/v1) <br>
- [ClawHub skill page](https://clawhub.ai/c4chuan/meme-collector) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown guidance, JSON batches, shell commands, and Dify API requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured meme documents and upload summaries; requires a Dify dataset ID and API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
