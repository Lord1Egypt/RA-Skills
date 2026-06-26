## Description: <br>
A vehicle log download and analysis tool that supports cloud log retrieval, local log processing, and automated fault analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lichm1007](https://clawhub.ai/user/lichm1007) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and vehicle diagnostics engineers use this skill to run IssueFinder commands for downloading vehicle logs by VIN and time, processing local log archives, and analyzing fault or reboot information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool can auto-download and run replacement code in a persistent user directory without integrity checks or clear approval. <br>
Mitigation: Review before installing, prefer running with --skip-version-check, and inspect or remove ~/.issuefinder/issuefinder-tool.py before use. <br>
Risk: Vehicle identifiers, time windows, and downloaded logs may be shared with the configured IssueFinder server or stored locally. <br>
Mitigation: Use only trusted IssueFinder servers, limit VIN and time queries to what is needed, and store downloaded logs in a restricted directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lichm1007/issuefinder-tool) <br>
- [Wrapper usage documentation](WRAPPER_USAGE.md) <br>
- [IssueFinder server endpoint](https://issuefinder-playground-init-dev.inner.chj.cloud) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files, Analysis] <br>
**Output Format:** [Markdown guidance with shell command examples and file outputs from the tool] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download vehicle logs to configured output directories and call the configured IssueFinder server.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
