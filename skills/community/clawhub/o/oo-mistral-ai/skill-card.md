## Description: <br>
Mistral AI (mistral.ai). Use this skill for ANY Mistral AI request - reading, creating, updating, and deleting data through the OOMOL-connected Mistral AI connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate Mistral AI through an OOMOL-connected account, including chat, agents, embeddings, moderation, OCR, audio transcription, files, libraries, conversations, batch jobs, and fine-tuning job workflows. The skill is intended for Mistral AI account operations that need schema inspection before execution and explicit review for write or destructive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a Mistral AI account through OOMOL and includes write, upload, sharing, and destructive actions. <br>
Mitigation: Review the action, target resource, and JSON payload before approving any write, upload, sharing, or delete request. <br>
Risk: First-time setup includes pipe-to-shell installer commands for the oo CLI. <br>
Mitigation: Install the oo CLI manually from trusted documentation with verification instead of letting an agent run installer commands. <br>


## Reference(s): <br>
- [Mistral AI homepage](https://mistral.ai) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the oo CLI to inspect live connector schemas and run Mistral AI actions with JSON inputs.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
