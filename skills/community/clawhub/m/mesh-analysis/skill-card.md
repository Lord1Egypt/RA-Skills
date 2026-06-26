## Description: <br>
Analyzes 3D mesh files in STL format to calculate geometric properties, identify connected components, and extract binary STL attribute data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect STL mesh files, estimate volume, identify the largest connected component in noisy scan data, and read material or attribute IDs from binary STL files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Very large or malformed STL files may cause parsing errors or high memory or CPU use during local analysis. <br>
Mitigation: Only analyze mesh files the user intends the agent to read, and review unusually large or malformed inputs before running the analyzer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/mesh-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, code] <br>
**Output Format:** [Python dictionary or printed text report containing mesh analysis results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports main_part_volume, main_part_material_id, and total_components; volume units match the STL coordinate units cubed.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
