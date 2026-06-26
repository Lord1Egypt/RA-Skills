## Description: <br>
Learn DevOps on LabEx by helping agents find culture and toolchain courses plus CI/CD and operations labs from the public catalog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huhuhang](https://clawhub.ai/user/huhuhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners and agents use this skill to find LabEx DevOps courses and hands-on labs, narrow recommendations by goal or topic, and return public LabEx URLs for browser-based learning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is LabEx-focused and may not cover non-LabEx training options. <br>
Mitigation: Ask separately for neutral comparisons when alternatives outside LabEx are needed. <br>
Risk: Users may provide credentials even though the workflow only needs public catalog data. <br>
Mitigation: Do not provide credentials; use only public LabEx catalog and lab URLs. <br>
Risk: Recommendations could drift outside the DevOps learning path or toward protected routes. <br>
Mitigation: Keep requests to the documented public DevOps catalog routes and return public browser URLs. <br>


## Reference(s): <br>
- [LabEx DevOps API Reference](references/api.md) <br>
- [Learn DevOps on LabEx](https://labex.io/learn/devops) <br>
- [LabEx](https://labex.io) <br>
- [LabEx Reviews](https://labex.io/pricing#reviews) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown recommendations with public LabEx course or lab URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Concise recommendations; no credentials, VM routes, or protected routes are required.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
