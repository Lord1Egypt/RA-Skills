## Description:

Enhanced spectrogram visualization tools for professional time-frequency analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyendt](https://clawhub.ai/user/wangyendt)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create spectrograms, spectral analysis views, and time-frequency plots for IMU, physiological, vibration, and audio signals with pywayne.plot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example code may be run on sensitive biomedical or business signal data with separately installed pywayne and plotting dependencies.

Mitigation: Trust and vet those dependencies before running examples on sensitive data.

Risk: Poor STFT parameter choices can lead to misleading time-frequency interpretation.

Mitigation: Use get_specgram_params and review the documented time and frequency resolution trade-off for the signal being analyzed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Code, Guidance]

**Output Format:** [Markdown with Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces plotting guidance and example pywayne.plot calls; it does not install or execute dependencies.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
