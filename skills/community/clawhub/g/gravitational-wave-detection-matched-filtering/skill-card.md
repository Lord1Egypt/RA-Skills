## Description: <br>
Matched filtering techniques for gravitational wave detection. Use when searching for signals in detector data using template waveforms, including both time-domain and frequency-domain approaches. Works with PyCBC for generating templates and performing matched filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and scientific computing practitioners use this skill to apply PyCBC matched filtering workflows to gravitational-wave detector data, including template generation, SNR calculation, and troubleshooting time-domain or frequency-domain approaches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Python examples and package installation commands may be copied into an analysis environment without review. <br>
Mitigation: Run examples in a controlled environment, install PyCBC and NumPy from trusted package sources, and review code against local detector data and analysis requirements before use. <br>
Risk: Matched-filtering guidance can produce misleading SNR results if templates, PSDs, sampling rates, or crop windows do not match the data pipeline. <br>
Mitigation: Validate template dimensions, frequency cutoffs, PSD assumptions, and crop amounts against the target dataset before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/gravitational-wave-detection-matched-filtering) <br>
- [PyCBC Tutorial: Waveform and Matched Filter](https://colab.research.google.com/github/gwastro/pycbc-tutorials/blob/master/tutorial/3_WaveformMatchedFilter.ipynb) <br>
- [PyCBC Waveform Documentation](https://pycbc.org/pycbc/latest/html/pycbc.waveform.html) <br>
- [PyCBC Filter Documentation](https://pycbc.org/pycbc/latest/html/pycbc.filter.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes scientific-computing guidance for PyCBC matched filtering; does not execute code by itself.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
