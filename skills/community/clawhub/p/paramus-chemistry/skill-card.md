## Description: <br>
Hundreds of chemistry and scientific computing tools. Molecular weight, LogP, TPSA, SMILES validation, thermodynamics, polymer analysis, electrochemistry, DOE, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gressling](https://clawhub.ai/user/Gressling) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and technical users use this skill to route chemistry, molecular property, thermodynamics, materials science, electrochemistry, and scientific computing questions through Paramus tools. It helps agents discover Paramus tool schemas, call the appropriate API endpoint, and present numeric results with units. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chemistry inputs may be sent to Paramus cloud when local mode is unavailable. <br>
Mitigation: Prefer local mode for confidential molecules, formulations, or datasets; use cloud mode only with user consent for data that can be sent to Paramus. <br>
Risk: The Paramus API token could be exposed if pasted into prompts, files, logs, or command history. <br>
Mitigation: Store PARAMUS_API_TOKEN as an environment variable or secret and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [Paramus Cloud Homepage](https://cloud1.paramus.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/Gressling/paramus-chemistry) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and PARAMUS_API_TOKEN for cloud mode; local mode uses localhost when available.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
