## Description: <br>
Manage Komodo infrastructure, including servers, Docker deployments, stacks, builds, and procedures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weird-aftertaste](https://clawhub.ai/user/weird-aftertaste) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to inspect and administer Komodo-managed servers, deployments, stacks, builds, repositories, and procedures through the Komodo Core API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete live Komodo infrastructure. <br>
Mitigation: Use least-privilege, environment-scoped Komodo API keys and require explicit human approval before stop, restart, deploy, delete, run-build, or run-procedure actions. <br>
Risk: Stack creation can upload compose files and environment-file contents to a Komodo environment. <br>
Mitigation: Review compose and env files before use, keep production credentials separate, and upload secrets only when intended for the target environment. <br>
Risk: Komodo API credentials grant infrastructure access. <br>
Mitigation: Set credentials only in trusted sessions, avoid sharing command output that may expose environment details, and rotate or revoke keys when access is no longer needed. <br>


## Reference(s): <br>
- [Komodo API Documentation](https://komo.do/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and plain-text or JSON API output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KOMODO_ADDRESS, KOMODO_API_KEY, and KOMODO_API_SECRET environment variables for API-backed commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
