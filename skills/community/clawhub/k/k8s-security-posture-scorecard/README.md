# Kubernetes Security Posture Scorecard 🛡️☸️

Assess your Kubernetes cluster's security posture across 30 controls in 7 domains. Get an overall score, domain grades, critical findings, and a prioritized remediation roadmap.

## Security Domains

- **Cluster Configuration** — RBAC, anonymous auth, node restriction, audit logging, etcd encryption
- **Workload Security** — Pod security policies, privileged/root containers, image scanning, admission controllers
- **Network Security** — NetworkPolicies, TLS enforcement, service mesh, pod isolation
- **Infrastructure as Code** — IaC usage, scanning, GitOps, drift detection
- **Runtime Security** — Monitoring, Falco, FIM, audit trails, auto incident response
- **Secrets Management** — Encryption at rest, external secrets manager, no hardcoded secrets

## Quick Start

```bash
# Install via OpenClaw
clawhub install k8s-security-posture-scorecard

# Set your API key
export TOOLWEB_API_KEY="your-key-from-portal.toolweb.in"
```

## Example

Ask your AI agent:
> "Assess the security posture of our production EKS cluster running K8s 1.29 on AWS. We have RBAC enabled but most other controls are default."

## API

```
POST https://portal.toolweb.in/apis/security/k8scorecard
```

## Pricing

- Free: 5 calls/day
- Developer $39/mo: 20 calls/day
- Professional $99/mo: 200 calls/day
- Enterprise $299/mo: 100K calls/day

## Author

**ToolWeb.in** — CISSP & CISM certified | 200+ Security APIs

- 🌐 https://toolweb.in
- 🔌 https://portal.toolweb.in
- 📺 https://youtube.com/@toolweb-009
