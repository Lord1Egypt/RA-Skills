## Description: <br>
Mailchimp (mailchimp.com). Use this skill for ANY Mailchimp request - reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect Mailchimp schemas and run Mailchimp audience, member, tag, and merge-field actions through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access subscriber, member, and audience data from the connected Mailchimp account. <br>
Mitigation: Install it only for agents that should access that Mailchimp account, and review read results as potentially sensitive data. <br>
Risk: Write and destructive actions can update, archive, tag, upsert, or permanently delete Mailchimp members. <br>
Mitigation: Require the agent to show the exact target, payload, and expected effect, and require explicit approval before those actions run. <br>
Risk: Incorrect payloads can affect the wrong Mailchimp object or fail against the current connector contract. <br>
Mitigation: Inspect the live action schema with `oo connector schema` before constructing each payload. <br>


## Reference(s): <br>
- [ClawHub Mailchimp skill page](https://clawhub.ai/oomol/oo-mailchimp) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Mailchimp homepage](https://mailchimp.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
