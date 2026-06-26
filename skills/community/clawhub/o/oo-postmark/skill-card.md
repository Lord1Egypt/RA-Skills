## Description: <br>
Postmark (postmarkapp.com). Use this skill for ANY Postmark request \u2014 reading, creating, and updating data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Postmark message, bounce, server, and template workflows through an OOMOL-connected Postmark account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires use of a connected Postmark account with sensitive credentials handled by the OOMOL connector. <br>
Mitigation: Install only when OOMOL is trusted and the connected Postmark account is intended for agent use. <br>
Risk: Write actions can send emails, batch templated emails, or modify templates. <br>
Mitigation: Review the exact payload and effect before approving email sends, batch sends, or template edits. <br>
Risk: First-time setup may require installing the oo CLI. <br>
Mitigation: Inspect the oo CLI install script before running it if the CLI is not already installed. <br>


## Reference(s): <br>
- [Postmark homepage](https://postmarkapp.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-postmark) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
