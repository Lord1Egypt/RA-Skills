## Description:

Chinese-language, game-world self-reflection skill that runs an NPC concentration quiz, scores seven axes, and returns a deterministic character-style result card with optional local HTML quiz generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dora233](https://clawhub.ai/user/dora233)

### License/Terms of Use:

MIT-0

## Use Case:

External users or agents use this skill to offer a Chinese-language, game-themed self-reflection quiz about repeated routines, expression, feedback, and service patterns. The skill can produce quiz prompts, parse answers, render a result card, list character profiles, and generate a local single-file HTML quiz.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake quiz results for psychological, medical, or workplace advice.

Mitigation: Present the built-in boundary clearly: the skill is an entertainment and self-reflection game, not a diagnostic, medical, or workplace advisory tool.

Risk: The sharp-toned result copy may feel personal, especially for high NPC concentration or high echo scores.

Mitigation: Preserve the artifact's exit protocol and disclaimer, and avoid extending the result into diagnoses, resources, or life decisions.

Risk: Calibration and HTML generation commands can modify local skill files or generated artifacts.

Mitigation: Run developer commands such as --calibrate or HTML generation only when intentionally maintaining or rebuilding the skill.

Risk: Privacy expectations may exceed what the host platform can guarantee.

Mitigation: Avoid collecting or sharing sensitive personal details, and do not treat package wording about local behavior as a guarantee about platform-level logging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dora233/skills/npc)
- [Mechanics reference](artifact/references/mechanics.md)
- [Style guide](artifact/references/style-guide.md)
- [Lines reference](artifact/references/lines.md)
- [NPC perspective writing module](artifact/references/npc-pov.md)
- [Regression prompts](artifact/references/test-prompts.md)
- [Frontend pitfalls reference](artifact/references/web-pitfalls.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown/plain text quiz prompts and result cards, plus optional generated HTML files and command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic local scoring; Chinese-language output; no network behavior found in security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
