## Description: <br>
Generates harmonic echo audio and structured profiles from Truth x Light metrics computed from images, LYGO profile JSON, or manual values. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deepseekoracle](https://clawhub.ai/user/deepseekoracle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and developers use this skill to convert images, LYGO creative profiles, or manual Truth x Light values into harmonic echo WAV audio and JSON profiles for creative sound workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional local 3-Brain memory integration may persist a summary of generated work when a compatible local lyra_brain.py is present. <br>
Mitigation: Run in a trusted project folder, review the local lyra_brain.py before use, and avoid sensitive filenames or profile contents if persistence is not desired. <br>
Risk: The skill generates local audio and profile files from user-provided image, JSON, or manual inputs. <br>
Mitigation: Use a dedicated working directory and review generated WAV and JSON outputs before sharing or importing them into other workflows. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/deepseekoracle/lygo-truthlightecho) <br>
- [LYGO RESONANCE companion site](https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; the skill runtime produces WAV audio and JSON profile files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports image, JSON profile, and manual metric inputs; can generate reproducible outputs when a seed is supplied.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and truthlightecho.py __version__) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
