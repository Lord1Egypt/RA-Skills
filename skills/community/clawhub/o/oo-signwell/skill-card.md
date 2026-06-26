## Description: <br>
SignWell (signwell.com). Use this skill for ANY SignWell request: reading, creating, and updating data through an OOMOL-connected SignWell account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate SignWell workflows from an agent, including reading account, document, and template details, creating documents from templates, sending drafts for signature, and sending reminder emails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connected-account credentials and can expose connected service data in the agent session. <br>
Mitigation: Install only when the user intends to let the agent access the connected account, and avoid using it with data that should not be visible in the session. <br>
Risk: Write actions can create documents, send drafts for signature, or send reminder emails. <br>
Mitigation: Confirm the exact payload and intended effect with the user before running any action marked as write. <br>
Risk: Connector action payloads may drift from the current service contract. <br>
Mitigation: Inspect the live action schema before building each payload. <br>


## Reference(s): <br>
- [SignWell homepage](https://www.signwell.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub SignWell skill page](https://clawhub.ai/oomol/oo-signwell) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live connector schemas should be inspected before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
