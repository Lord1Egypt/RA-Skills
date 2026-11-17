## Description:

This skill guides agents through matched filtering for gravitational-wave detection with PyCBC template waveforms in time-domain and frequency-domain workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, scientists, and technical agents use this skill to generate gravitational-wave template waveforms, run matched filters against conditioned detector data, calculate SNR peaks, and troubleshoot PyCBC matched-filtering workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing scientific Python dependencies can affect reproducibility or expose the host environment to package-level risk.

Mitigation: Install PyCBC and NumPy in a virtual environment or container, avoid administrator privileges, and pin package versions for reproducible or audited setups.

## Reference(s):

- [PyCBC Tutorial: Waveform & Matched Filter](https://colab.research.google.com/github/gwastro/pycbc-tutorials/blob/master/tutorial/3_WaveformMatchedFilter.ipynb)
- [PyCBC Waveform Documentation](https://pycbc.org/pycbc/latest/html/pycbc.waveform.html)
- [PyCBC Filter Documentation](https://pycbc.org/pycbc/latest/html/pycbc.filter.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers PyCBC dependency installation, waveform generation, matched-filter execution, SNR peak extraction, and troubleshooting.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
