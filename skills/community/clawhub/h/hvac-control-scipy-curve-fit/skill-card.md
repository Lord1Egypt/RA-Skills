## Description: <br>
Use scipy.optimize.curve_fit for nonlinear least squares parameter estimation from experimental data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for guidance on fitting nonlinear models to experimental data with SciPy, including first-order step-response parameter estimation and fit-quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example fitting code may produce misleading parameters if the user's data, units, model form, or bounds are inappropriate. <br>
Mitigation: Review and adapt the model, initial guesses, bounds, and fit-quality checks before using the guidance on real experimental data. <br>
Risk: Using NumPy or SciPy from untrusted package sources can introduce supply-chain risk. <br>
Mitigation: Install NumPy and SciPy only from trusted package repositories and verify dependency provenance in the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/hvac-control-scipy-curve-fit) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown with Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; examples require user adaptation to local data and model assumptions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
