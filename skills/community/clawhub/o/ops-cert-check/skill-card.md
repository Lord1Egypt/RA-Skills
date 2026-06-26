## Description: <br>
SSL/TLS Certificate Check & Renewal SOP. Covers certificate validation (PEM/CRT/JKS), Nginx certificate update, Let's Encrypt wildcard application, and emergency response for expired certificates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freepengyang](https://clawhub.ai/user/freepengyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Ops and infrastructure engineers use this skill as a runbook for checking certificate validity, updating Nginx and JKS certificates, issuing Let's Encrypt wildcard certificates, and responding to expired-certificate incidents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Certificate maintenance can involve privileged systems, private keys, keystore passwords, and DNS API credentials. <br>
Mitigation: Use the guidance only on systems you are authorized to administer, keep secrets out of chat and version control, and store private keys in approved server paths or a secrets manager. <br>
Risk: Incorrect certificate replacement, certbot plugin installation, service reloads, or renewal hooks can disrupt TLS service. <br>
Mitigation: Verify package sources, run configuration tests and renewal dry-runs before applying changes, and review cron deploy hooks before enabling automatic renewal. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freepengyang/ops-cert-check) <br>
- [Alibaba Cloud CLI credential configuration](https://help.aliyun.com/zh/cli/configure-credentials) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes certificate validation, Nginx reload, certbot renewal, and emergency response procedures.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
