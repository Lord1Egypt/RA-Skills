## Description:

Natural language search for local files (100G-1T). Supports xlsx, pptx, pdf, docx formats with location info. Triggered when user asks to search local/computer/folder content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaoshuping99](https://clawhub.ai/user/gaoshuping99)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and engineers use this skill to convert and index selected local documents, then query them with natural language through a Khoj-backed local search workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Khoj service may expose indexed local documents if bound beyond trusted local access or run in anonymous mode on a reachable network.

Mitigation: Bind the service to 127.0.0.1, avoid anonymous mode on reachable networks, and use an authenticated trusted loopback or HTTPS KHOJ_URL.

Risk: Selected local documents are indexed under ~/.khoj and query content can be sent to configured cloud LLM providers.

Mitigation: Review files before indexing, avoid sensitive content unless approved, and confirm the configured LLM provider is acceptable for the data.

Risk: Scheduled sync adds persistence and the security evidence flags the cron construction as needing review.

Mitigation: Do not enable scheduled sync until the cron construction is fixed and reviewed; prefer manual sync for sensitive folders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaoshuping99/skills/local-ai-search)
- [Khoj documentation](https://docs.khoj.dev/)
- [Khoj GitHub repository](https://github.com/khoj-ai/khoj)
- [MarkItDown GitHub repository](https://github.com/microsoft/markitdown)
- [DeepSeek API documentation](https://platform.deepseek.com/)
- [OpenAI API documentation](https://platform.openai.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style responses with source snippets, file locations, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file names, approximate worksheet or slide locations, indexed content snippets, and optional JSON output from query scripts.]

## Skill Version(s):

1.4.0 (source: server release metadata and artifact config.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
