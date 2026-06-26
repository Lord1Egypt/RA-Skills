## Description: <br>
Operates Zoom through an OOMOL-connected account to read, create, list, and update Zoom user and meeting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and automation agents use this skill to inspect Zoom schemas and run Zoom connector actions for user lookup and meeting scheduling or updates through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Creating or updating Zoom meetings can change real Zoom or calendar state. <br>
Mitigation: Confirm the exact action, target user or meeting ID, and JSON payload before running write actions. <br>
Risk: The connected OOMOL Zoom account or OAuth scopes may not match the user's intended account or permissions. <br>
Mitigation: Review the connected Zoom account and granted OAuth scopes in OOMOL before use, especially before write actions. <br>


## Reference(s): <br>
- [ClawHub Zoom skill page](https://clawhub.ai/oomol/oo-zoom) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Zoom homepage](https://www.zoom.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are returned as JSON with data and meta.executionId fields.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
