## Description: <br>
Natural-language read-only querying for MySQL, Redis, and MongoDB with explicit connection configuration, guarded query planning, and deterministic script executors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gakkiismywife](https://clawhub.ai/user/gakkiismywife) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn natural-language requests into guarded read-only queries against configured MySQL, Redis, and MongoDB profiles, then inspect sanitized previews and short interpretations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unclear natural-language requests may trigger broad database reads, including the noted users-table fallback. <br>
Mitigation: Review generated plans before execution, require explicit datasource/profile intent, and fix or disable broad default fallbacks before broad use. <br>
Risk: Prompts and schema context may be sent to OpenAI when OPENAI_API_KEY is configured. <br>
Mitigation: Unset OPENAI_API_KEY or use the rule-based router when prompts or schema context must remain local. <br>
Risk: Connection profiles contain database credentials and generated plan files may reveal sensitive query details. <br>
Mitigation: Use least-privileged read-only accounts, protect connections.json, and delete retained plan files after review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gakkiismywife/middleware-query) <br>
- [Configuration reference](artifact/references/config.md) <br>
- [Safety policy](artifact/references/safety-policy.md) <br>
- [Examples](artifact/references/examples.md) <br>
- [Middleware Query Plan schema](artifact/references/plan-schema.json) <br>
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON query/result previews] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs identify the datasource and profile, sanitized executed operation, count, truncated preview, and a short Chinese interpretation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
