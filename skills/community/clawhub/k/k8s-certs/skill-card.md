## Description: <br>
Kubernetes certificate management with cert-manager. Use when managing TLS certificates, configuring issuers, or troubleshooting certificate issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rohitg00](https://clawhub.ai/user/rohitg00) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and platform engineers use this skill to inspect cert-manager resources, create certificate and issuer manifests, troubleshoot certificate readiness, and connect TLS certificates to Kubernetes Ingress resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes ready-to-run Kubernetes manifests and kubectl apply examples that can change live clusters. <br>
Mitigation: Use least-privileged Kubernetes credentials, confirm the active context and namespace, inspect each manifest, and require explicit approval before applying changes. <br>
Risk: Production Let's Encrypt issuers and Ingress changes can affect public TLS issuance and application traffic. <br>
Mitigation: Test issuer configuration in staging first, verify DNS and Ingress settings, and review production changes before execution. <br>


## Reference(s): <br>
- [Kubernetes Skills on ClawHub](https://clawhub.ai/rohitg00/k8s-certs) <br>
- [Let's Encrypt Staging ACME Directory](https://acme-staging-v02.api.letsencrypt.org/directory) <br>
- [Let's Encrypt Production ACME Directory](https://acme-v02.api.letsencrypt.org/directory) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline command and Kubernetes manifest examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include kubectl apply examples that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
