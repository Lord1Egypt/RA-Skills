## Description: <br>
OpenClaw Teaching helps agents maintain an OpenClaw knowledge base and generate teaching materials such as PPT or Word documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RoadheroGB](https://clawhub.ai/user/RoadheroGB) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, and OpenClaw platform users can use this skill to organize OpenClaw teaching knowledge, update knowledge entries, and prepare generated learning documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create generated documents and mutate local knowledge-base files. <br>
Mitigation: Run it in a controlled workspace, keep output paths constrained, and require explicit approval before update, delete, restore, or export actions. <br>
Risk: generate_docs.py modifies Python's import search path before importing document libraries. <br>
Mitigation: Review or remove the external sys.path insertion before installation, and prefer trusted dependencies from the active environment. <br>
Risk: The security scan labels the release suspicious because file mutation is under-disclosed. <br>
Mitigation: Review the scripts and generated backups before deployment, and document expected file writes for users. <br>


## Reference(s): <br>
- [OpenClaw Teaching on ClawHub](https://clawhub.ai/RoadheroGB/openclaw-teaching) <br>
- [README](artifact/README.md) <br>
- [Knowledge Base](artifact/KNOWLEDGE_BASE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated files may include PPTX, DOCX, or text reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, update, delete, restore, or export local knowledge-base files when its scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
