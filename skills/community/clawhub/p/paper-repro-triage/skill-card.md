## Description: <br>
Paper Repro Triage guides agents through Chinese-language AI paper reproducibility triage by reading paper evidence, finding or cloning likely official code, tracing dataset sources, locating data-processing logic, and writing a Markdown report or scaffolded PyTorch project without running training. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slight-leaves](https://clawhub.ai/user/slight-leaves) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to assess reproducibility for ML, AI, LLM, CV, NLP, multimodal, benchmark, prompt-engineering, and agent papers. It gathers local and online code evidence, inspects data-processing paths, and produces a Chinese Markdown report before any dependency installation, dataset download, training, evaluation, or inference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create a local paper-repro-workspace and clone official or likely-official research repositories for inspection. <br>
Mitigation: Review cloned code before installing dependencies, downloading datasets, running training, running evaluation, or executing inference. <br>
Risk: Generated requirements or scaffolded project files may include assumptions from incomplete paper evidence. <br>
Mitigation: Confirm generated requirements, TODO markers, and ASSUMPTION fields against the paper and repository documentation before use. <br>
Risk: A reproducibility report can influence downstream decisions even when code, data, or protocol evidence is incomplete. <br>
Mitigation: Use the report's unresolved items and manual-confirmation sections to gate any follow-on reproduction work. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/slight-leaves/paper-repro-triage) <br>
- [Dataset Source Tracing](references/dataset-source-tracing.md) <br>
- [No-Code Reproduction Workflow](references/no-code-reproduction.md) <br>
- [Output Report Template](references/output-template.md) <br>
- [Reproducibility Rubric](references/reproducibility-rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Chinese chat summary, Markdown report, and optional PyTorch project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports under paper-repro-workspace and may create a local reproduction scaffold when paper evidence supports it.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
