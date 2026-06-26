---
name: k8sskill
description: Diagnose Kubernetes cluster issues. Use when users ask about Pod crashes, deployment failures, service inaccessibility, or other K8s problems.
---

# K8sSkill - Kubernetes Intelligent Diagnostic Assistant

## AI Execution Guide (Must Read)

**Follow these rules when executing diagnostics:**

**Correct Approach:**
```powershell
cd scripts
python -c "from orchestrator import analyze_cluster; print(analyze_cluster('cluster has issues'))"
```

Specify namespace:
```powershell
cd scripts
python -c "from orchestrator import analyze_cluster; print(analyze_cluster('check Pod issues', namespace='kubesphere-logging-system'))"
```

**Prohibited Actions:**
1. Do not create any additional Python script files
2. Do not create report output files
3. Do not wrap orchestrator.py functionality

---

## Usage

Users describe problems in natural language, AI automatically calls k8sskill for diagnosis.

**Trigger Examples:**
- "Check why my Pod is crashing"
- "What happened to the deployment"
- "Why can't I access the service"
- "Node has issues"
- "Storage binding failed"
- "View recent events"
- "What problems does the cluster have"

---

## Supported Query Types

| Query Type | Example Phrases |
|-------------|----------------|
| **Pod Issues** | "Check why Pod is crashing" / "Why is Pod restarting" |
| **Deployment Issues** | "What happened to the deployment" / "deployment rollout stuck" |
| **Service Issues** | "Why can't I access the service" / "Can't access my service" |
| **Node Issues** | "Node has issues" / "Check node health status" |
| **Storage Issues** | "Storage binding failed" / "PVC cannot mount" |
| **Event Logs** | "View recent events" / "What warnings does the cluster have" |
| **Full Check** | "What problems does the cluster have" / "Check all resources" |

---

## Core Capabilities

### Intelligent Resource Diagnosis (22 Analyzers)

**Workload Analyzers:**
- **PodAnalyzer** - Detects CrashLoopBackOff, OOMKilled, ImagePullBackOff, and other states
- **DeploymentAnalyzer** - Checks rolling update failures, insufficient replicas, and other issues
- **ServiceAnalyzer** - Diagnoses missing endpoints, load balancing anomalies
- **StatefulSetAnalyzer** - Checks Headless Service, StorageClass, Pod readiness status
- **JobAnalyzer** - Detects Job suspension, execution failures, timeout issues
- **CronJobAnalyzer** - Checks Cron expression format, scheduling configuration
- **ReplicaSetAnalyzer** - Checks replica creation failures, ReplicaFailure conditions
- **HPAAnalyzer** - Checks auto-scaling configuration, target resource existence, scaling limits

**Storage and Network Analyzers:**
- **PVCAnalyzer** - Detects storage binding failures, ProvisioningFailed errors
- **IngressAnalyzer** - Checks IngressClass configuration, backend Service existence, TLS certificates
- **GatewayAnalyzer** - Checks Gateway API configuration, GatewayClass existence, acceptance status
- **HTTPRouteAnalyzer** - Checks HTTPRoute-referenced Gateway, backend Service existence
- **NetworkPolicyAnalyzer** - Checks network policy scope, unapplied policies

**Cluster Analyzers:**
- **NodeAnalyzer** - Monitors node readiness status, memory/disk/PID pressure
- **EventAnalyzer** - Analyzes recent warning events, abnormal event patterns
- **StorageAnalyzer** - Checks StorageClass configuration, PV status, PVC binding
- **SecurityAnalyzer** - Checks ServiceAccount usage, container security context, privileged mode
- **WebhookAnalyzer** - Checks Validating/Mutating Webhook backend Service and Pod

**Configuration Analyzers:**
- **ConfigMapAnalyzer** - Detects unused ConfigMaps, empty configurations
- **SecretAnalyzer** - Checks unused Secrets, TLS certificate format, Docker Registry configuration
- **PDBAnalyzer** - Checks PodDisruptionBudget disruption limits, selector matching

### Natural Language Interaction

| User Input Example | Analysis Executed |
|-------------------|------------------|
| "Check why my Pod is crashing" | PodAnalyzer - Check container status and events |
| "Why can't I access the service" | ServiceAnalyzer + IngressAnalyzer |
| "What happened to the deployment" | DeploymentAnalyzer + Event analysis |
| "Storage binding failed" | PVCAnalyzer - Check PVC status |
| "Node has issues" | NodeAnalyzer - Check node health |
| "View recent events" | EventAnalyzer - Analyze warning events |
| "What problems does the cluster have" | Full analysis of all resources |

### Analysis Result Display
- **Structured Output**: Clear tables and lists displaying issues
- **Severity Classification**: Critical/Warning/Info three-level classification
- **Fix Recommendations**: Step-by-step solutions based on SRE experience
- **Related Resource Association**: Display upstream and downstream dependencies of problematic resources

---

## Usage Examples

```python
# Execute in scripts/ directory
from orchestrator import AnalyzerOrchestrator, analyze_cluster

# Method 1: Use orchestrator
orchestrator = AnalyzerOrchestrator()
results = orchestrator.analyze("check Pod issues", namespace="default")
report = orchestrator.format_report(results)
print(report)

# Method 2: Use convenience function
report = analyze_cluster("check cluster issues", namespace="production")
print(report)
```

---

## Configuration

### kubeconfig Support
Supports 3 configuration methods:
1. Project included: `config/k8s-Test-admin.conf`
2. Default location: `~/.kube/config`
3. Environment variable: `KUBECONFIG=/path/to/config`

### Quick Configuration Verification
```python
# Execute in scripts/ directory
from core import verify_k8s_connection
success, message = verify_k8s_connection()
print(message)
```

---

## Reference Documentation

- [Analyzer Detailed Description](references/analyzers.md) - Detection logic and failure patterns of each analyzer
- [Troubleshooting Manual](references/troubleshooting.md) - Troubleshooting steps for common issues

---

## Dependency Requirements

- Python 3.8+
- kubernetes-python client
- Valid kubeconfig file

---

## Usage Limitations

- This skill is a **diagnostic tool** and does not modify cluster resources
- Requires **read-only permissions** on the cluster to run
- Analysis of large clusters (>1000 Pods) may take several seconds
- Ensure kubeconfig is correctly configured before first use

---

**Version**: 1.0.0  
**Last Updated**: 2026-04-03
