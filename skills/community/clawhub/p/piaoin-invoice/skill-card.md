## Description:

对接票IN/Piaoin PAT 发票开放接口，用于下载/同步已归集发票、在本地保存发票文件与结构化数据、上传本地发票图片或 PDF 到票IN。

This skill is ready for commercial/non-commercial use.

## Publisher:

[workopilot](https://clawhub.ai/user/workopilot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to download, synchronize, summarize, and upload Piaoin invoice records and files through the Piaoin PAT API. It supports local state management, scoped user or tenant downloads, and Markdown summaries for invoice operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive invoice records and uploads.

Mitigation: Use it only when the agent is permitted to access the relevant Piaoin invoice data and confirm tenant-wide downloads are authorized.

Risk: The skill may receive and persist a Piaoin API key in local state.

Mitigation: Prefer an environment variable or secure secret store, keep .piaoin_evn out of source control, verify file permissions, and mask keys in output.

Risk: The API base URL and tenant scope can affect what data is accessed.

Mitigation: Verify BASE_URL before use and require an authorized tenant administrator key before any tenant-wide download.

## Reference(s):

- [票IN PAT API 参考](artifact/references/pat-api.md)
- [ClawHub skill page](https://clawhub.ai/workopilot/skills/piaoin-invoice)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files, Configuration, API calls, Guidance]

**Output Format:** [Markdown summaries with shell commands, local files, JSONL data, and downloaded invoice files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update .piaoin_evn and piaoin_invoice/ when local file access is available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
