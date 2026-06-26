## Description: <br>
Runs data quality checks on PMU (Phasor Measurement Unit) CSV data for frequency, voltage magnitude, phasor angle, missing data, and timestamp continuity issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clayutk](https://clawhub.ai/user/clayutk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and power-system engineers use this skill to validate PMU CSV measurements against configurable frequency, voltage, phasor-angle, missing-data, and timestamp-continuity checks before reviewing flagged operational data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PMU source measurements and generated reports may contain sensitive operational data. <br>
Mitigation: Use explicit input and output paths, store flagged CSV and HTML reports in an appropriate controlled directory, and handle derived reports with the same sensitivity as the source measurements. <br>
Risk: The skill writes local report files during normal use. <br>
Mitigation: Review the chosen output directory before execution and clean up generated reports according to the user's retention and access-control requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clayutk/pmu-data-quality-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash commands; local report outputs as stdout text, flagged-row CSV, and optional HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes flagged-row CSV files beside the input data or to an explicit output directory; optional HTML reporting depends on the skill's --html path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
