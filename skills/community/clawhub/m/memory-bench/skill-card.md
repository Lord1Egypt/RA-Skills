## Description:

memory-bench benchmarks an AI agent or LLM's long-term memory with local EM/F1 scoring across 12 question types and an optional user-enabled real-model evaluation mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Developers, agent builders, AI product managers, and memory-solution evaluators use this skill to benchmark long-term memory behavior, compare memory approaches, and generate reproducible evaluation evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API evaluation mode can send benchmark text to the configured model provider.

Mitigation: Keep the default internal mode for offline use; when enabling MODEL_BACKEND=api, use a trusted REAL_API_BASE and avoid private transcripts, production memory logs, secrets, or regulated data.

Risk: Users may overstate results from the self-built memory benchmark or local self-tests.

Mitigation: Present results as reproducible local benchmark evidence and avoid claiming equivalence to official datasets or third-party certifications.

Risk: API credentials could be mishandled if users place them in files or shared command examples.

Mitigation: Provide credentials through environment variables such as REAL_API_KEY, SILICONFLOW_API_KEY, or DEEPSEEK_API_KEY, and do not commit or publish those values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoxinghua09-cell/skills/memory-bench)
- [Skill documentation](artifact/SKILL.md)
- [Security audit report](artifact/安全审计报告.md)
- [Security test results](artifact/tools/security_results.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python command examples, terminal score summaries, JSON security results, and optional SVG radar output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally by default; API evaluation is optional and sends benchmark prompts only when the user enables API mode and provides credentials.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
