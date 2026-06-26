## Description: <br>
AI-agent-friendly Hologres CLI with safety guardrails and structured JSON output for database operations, schema inspection, SQL execution, data import/export, Dynamic Table lifecycle management, and GUC parameter management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenbingyu](https://clawhub.ai/user/wenbingyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to operate Hologres databases through CLI commands, inspect schemas, run guarded SQL, manage Dynamic Tables, and handle import/export, AI, volume, and model workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates database, storage, and credential-handling actions to an external pip package. <br>
Mitigation: Verify the `hologres-cli` package source before installation and pin a reviewed version. <br>
Risk: The CLI may use sensitive database, OSS, and model-provider credentials. <br>
Mitigation: Use least-privilege credentials, avoid placing secrets in chat or command-line arguments, and protect or clear `~/.hologres` history and config files. <br>
Risk: Write, destructive, import, GUC, model registration, local upload, and volume view operations can affect live systems or expose data. <br>
Mitigation: Require explicit human approval before running write, drop, truncate, import-with-truncate, GUC set, model registration/deletion, local file upload, or `volume view` operations. <br>


## Reference(s): <br>
- [Hologres CLI command reference](references/commands.md) <br>
- [AI, volume, and model commands](references/ai-volume-model.md) <br>
- [Safety features](references/safety-features.md) <br>
- [ClawHub skill page](https://clawhub.ai/wenbingyu/hologres-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance, Markdown, JSON, CSV, JSON Lines] <br>
**Output Format:** [Markdown guidance with CLI commands and structured CLI outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI output may be JSON, table, CSV, or JSONL depending on command options.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and VERSION; package.json lists 0.2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
