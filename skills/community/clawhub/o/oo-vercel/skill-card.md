## Description: <br>
This skill lets agents operate Vercel through OOMOL's oo CLI connector for reading, creating, updating, and deleting Vercel resources instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and manage Vercel projects, domains, deployments, runtime logs, environment variables, teams, and webhooks through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform credentialed Vercel operations through an OOMOL-connected account. <br>
Mitigation: Use it only for Vercel tasks you requested, and provide account access or files only when they clearly match the intended operation. <br>
Risk: Some supported actions create, update, delete, or overwrite Vercel resources. <br>
Mitigation: Confirm the exact target, payload, and expected effect before running actions marked write or destructive. <br>
Risk: Connector inputs may change as Vercel or OOMOL connector schemas evolve. <br>
Mitigation: Fetch the live action schema with oo connector schema before constructing a payload. <br>


## Reference(s): <br>
- [Vercel homepage](https://vercel.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-vercel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses oo CLI connector schema and run commands; connector responses are JSON objects containing data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
