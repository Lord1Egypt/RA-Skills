## Description: <br>
Deterministic handbook-grounded retrieval and thermocouple computations for reflow profile compliance outputs such as ramp, TAL, peak, feasibility, and selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Manufacturing engineers and developers use this skill to extract handbook-defined reflow limits and compute deterministic thermocouple compliance metrics for production runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process handbook content and production thermocouple or MES datasets supplied by the user. <br>
Mitigation: Scope input files intentionally and avoid providing data beyond what is needed for the compliance calculation. <br>
Risk: Calculated compliance outputs may be operationally incorrect if handbook limits, thresholds, or sensor data are wrong or incomplete. <br>
Mitigation: Validate the computed results against known examples before relying on them in production decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lnj22/manufacturing-equipment-maintenance-reflow-profile-compliance-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python code snippets and JSON-like configuration or compliance output objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deterministic sorting, stable thermocouple tie-breaks, two-decimal numeric rounding, and nulls for unavailable or invalid numeric results.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
