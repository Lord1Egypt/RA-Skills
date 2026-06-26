## Description: <br>
lexoffice (office.lexware.de). Use this skill for any lexoffice request involving reading, creating, or updating data through the OOMOL-connected lexoffice connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business operators use this skill to let an agent work with lexoffice records through an OOMOL-connected account, including profiles, organization metadata, contacts, articles, and voucher metadata. It supports read workflows and confirmed write workflows for creating or updating contacts and articles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and update business records in a connected lexoffice account. <br>
Mitigation: Install it only when agent access to that lexoffice account is intended, and review requested operations against the account context before use. <br>
Risk: Write actions can create or update contacts and articles. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running any action marked as write. <br>
Risk: First-time setup may require installing the oo CLI. <br>
Mitigation: Run the optional installer only from trusted OOMOL sources and only when the CLI is actually missing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-lexoffice) <br>
- [lexoffice homepage](https://office.lexware.de/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the oo CLI to inspect live connector schemas and run lexoffice actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
