## Description:

Build and operate an OpenClaw-based local knowledge assistant that imports personal/local documents into a knowledge base and creates practice exercises during import.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sibo-zhao](https://clawhub.ai/user/sibo-zhao)

### License/Terms of Use:


## Use Case:

Developers, learners, and knowledge workers use this skill to import local notes and files into an OpenClaw knowledge workflow, then generate retrieval-practice exercises, review plans, and traceability back to source chunks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and running OpenPraxis can execute third-party package code in the user's environment.

Mitigation: Install it in a virtual environment or other isolated workspace, avoid elevated privileges, and review or pin the OpenPraxis package or source version before use.

Risk: Configured LLM providers may process imported document content.

Mitigation: Choose providers intentionally, review their data handling terms, and avoid importing sensitive content unless the selected provider and configuration are approved for it.

## Reference(s):

- [Exercise Patterns](references/exercise-patterns.md)
- [OpenPraxis Source Repository](https://github.com/Sibo-Zhao/OpenPraxis.git)
- [ClawHub Skill Page](https://clawhub.ai/sibo-zhao/skills/openclaw-knowledge-coach)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and compact JSON-like exercise records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes import summaries, exercise summaries, review plans, and source-to-exercise traceability maps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
