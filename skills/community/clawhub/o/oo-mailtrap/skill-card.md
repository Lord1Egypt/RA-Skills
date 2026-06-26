## Description: <br>
Mailtrap (mailtrap.io). Use this skill for Mailtrap requests that read, create, update, or delete data through the OOMOL connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support teams use this skill to operate Mailtrap inboxes, projects, contacts, templates, sending domains, suppressions, and sending statistics from an agent session. It supports both read workflows and confirmed state-changing Mailtrap operations through the OOMOL CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The inbox-cleaning action deletes messages and is not tagged for explicit confirmation under the skill's own safety rules. <br>
Mitigation: Require explicit user confirmation of the target inbox before running clean_inbox. <br>
Risk: The skill may ask users to run one-time remote installer commands for the OOMOL CLI. <br>
Mitigation: Verify the OOMOL CLI install source before executing remote installation commands. <br>
Risk: The skill requires sensitive credentials through a connected Mailtrap account. <br>
Mitigation: Use the OOMOL-managed connection flow and avoid exposing raw Mailtrap API tokens in prompts, logs, or shell history. <br>


## Reference(s): <br>
- [ClawHub Mailtrap skill page](https://clawhub.ai/oomol/oo-mailtrap) <br>
- [Mailtrap homepage](https://mailtrap.io/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce live action schemas, connector command payloads, and Mailtrap operation guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
