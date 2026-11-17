## Description:

Conduct open-ended research on a topic, building a living markdown document. Supports interactive and deep research modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brennerspear](https://clawhub.ai/user/brennerspear)

### License/Terms of Use:


## Use Case:

Developers, researchers, and other agent users use this skill to investigate open-ended questions, maintain a living markdown research document, and optionally run longer Parallel AI deep research jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance asks users to run a remote installer and broadly persist a Parallel AI API key in shell startup files.

Mitigation: Review setup before installation; prefer a pinned or package-manager uv install, use a command-scoped environment variable or secret manager, and avoid adding the API key loader to shell startup files.

Risk: Deep research prompts and findings may be saved locally and may be sent to Parallel AI.

Mitigation: Avoid entering sensitive data unless the deployment has approved Parallel AI use, and review local research folders for data-retention requirements.

Risk: System-wide installation uses elevated privileges when the user chooses that setup path.

Mitigation: Use the user-scoped ~/.local/bin symlink unless system-wide installation is intentionally required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brennerspear/skills/parallel-ai-research)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown research documents with inline shell commands and optional JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local prompt.md, research.md, and research.pdf files in a per-topic research folder.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
