## Description: <br>
Checks for OpenClaw updates by comparing the installed version against the npm registry and reporting whether an update is available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pfrederiksen](https://clawhub.ai/user/pfrederiksen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to check whether a globally installed OpenClaw package is current, including periodic monitoring or responding to version-status questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads OpenClaw package.json from known global npm install paths and contacts the npm registry over HTTPS. <br>
Mitigation: Use it only where those read-only local version checks and outbound access to registry.npmjs.org are acceptable; it should not need credentials or write access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pfrederiksen/openclaw-update-checker) <br>
- [OpenClaw npm registry endpoint](https://registry.npmjs.org/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [Plain text status summary or JSON object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only output reports installed version, latest version, update status, newer versions, and a changelog URL when available.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
