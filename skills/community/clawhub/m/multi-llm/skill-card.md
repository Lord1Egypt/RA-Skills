## Description:

Queries multiple LLM providers in parallel and synthesizes their responses with a Mixture of Agents pattern for complex reasoning, code review, research, planning, and other quality-sensitive tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goodmorning0000](https://clawhub.ai/user/goodmorning0000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need a synthesized answer from multiple available models rather than relying on one LLM for complex analysis, research, code review, or strategic planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, code, and intermediate model outputs may be sent to configured external AI providers.

Mitigation: Avoid secrets, regulated data, private source code, and other sensitive inputs unless provider approval and data handling requirements have been reviewed.

Risk: The skill can write model output to a user-selected path.

Mitigation: Review output paths before execution and avoid startup files, shell configuration, repository hooks, credentials, or agent memory/configuration files.

Risk: Financial or trading prompts may produce unreliable decision support.

Mitigation: Use outputs as review material only and require qualified human validation before financial or trading decisions.

Risk: An untrusted Ollama endpoint could expose prompts or return untrusted model output.

Mitigation: Keep OLLAMA_HOST local or point it only at a trusted endpoint.

## Reference(s):

- [MoA (Mixture of Agents) Guide](references/moa-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/goodmorning0000/skills/multi-llm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text by default, with optional JSON containing the synthesis, synthesizer, rounds, and proposer responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and at least one configured LLM provider endpoint or local Ollama host.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
