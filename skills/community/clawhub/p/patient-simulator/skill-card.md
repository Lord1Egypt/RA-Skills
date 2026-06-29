## Description: <br>
Guides an agent through installing, configuring, running, batching, troubleshooting, and documenting AnnaAgent seeker or virtual-patient simulations from the CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sci-m-wang](https://clawhub.ai/user/sci-m-wang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agent operators use this skill to set up AnnaAgent workspaces, configure model services, generate reusable seeker simulation state, run chats or batches, and prepare the skill for public registry release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides installation and use of an external AnnaAgent package, API-backed model services, and local simulation state. <br>
Mitigation: Verify the package and model endpoints against local trust requirements before use. <br>
Risk: API keys, generated logs, run outputs, local memories, and prompt state can contain sensitive information. <br>
Mitigation: Use non-sensitive test data, keep secrets in .env-style storage, exclude generated artifacts from commits, and review logs before sharing or publishing. <br>
Risk: Full initialization, batch runs, and SFT/vLLM workflows can trigger live model calls or GPU-backed services. <br>
Mitigation: Run anna doctor, anna test model, anna test embedding, and dry-run deployment checks before costly or long-running operations. <br>


## Reference(s): <br>
- [AnnaAgent ACL 2025 paper](https://aclanthology.org/2025.findings-acl.1192/) <br>
- [AnnaAgent repository](https://github.com/sci-m-wang/AnnaAgent) <br>
- [AnnaAgent CLI Workflow Reference](references/cli-workflow.md) <br>
- [Publishing AnnaAgent Skills Publicly](references/publishing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with runnable CLI commands and concise explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file paths, endpoint placeholders, troubleshooting steps, and registry publishing checklists.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
