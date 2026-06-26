## Description: <br>
Basin (usebasin.com) helps an agent read, create, update, and delete Basin data through the OOMOL-connected Basin connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage Basin projects, forms, webhooks, and submissions through a connected OOMOL account. It is intended for Basin workflows that require read access, writes, or explicit user-approved destructive operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read Basin project, form, webhook, and submission data from the connected account. <br>
Mitigation: Install it only for Basin accounts where agent access is appropriate, and treat returned submission data as account data that may need access controls. <br>
Risk: Write and destructive actions can change or remove Basin resources. <br>
Mitigation: Confirm the exact target, payload, and expected effect with the user before running any write or destructive action. <br>
Risk: The skill depends on OOMOL-connected Basin credentials. <br>
Mitigation: Use OOMOL connection management for credential setup and renewal, and avoid exposing raw credentials in prompts or files. <br>


## Reference(s): <br>
- [Basin homepage](https://usebasin.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-basin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads; action responses are JSON from the OOMOL connector.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
