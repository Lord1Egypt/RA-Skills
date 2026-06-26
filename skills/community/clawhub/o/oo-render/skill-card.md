## Description: <br>
Operate Render through an OOMOL-connected account for reading services, workspaces, deploys, and initiating supported service operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Render users, workspaces, services, service details, and deploy history, and to request controlled deploy, restart, resume, suspend, or rollback actions through an OOMOL-connected Render account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change Render service state, including deploy, restart, resume, suspend, and rollback operations. <br>
Mitigation: Require explicit user confirmation of the target service, payload, and expected effect before running any state-changing action. <br>
Risk: Evidence security guidance notes that suspend_service is not clearly marked with the same state-changing tag as other write actions. <br>
Mitigation: Treat suspend_service as a write action and require the same confirmation standard used for deploy, restart, resume, and rollback. <br>
Risk: The skill depends on an installed and authenticated oo CLI connected to a Render account. <br>
Mitigation: Run installation, login, or Render connection steps only after a command fails with a matching setup or authentication error. <br>


## Reference(s): <br>
- [ClawHub Render Skill](https://clawhub.ai/oomol/oo-render) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [Render Homepage](https://render.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads; setup guidance is used only after authentication or connection failures.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
