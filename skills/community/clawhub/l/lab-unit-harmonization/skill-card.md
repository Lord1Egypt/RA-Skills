## Description: <br>
Provides clinical laboratory data harmonization guidance for multi-source healthcare analytics, including conventional/SI unit conversion, numeric format standardization, and data quality cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and clinical data analysts use this skill to harmonize multi-source lab values, normalize numeric formats, convert between conventional and SI units, and prepare CKD-related lab panels for analytics or model preprocessing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated harmonization guidance may encode incorrect missing-data policy or unit conversion assumptions for a specific dataset. <br>
Mitigation: Have a clinical data or biostatistics reviewer approve the missing-data policy, conversion rules, out-of-range handling, and generated code before use with real patient or research data. <br>
Risk: Dropping incomplete records can discard clinically meaningful partial panels or bias downstream analysis. <br>
Mitigation: Review missingness patterns and document an approved missing-data policy before applying complete-record filtering. <br>
Risk: Range-based unit detection can misclassify true out-of-range clinical values as unit errors. <br>
Mitigation: Validate conversions against source units where available and flag values that remain outside expected ranges for review instead of silently changing them. <br>


## Reference(s): <br>
- [CKD Lab Features Dictionary](reference/ckd_lab_features.md) <br>
- [ClawHub release page](https://clawhub.ai/wu-uk/lab-unit-harmonization) <br>
- [KDIGO Guidelines](https://kdigo.org/) <br>
- [UCUM](https://ucum.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance with Python code snippets and reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; generated code, missing-data policy, unit conversions, and out-of-range handling should be reviewed before use with clinical or research datasets.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
