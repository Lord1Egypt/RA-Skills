## Description: <br>
Protein, peptide, antibody, nanobody, binder, enzyme, and sequence design workflows using Boltzgen, RFdiffusion, RFdiffusion2, RFdiffusion3, ProteinMPNN, LigandMPNN, and BindCraft through SciMiner APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sciminer](https://clawhub.ai/user/sciminer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Scientists, developers, and external users use this skill to choose and run SciMiner protein-design workflows for binder generation, backbone design, enzyme scaffolding, sequence design, and multi-step design pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a user-provided SciMiner API key. <br>
Mitigation: Store the key only in the declared credential file, do not commit it to repositories, and avoid printing or persisting it in prompts, logs, or generated files. <br>
Risk: Protein, ligand, target-structure, or research files may be uploaded to SciMiner to run remote design jobs. <br>
Mitigation: Upload only files that are acceptable to share with SciMiner, and avoid sensitive unpublished data unless SciMiner is approved for that use. <br>
Risk: Incorrect protein-design parameters can produce failed jobs or misleading design results. <br>
Mitigation: Read the selected SciMiner tool API documentation before each invocation and use its exact parameters, file-upload rules, and allowed values. <br>


## Reference(s): <br>
- [Protein Design on ClawHub](https://clawhub.ai/sciminer/protein-design) <br>
- [SciMiner Tool API Files](https://sciminer.tech/tool_api_files/) <br>
- [SciMiner API Key Utility](https://sciminer.tech/utility) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Markdown] <br>
**Output Format:** [Markdown summaries with invocation code or commands, task identifiers, and SciMiner share URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include selected tool documentation citations and remote job status details.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
