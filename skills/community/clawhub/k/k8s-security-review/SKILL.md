---
name: Kubernetes Security Review
description: Analyzes Kubernetes YAML manifests for security misconfigurations, best practices violations, and compliance risks.
---

# Overview

Kubernetes Security Review is a specialized security analysis tool that scans Kubernetes YAML manifests for vulnerabilities, misconfigurations, and deviations from industry security best practices. Organizations using Kubernetes in production environments can leverage this tool to identify and remediate security gaps before deployment.

The tool performs comprehensive static analysis on Kubernetes resources, detecting issues such as missing security contexts, overly permissive RBAC configurations, exposed secrets, resource limits violations, and container image best practices. This proactive approach helps prevent common Kubernetes security incidents and ensures compliance with organizational security policies.

Ideal users include DevOps engineers, platform security teams, Kubernetes administrators, and organizations implementing security-as-code practices. The tool integrates seamlessly into CI/CD pipelines, policy enforcement workflows, and infrastructure-as-code validation processes.

## Usage

### Sample Request

```json
{
  "yaml_content": "apiVersion: v1\nkind: Pod\nmetadata:\n  name: web-app\n  namespace: production\nspec:\n  containers:\n  - name: nginx\n    image: nginx:latest\n    ports:\n    - containerPort: 80\n    securityContext:\n      runAsNonRoot: false\n      privileged: true\n    resources:\n      requests:\n        memory: \"64Mi\"\n        cpu: \"250m\"\n    volumeMounts:\n    - name: config\n      mountPath: /etc/config\n  volumes:\n  - name: config\n    secret:\n      secretName: db-credentials"
}
```

### Sample Response

```json
{
  "manifest_valid": true,
  "findings": [
    {
      "severity": "HIGH",
      "rule_id": "K8S-001",
      "category": "Security Context",
      "message": "Container running in privileged mode - potential security risk",
      "resource": "Pod/web-app/containers/nginx",
      "recommendation": "Set privileged: false and use specific capabilities instead"
    },
    {
      "severity": "HIGH",
      "rule_id": "K8S-002",
      "category": "Container Image",
      "message": "Using image tag 'latest' is not recommended in production",
      "resource": "Pod/web-app/containers/nginx",
      "recommendation": "Pin image to a specific version tag (e.g., nginx:1.25.3)"
    },
    {
      "severity": "MEDIUM",
      "rule_id": "K8S-003",
      "category": "Security Context",
      "message": "Container should run as non-root user",
      "resource": "Pod/web-app/containers/nginx",
      "recommendation": "Set runAsNonRoot: true and specify a non-zero uid"
    },
    {
      "severity": "MEDIUM",
      "rule_id": "K8S-004",
      "category": "Pod Security",
      "message": "Pod does not enforce read-only root filesystem",
      "resource": "Pod/web-app",
      "recommendation": "Set readOnlyRootFilesystem: true where possible"
    }
  ],
  "summary": {
    "total_findings": 4,
    "high_severity": 2,
    "medium_severity": 2,
    "low_severity": 0,
    "compliance_score": 65
  }
}
```

## Endpoints

### POST /review-k8s

Analyzes a Kubernetes YAML manifest for security issues, misconfigurations, and best practices violations.

**Method:** `POST`

**Path:** `/review-k8s`

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `yaml_content` | string | Yes | Complete Kubernetes YAML manifest as a string. Can include single or multiple resources (Pods, Deployments, Services, ConfigMaps, Secrets, RBAC definitions, Network Policies, etc.). |

**Request Body:**
```json
{
  "yaml_content": "<kubernetes-yaml-manifest>"
}
```

**Response (200 OK):**
Returns a comprehensive security analysis report including:
- `manifest_valid`: Boolean indicating if YAML is syntactically valid
- `findings`: Array of security findings, each containing:
  - `severity`: One of HIGH, MEDIUM, LOW
  - `rule_id`: Unique identifier for the security rule
  - `category`: Type of finding (e.g., Security Context, Container Image, Pod Security, RBAC, Secrets Management)
  - `message`: Detailed description of the issue
  - `resource`: Kubernetes resource path affected
  - `recommendation`: Remediation guidance
- `summary`: Aggregate statistics including total findings, severity breakdown, and compliance score

**Response (422 Validation Error):**
Returned when the request payload fails validation.

```json
{
  "detail": [
    {
      "loc": ["body", "yaml_content"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Pricing

| Plan | Calls/Day | Calls/Month | Price |
|------|-----------|-------------|-------|
| Free | 5 | 50 | Free |
| Developer | 20 | 500 | $39/mo |
| Professional | 200 | 5,000 | $99/mo |
| Enterprise | 100,000 | 1,000,000 | $299/mo |

## About

ToolWeb.in - 200+ security APIs, CISSP & CISM, platforms: Pay-per-run, API Gateway, MCP Server, OpenClaw, RapidAPI, YouTube.

- [toolweb.in](https://toolweb.in)
- [portal.toolweb.in](https://portal.toolweb.in)
- [hub.toolweb.in](https://hub.toolweb.in)
- [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)

## References

- **Kong Route:** https://api.mkkpro.com/security/k8s-security-review
- **API Docs:** https://api.mkkpro.com:8022/docs
