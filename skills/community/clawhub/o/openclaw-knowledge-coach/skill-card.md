## Description: <br>
Build and operate an OpenClaw-based local knowledge assistant that imports personal/local documents into a knowledge base and creates practice exercises during import. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sibo-Zhao](https://clawhub.ai/user/Sibo-Zhao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and knowledge workers use this skill to set up OpenClaw and OpenPraxis workflows that ingest local notes or files, create traceable knowledge records, and generate retrieval-practice exercises tied to the imported content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow installs and runs a third-party CLI and may process user-selected local documents. <br>
Mitigation: Review the OpenPraxis package or source before installation, ingest only files the user chooses, and avoid sensitive files unless the user accepts the CLI and selected LLM provider handling that content. <br>
Risk: Provider API keys may be needed for model-backed ingestion and practice generation. <br>
Mitigation: Use scoped API keys and configure only the provider credentials needed for the task. <br>


## Reference(s): <br>
- [Exercise Patterns](references/exercise-patterns.md) <br>
- [OpenPraxis GitHub repository](https://github.com/Sibo-Zhao/OpenPraxis.git) <br>
- [ClawHub skill page](https://clawhub.ai/Sibo-Zhao/openclaw-knowledge-coach) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-like exercise records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected outputs include import summaries, exercise summaries, review plans, and traceability maps from source files to generated exercises.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
