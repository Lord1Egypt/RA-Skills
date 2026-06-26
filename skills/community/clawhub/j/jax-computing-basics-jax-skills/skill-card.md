## Description: <br>
jax-skills helps agents use JAX for numerical computing and machine learning workflows, including array loading and saving, map and reduce operations, gradients, RNN-style scans, and JIT execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to work with JAX-native arrays, automatic differentiation, JIT compilation, simple recurrent scans, and numerical transformations for scientific computing and machine learning prototyping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Loading arrays from untrusted files can expose users to unsafe or unexpected file contents, especially if pickle-based workflows are introduced. <br>
Mitigation: Prefer .npy or .npz files from trusted sources and avoid loading pickle files from untrusted sources. <br>
Risk: Saving arrays can overwrite existing output files. <br>
Mitigation: Check destination paths before running save operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/jax-computing-basics-jax-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Guidance, Configuration] <br>
**Output Format:** [Markdown with Python code examples and helper functions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs focus on local JAX and NumPy array operations; save operations can overwrite destination files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
