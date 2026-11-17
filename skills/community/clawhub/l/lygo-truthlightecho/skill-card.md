## Description:

Generates harmonic echo sequences from Truth x Light metrics by computing or ingesting image, profile, or manual inputs and mapping them to recursive harmonic audio parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creative developers use this skill to sonify images, LYGO creative profiles, or manual Truth x Light scores into harmonic echo WAV files and structured JSON profiles for creative audio workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill loads local integration modules and can persist generated run summaries into local agent memory.

Mitigation: Install in an isolated folder and virtual environment, inspect local resonance_engine.py and lyra_brain.py before running, and disable the 3-Brain growth block unless persistent memory writes are intended.

Risk: Daemon, queue, catalog, or publishing workflows may create side effects beyond local audio generation.

Mitigation: Avoid those workflows unless they are explicitly intended, and review commands before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-truthlightecho)
- [LYGO RESONANCE Companion Site](https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands; runtime outputs include WAV audio files and JSON echo profiles.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports image inputs, JSON profile inputs, manual Truth x Light scores, presets, duration, and seed-controlled reproducibility.]

## Skill Version(s):

0.1.0 (source: server release metadata and truthlightecho.py __version__)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
