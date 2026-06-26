## Description: <br>
Packages and deploys OpenClaw environments across local, remote, and batch hosts with sensitive-data removal, SHA256 integrity checks, conflict handling, logging, and troubleshooting guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lyx058019](https://clawhub.ai/user/lyx058019) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to package OpenClaw configurations, workspace content, skills, and deployment assets, then deploy them locally, over SSH, or to multiple hosts from an inventory. It is suited for environment migration, backup, and team-standardized OpenClaw deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Packaging may include private workspace memory, skills, notes, code, or secrets. <br>
Mitigation: Inspect archive contents before packaging or deployment and remove private or sensitive material that should not be copied. <br>
Risk: Deployment workflows can overwrite local or remote systems. <br>
Mitigation: Test with --dry-run or non-production hosts first, prefer backup or update modes, and review overwrite choices before execution. <br>
Risk: Remote deployment can expose credentials or connect to unintended hosts. <br>
Mitigation: Prefer SSH keys over password arguments, verify host keys manually for production systems, and avoid arbitrary deployment URLs. <br>


## Reference(s): <br>
- [OpenClaw Deploy ClawHub Release](https://clawhub.ai/lyx058019/lyx-openclaw-deploy) <br>
- [OpenClaw Deploy Repository](https://github.com/lyx058019/openclaw-deploy) <br>
- [OpenClaw Deploy User Guide](artifact/docs/README.md) <br>
- [Troubleshooting Guide](artifact/docs/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment guidance and commands for Bash, tar, SSH, Docker Compose, and inventory-based batch deployment workflows.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
