## Description:

Use this skill whenever the user wants an agentic LLM to install, configure, initialize, run, batch, troubleshoot, or document AnnaAgent seeker/virtual-patient simulation from the CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sci-m-wang](https://clawhub.ai/user/sci-m-wang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agent operators use this skill to run AnnaAgent as a psychological-counseling seeker or virtual-patient simulator from the CLI, including setup, workspace configuration, reusable prompt-state initialization, chat, batch runs, troubleshooting, and public skill publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running AnnaAgent can introduce ordinary package and environment risk.

Mitigation: Pin anna-agent to a reviewed version and use a controlled Python tool environment before running generated commands.

Risk: Model endpoint credentials, .env files, logs, local memories, and generated runs may contain sensitive data.

Mitigation: Keep those files out of commits, avoid printing real keys, and review outputs before sharing or publishing.

Risk: Costly or long-running initialization and model-service workflows can fail when configuration or live connectivity is wrong.

Mitigation: Run anna doctor, anna test model, anna test embedding, and dry-run deployment checks before full initialization or vLLM deployment.

## Reference(s):

- [AnnaAgent CLI Workflow Reference](references/cli-workflow.md)
- [ACL 2025 AnnaAgent Paper](https://aclanthology.org/2025.findings-acl.1192/)
- [AnnaAgent Repository](https://github.com/sci-m-wang/AnnaAgent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with runnable shell command blocks and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AnnaAgent paper and repository attribution, diagnostic checks, and warnings about secrets, logs, local memories, and generated runs.]

## Skill Version(s):

0.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
