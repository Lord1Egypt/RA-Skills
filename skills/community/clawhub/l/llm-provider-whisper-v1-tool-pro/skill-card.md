## Description:

Whisper v1转录专业版 helps agents set up and operate enterprise-style speech-to-text workflows with batch transcription, model management, GPU acceleration, custom prompts, FastAPI service deployment, quality review, and monitoring guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and transcription workflow owners use this skill to guide agents through batch audio transcription, model selection, GPU setup, output generation, and optional API service packaging for Whisper v1-based workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes remote FastAPI transcription service guidance that could expose uploaded audio, transcripts, or logs if deployed on an untrusted network.

Mitigation: Keep the service on trusted networks unless authentication, HTTPS, retention limits, and log scrubbing are added.

Risk: The skill uses install commands and batch processing patterns that can affect broad audio directories or local environments.

Mitigation: Review commands before execution and scope batch jobs to known audio directories with expected output locations.

Risk: Server security evidence says the activation scope and remote API guidance are broader than the skill purpose warrants.

Mitigation: Use the skill only for intended audio transcription workflows and avoid exposing unrelated files, services, or execution surfaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/llm-provider-whisper-v1-tool-pro)
- [PyTorch CUDA package index](https://download.pytorch.org/whl/cu121)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, YAML configuration, and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce transcription text, subtitle files, JSON reports, service setup guidance, and operational recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
