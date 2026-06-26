## Description: <br>
Query HashiCorp Nomad clusters. List jobs, nodes, allocations, evaluations, and services. Read-only operations for monitoring and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danfedick](https://clawhub.ai/user/danfedick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations engineers use this skill to inspect Nomad jobs, allocations, nodes, evaluations, services, variables, and cluster health during monitoring and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Nomad allocation logs and variables can expose sensitive cluster data or secrets. <br>
Mitigation: Use a least-privilege read-only Nomad ACL token and redact logs or variables before sharing outputs. <br>
Risk: A misconfigured Nomad address, namespace, or region can cause queries against the wrong cluster scope. <br>
Mitigation: Verify NOMAD_ADDR, NOMAD_NAMESPACE, and NOMAD_REGION before running troubleshooting commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danfedick/nomad) <br>
- [Publisher profile](https://clawhub.ai/user/danfedick) <br>
- [Skill homepage](https://github.com/danfedick/nomad-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Nomad JSON output examples and filter expressions when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
