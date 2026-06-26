## Description: <br>
InspirAI Deploy helps agents detect a project's deployment strategy, run pre-deployment checks, execute releases, and monitor deployments across Kubernetes/Helm, Docker Compose, Vercel, and Fly.io. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexxxiong](https://clawhub.ai/user/alexxxiong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to initialize deployment configuration, check deployment readiness, run deployments, and monitor rollout health for common container and platform deployment targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect live or production-like deployment environments. <br>
Mitigation: Require explicit user confirmation before every deploy and review generated commands before execution. <br>
Risk: Bypass flags such as skip-check or force can weaken deployment safeguards. <br>
Mitigation: Restrict bypass flags to disposable development environments or cases where checks are technically blocked. <br>
Risk: Use with real deployment credentials can expose or misuse sensitive access. <br>
Mitigation: Review before installation in credentialed environments and avoid writing secrets into generated configuration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alexxxiong/inspirai-deploy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell snippets and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose deployment commands and generate or update deployment configuration such as .deploy.yaml.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
