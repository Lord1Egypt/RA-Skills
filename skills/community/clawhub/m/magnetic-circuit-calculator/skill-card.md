## Description: <br>
Calculates early motor magnetic-circuit estimates using the magnetic equivalent circuit method, including air-gap flux density, permanent-magnet working point, leakage factor, back-EMF, torque constant, magnet-thickness sweeps, and slot/pole comparisons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yongjie666888](https://clawhub.ai/user/yongjie666888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Motor designers and engineers use this skill for early-stage permanent-magnet motor estimates, parameter checks before Maxwell simulations, and rough comparisons of slot/pole layouts or magnet thickness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calculator outputs are preliminary estimates and may not capture high-precision electromagnetic behavior. <br>
Mitigation: Validate final designs with Maxwell, FEA, or equivalent engineering review before production use. <br>
Risk: Sweep mode writes a local plot image. <br>
Mitigation: Run sweep analysis in a working directory where creating hm_sweep_analysis.png is acceptable. <br>


## Reference(s): <br>
- [Silicon Steel and Permanent Magnet Material Library](references/steel_pm_materials.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and calculator output text; sweep mode may generate a PNG plot file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are preliminary engineering estimates and should be validated with higher-fidelity simulation before final design decisions.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
