## Description:

Search and discover Hugging Face open-source models and datasets, then run OpenAI-compatible chat or embedding inference securely with cost control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to guide agents through Hugging Face model and dataset discovery, runnable model confirmation, chat completions, and embedding workflows while controlling cost and checking licenses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides agents to use Hugging Face MCP tools that can make network calls and billed inference requests.

Mitigation: Confirm this access is intended before installation, use free discovery first, set max_tokens for chat, batch embeddings, and review usage after inference.

Risk: A Hugging Face access token may be exposed or granted broader access than needed.

Mitigation: Use a least-privilege HF_TOKEN, keep it in secrets, use placeholders in shared configuration, and never print or log the token.

Risk: Generated outputs or downstream use may rely on models or datasets with incompatible licenses.

Mitigation: Check model and dataset card licenses before downstream use, record exact model or dataset ids, and re-check licenses when adopting new assets.

Risk: Embedding or caching workflows may retain private source text or derived vectors.

Mitigation: Be deliberate about caching embeddings or source text from private data, and store only what the deployment policy permits.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/simonpierreboucher02/skills/hugging-face-api)
- [Hugging Face agent playbook](artifact/SKILL.md)
- [APIs and tools reference](artifact/reference/apis-and-tools.md)
- [Best practices reference](artifact/reference/best-practices.md)
- [Models and tasks reference](artifact/reference/models-and-tasks.md)
- [Hugging Face documentation](https://huggingface.co/docs)
- [Hugging Face token settings](https://huggingface.co/settings/tokens)

## Skill Output:

**Output Type(s):** [Guidance, API calls, JSON, Markdown]

**Output Format:** [Markdown playbook with JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include selected model ids, dataset ids, license notes, token usage, chat responses, embedding vectors, and cost-control recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
