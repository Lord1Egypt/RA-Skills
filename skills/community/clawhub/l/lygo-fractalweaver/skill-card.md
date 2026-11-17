## Description:

LYGO FractalWeaver analyzes fractal or self-similar images and generates evolving audio textures plus structured profiles using LYGO RESONANCE-style mappings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to turn generated or user-provided fractal imagery into reproducible WAV soundscapes and JSON profiles for creative audio workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may load local companion code from the working directory and may write derived file information into persistent 3-Brain memory.

Mitigation: Run it in a clean working directory, avoid placing untrusted companion modules beside it, and review or disable memory-growth behavior before use.

Risk: Dependency behavior can vary across Python environments.

Mitigation: Pin dependencies when reproducing or publishing outputs.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/deepseekoracle/skills/lygo-fractalweaver)
- [LYGO RESONANCE Companion Site](https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash examples; generated artifacts are WAV audio files and JSON profiles.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports batch processing and seed-controlled reproducibility.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
