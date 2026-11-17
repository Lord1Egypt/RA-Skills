## Description:

Find potential token waste in OpenClaw or Hermes Agent by reviewing model choices, large instructions, recurring tasks, and related evidence, then suggest safe next steps without changing settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asif2bd](https://clawhub.ai/user/asif2bd)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to audit OpenClaw or Hermes Agent setups for likely token waste, costly model choices, oversized context, and recurring automation review candidates. It produces prioritized recommendations and caveats while leaving configuration, schedules, and credentials unchanged.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated audit reports can disclose model names, agent IDs, file basenames, and findings that reveal private operational details.

Mitigation: Review and sanitize reports before sharing them outside the trusted operational context.

Risk: The skill reads explicitly selected config/profile files and local diagnostics, which may be sensitive even when raw values are not printed.

Mitigation: Run it only in a trusted local agent session, use sanitized exports when practical, and avoid publishing real configs or reports.

Risk: OpenClaw live diagnostics may contact configured services or update native caches through the installed OpenClaw CLI.

Mitigation: Use live mode only when those local read-only side effects are acceptable; otherwise provide offline JSON exports.

Risk: Optimization recommendations are review candidates, not measured savings or automatic fixes.

Mitigation: Validate each proposed change against current policy, model availability, and before/after measurements before changing production settings.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/asif2bd/skills/openclaw-token-optimizer)
- [Agent quick start](artifact/references/QUICKSTART.md)
- [Hermes Agent compatibility](artifact/references/HERMES.md)
- [Provider policy](artifact/references/PROVIDERS.md)
- [Security policy](artifact/SECURITY.md)
- [OpenClaw 2026.9.4 release documentation](https://docs.openclaw.ai/releases/2026.9.4)
- [OpenAI Codex model documentation](https://developers.openai.com/codex/models)
- [Hermes Agent pinned compatibility source](https://github.com/NousResearch/hermes-agent/tree/d7b836ab1c0cddaafc109ed24c9a83b6191cdc88)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Plain-language Markdown guidance with optional JSON reports and read-only shell command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports intentionally avoid raw config, prompts, credentials, and environment values; selected model, agent, file, and finding identifiers may still be sensitive.]

## Skill Version(s):

4.1.1 (source: SKILL.md frontmatter, CHANGELOG.md, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
