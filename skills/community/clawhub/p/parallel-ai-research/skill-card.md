## Description: <br>
Conduct open-ended research on a topic, building a living markdown document. Supports interactive and deep research modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrennerSpear](https://clawhub.ai/user/BrennerSpear) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to research questions, compare options, maintain a living markdown research document, and optionally run deeper asynchronous research through the Parallel AI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup references helper commands for deep research and PDF export that should be verified before use. <br>
Mitigation: Verify the parallel-research and export-pdf scripts from a trusted source before enabling deep research or PDF export. <br>
Risk: Setup asks users to persist a Parallel AI API key locally. <br>
Mitigation: Use a scoped or revocable API key, store it with restrictive file permissions, and rotate it if exposed. <br>
Risk: The setup flow includes system-wide symlink and shell installation options. <br>
Mitigation: Prefer user-local symlinks and a trusted uv installation method unless system-wide installation is required. <br>


## Reference(s): <br>
- [OpenClaw](https://openclaw.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/BrennerSpear/parallel-ai-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research notes with optional shell commands and PDF export guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local prompt, research, and PDF files in a per-topic research folder.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
