## Description: <br>
Webvizio helps agents operate Webvizio through an OOMOL-connected account by inspecting connector schemas and running supported REST Hook subscription actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage Webvizio REST Hook subscriptions through the OOMOL oo CLI, including schema inspection, subscription creation, and subscription deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Webvizio account and may operate with sensitive account credentials handled server-side. <br>
Mitigation: Connect only the intended Webvizio account and scopes, and use this skill only when managing Webvizio through OOMOL is expected. <br>
Risk: Creating REST Hook subscriptions can send Webvizio event notifications to an external callback URL. <br>
Mitigation: Confirm the exact event and callback URL with the user before running subscription creation. <br>
Risk: Deleting a REST Hook subscription removes an existing Webvizio webhook by ID. <br>
Mitigation: Confirm the target webhook ID and get explicit approval before running the destructive delete action. <br>
Risk: First-time setup may require installing the oo CLI through remote installer commands. <br>
Mitigation: Verify the oo CLI installer source before running setup commands. <br>


## Reference(s): <br>
- [Webvizio homepage](https://webvizio.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-webvizio) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
