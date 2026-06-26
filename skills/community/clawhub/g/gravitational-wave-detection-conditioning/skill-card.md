## Description: <br>
Data conditioning techniques for gravitational wave detector data. Use when preprocessing raw detector strain data before matched filtering, including high-pass filtering, resampling, removing filter wraparound artifacts, and estimating power spectral density (PSD). Works with PyCBC TimeSeries data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to condition PyCBC TimeSeries gravitational-wave strain data before matched filtering, including filtering, resampling, cropping edge artifacts, and PSD estimation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing PyCBC or related dependencies from untrusted package sources could introduce supply-chain risk. <br>
Mitigation: Install dependencies from trusted package sources, preferably inside a virtual environment. <br>
Risk: Incorrect filter, resampling, crop, or PSD parameters can produce misleading gravitational-wave analysis results. <br>
Mitigation: Validate conditioning parameters against the dataset and review outputs before relying on analysis results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wu-uk/gravitational-wave-detection-conditioning) <br>
- [PyCBC Tutorial: Waveform & Matched Filter](https://colab.research.google.com/github/gwastro/pycbc-tutorials/blob/master/tutorial/3_WaveformMatchedFilter.ipynb) <br>
- [PyCBC Filter Documentation](https://pycbc.org/pycbc/latest/html/pycbc.filter.html) <br>
- [PyCBC PSD Documentation](https://pycbc.org/pycbc/latest/html/pycbc.psd.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces preprocessing recommendations and example PyCBC snippets; does not run analyses by itself.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
