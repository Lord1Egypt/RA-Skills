## Description:

Provides data conditioning techniques for gravitational wave detector data before matched filtering, including high-pass filtering, resampling, removing filter wraparound artifacts, and estimating PSD with PyCBC TimeSeries data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare raw gravitational-wave detector strain data for matched filtering by applying high-pass filtering, resampling, edge cropping, and PSD estimation in PyCBC.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing PyCBC without version review or isolation can reduce reproducibility or expose the environment to routine dependency risk.

Mitigation: Install PyCBC in a virtual environment and pin or review dependency versions for reproducible or higher-assurance analysis.

Risk: Incorrect conditioning parameters can distort detector strain data before matched filtering.

Mitigation: Review high-pass cutoff, resampling rate, crop duration, and PSD settings for the dataset, and verify conditioned strain quality before downstream analysis.

## Reference(s):

- [PyCBC Tutorial: Waveform & Matched Filter](https://colab.research.google.com/github/gwastro/pycbc-tutorials/blob/master/tutorial/3_WaveformMatchedFilter.ipynb)
- [PyCBC Filter Documentation](https://pycbc.org/pycbc/latest/html/pycbc.filter.html)
- [PyCBC PSD Documentation](https://pycbc.org/pycbc/latest/html/pycbc.psd.html)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes PyCBC TimeSeries conditioning examples, parameter guidance, and troubleshooting notes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
