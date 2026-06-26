## Description: <br>
Operate Netlify through an OOMOL-connected account to read site, account, user, deploy, build, form, and submission data and to run deployment-related actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to inspect and manage Netlify resources from an agent session through the OOMOL `oo` CLI connector. It supports read workflows and user-confirmed state-changing deployment, build, lock, unlock, upload, and submission deletion actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act with sensitive Netlify credentials through the connected OOMOL account. <br>
Mitigation: Use only with an intended Netlify connection and rely on the server-side credential flow rather than handling raw tokens in the agent session. <br>
Risk: Write actions can change deploy, build, lock, unlock, notification, or upload state in Netlify. <br>
Mitigation: Confirm the exact target and payload with the user before running any action marked `[write]`. <br>
Risk: The `delete_submission` action removes Netlify form submission data. <br>
Mitigation: Require explicit approval for the specific submission ID before running the destructive action. <br>
Risk: Connector schemas and authentication status can change outside the artifact. <br>
Mitigation: Fetch the live action schema before constructing payloads and use first-time setup or reconnection steps only after an authentication or connection failure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-netlify) <br>
- [Netlify homepage](https://www.netlify.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke Netlify connector actions through the OOMOL `oo` CLI and return JSON-shaped action responses.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
