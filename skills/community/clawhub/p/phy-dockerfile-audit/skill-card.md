## Description: <br>
Dockerfile static security auditor that scans Dockerfiles for root execution, unpinned base images, secrets in ENV or ARG, remote ADD fetches, shell-form ENTRYPOINT or CMD, sudo installation, missing .dockerignore files, privileged exposed ports, apt-get bloat, and hardcoded ARG defaults. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to audit Dockerfiles locally or in CI and identify common container security misconfigurations before images are built or released. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanner output can include matching Dockerfile lines, which may expose secret-like values if the scanned files contain real secrets. <br>
Mitigation: Run the scanner only on repositories intended for audit and avoid sharing raw output publicly when Dockerfiles may contain sensitive values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-dockerfile-audit) <br>
- [Publisher profile](https://clawhub.ai/user/PHY041) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text reports, JSON findings, or GitHub Actions annotations with file, line, severity, CWE, snippet, and fix guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CI mode exits nonzero when CRITICAL or HIGH findings are detected.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
