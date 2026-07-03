## Description: <br>
Token消耗优化器 helps developers audit API, RAG, Agent, and tool-output token usage, then produce prioritized optimization plans with cost estimates, Pre-LLM compression, and CCR reversible-compression guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqyougitcom](https://clawhub.ai/user/qqyougitcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI operations teams use this skill to diagnose token spend, compare model costs, plan budgets, compress large contexts or tool outputs, and define quality-checked cost-reduction steps for API, RAG, and multi-agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect sensitive failure or session logs while diagnosing token usage. <br>
Mitigation: Use it only in trusted environments, redact logs before analysis, and avoid exposing secrets or sensitive user data. <br>
Risk: Self-repair or configuration guidance could alter agent behavior if applied without review. <br>
Mitigation: Prefer dry-run recommendations, back up configuration, and require explicit approval before any configuration writes. <br>
Risk: Aggressive compression, truncation, or model routing can reduce available context and affect output quality. <br>
Mitigation: Validate changes with A/B checks, keep quality-drop thresholds explicit, and preserve original data for CCR retrieval when completeness matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/mimo-token-optimizer) <br>
- [Token optimization details reference](artifact/references/details.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Chinese Markdown with tables, checklists, estimates, and optional code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces quantitative token and cost estimates, prioritized mitigations, and quality checks; configuration or execution changes require the calling agent or user to apply them.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
