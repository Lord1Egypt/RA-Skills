## Description:

Li PhotoIndexWithLLM helps agents scan local photo directories, index image content with vision-language models, and search photos by natural-language queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add command-line photo scanning, indexing, and semantic search to personal or workflow agents, with JSON output for downstream parsing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private, family, work, or document photos may be sent to a configured non-local model endpoint.

Mitigation: Use only a verified loopback endpoint such as localhost or 127.0.0.1, and keep REMOTE_LLM_ENABLED=false unless remote analysis is intentional.

Risk: The local index stores full file paths and derived photo descriptions in plaintext.

Mitigation: Protect the SQLite database with local file permissions, avoid indexing sensitive directories unless necessary, and remove the database when the index is no longer needed.

Risk: Local API keys or endpoint settings in .env may expose access to model services.

Mitigation: Keep .env private, restrict its permissions, and avoid committing it or sharing it with skill outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/43622283/skills/li-photoindexwithllm)
- [Publisher profile](https://clawhub.ai/user/43622283)
- [English README](artifact/README_EN.md)
- [Privacy guide](artifact/PRIVACY_GUIDE.md)
- [Privacy and data security report](artifact/PRIVACY.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Command-line text and JSON search, scan, statistics, and connection-test results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local file paths, derived photo descriptions, tags, counts, and model connection status.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
