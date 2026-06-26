## Description: <br>
Analyzes and processes TOML pipe-network descriptions, including conversion to files, network loading and solving, reliability analysis, and structure/status visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spiderdking](https://clawhub.ai/user/spiderdking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate TOML configurations for fluid pipe networks, load and solve those networks, analyze operating conditions, and produce visualizations for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User- or model-controlled network and scenario names can influence local TOML and HTML output paths. <br>
Mitigation: Use trusted TOML inputs, avoid names containing path separators or '..', review generated paths before opening files, and run the skill in a sandbox until path validation and overwrite controls are added. <br>
Risk: Generated network analyses and visualizations may be incorrect if the TOML model or scenario definitions are invalid or untrusted. <br>
Mitigation: Review TOML configurations and solver logs before relying on results for engineering decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spiderdking/pipenet-skill) <br>
- [Publisher profile](https://clawhub.ai/user/spiderdking) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance, files] <br>
**Output Format:** [Structured tool responses, TOML configuration files, execution logs, and generated HTML visualizations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes TOML and HTML files locally based on network and scenario names.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
