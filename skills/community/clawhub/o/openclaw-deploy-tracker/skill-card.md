## Description: <br>
Records and queries OpenClaw ecosystem deployment services, including new deployments, existing services, service status, dependencies, and standardized local service records without requiring credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to maintain local Markdown records for OpenClaw-related services, including service registration, status updates, dependency notes, health checks, and port lookup workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Service records could accidentally capture credentials, private configuration contents, or unnecessary internal topology details. <br>
Mitigation: Record only credential variable names or file paths, never passwords, tokens, secret keys, private config contents, or unnecessary topology details. <br>
Risk: Local deployment notes can become stale and mislead future service checks. <br>
Mitigation: Update registry.md and the matching service record whenever service status changes, and check the registry before answering service-related questions. <br>


## Reference(s): <br>
- [OpenClaw deployment record specification](references/spec.md) <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/openclaw-deploy-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown service records with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and updates local files under memory/services; credentials should be recorded only as variable names or file paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
