## Description:

Fit more skills in your context window - compress without losing what matters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent-skill authors use this skill to compress verbose skill Markdown into shorter variants while preserving triggers, core instructions, constraints, and visible trade-offs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compressed output can weaken a skill if safety-relevant examples or edge cases are removed.

Mitigation: Review the compressed output and diff before replacing an installed skill, especially for sensitive or high-impact workflows.

Risk: Local compression history may be retained in .learnings/skill-distiller/calibration.jsonl.

Mitigation: Review or delete the calibration file when local compression history should not persist.

Risk: Optional cloud LLM provider use may route skill text through the configured provider.

Mitigation: Use local inference for sensitive content or confirm the selected provider and API-key use are approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leegitw/skills/neon-skill-distiller)
- [Skill Homepage](https://github.com/live-neon/skills/tree/main/skill-distiller)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Full Reference Variant](reference/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with compression metrics, removed-content summary, and optional TRIGGER/ACTION/RESULT text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append local calibration history to .learnings/skill-distiller/calibration.jsonl; token counts use a 4 chars/token estimate and functionality scores are LLM-estimated.]

## Skill Version(s):

0.2.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
