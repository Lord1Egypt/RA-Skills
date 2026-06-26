## Description: <br>
Connects an OpenClaw instance to Kemia for visual agent configuration management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cwendler](https://clawhub.ai/user/cwendler) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to enroll an OpenClaw workspace with a Kemia deployment, export local agent configuration, check deploy status, generate one-time Kemia login links, and import deploy-ready Kemia snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Importing from Kemia can overwrite workspace markdown files chosen by the server without local filename validation. <br>
Mitigation: Install only for trusted Kemia deployments; prefer a release that validates filenames against a fixed allowlist and shows the files or diff before overwriting workspace content. <br>
Risk: The skill stores and uses sensitive Kemia credentials for API access. <br>
Mitigation: Keep the OpenClaw workspace private, avoid sharing enrollment or one-time login URLs, and rotate credentials by reconnecting if exposure is suspected. <br>


## Reference(s): <br>
- [Kemia API v1 Reference](references/api.md) <br>
- [Kemia service](https://kemia.byte5.ai) <br>
- [ClawHub release page](https://clawhub.ai/cwendler/kemia) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, markdown] <br>
**Output Format:** [Terminal text with JSON configuration and imported OpenClaw markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; stores Kemia connection credentials in the OpenClaw workspace and can overwrite workspace markdown files during import.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
