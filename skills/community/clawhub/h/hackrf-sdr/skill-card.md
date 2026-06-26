## Description: <br>
Use HackRF One SDR for frequency scanning, IQ capture, signal analysis, waterfall generation, and demodulation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arsatyants](https://clawhub.ai/user/arsatyants) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, radio engineers, and authorized SDR operators use this skill to operate a HackRF One, discover radio signals, capture IQ samples, generate spectrum and waterfall plots, analyze modulation characteristics, and demodulate captured signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad radio scanning, capture, and demodulation, which can create legal, privacy, or authorization concerns. <br>
Mitigation: Use it only on frequencies and signals the operator is legally authorized to monitor, and review proposed commands before running captures or demodulation. <br>
Risk: IQ capture files can be large and may contain sensitive radio-derived content. <br>
Mitigation: Store captures locally only as needed for analysis and delete temporary IQ files after use. <br>
Risk: Incorrect gain, bandwidth, or frequency choices can produce misleading signal analysis or saturated captures. <br>
Mitigation: Start with conservative gain settings, verify HackRF parameters, and treat modulation and signal classifications as analysis aids rather than definitive conclusions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arsatyants/hackrf-sdr) <br>
- [Frequency Band Reference](references/frequency_bands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and references to generated analysis files such as PNG plots, raw IQ captures, and WAV audio.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may involve local HackRF command execution and large local capture files.] <br>

## Skill Version(s): <br>
2.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
