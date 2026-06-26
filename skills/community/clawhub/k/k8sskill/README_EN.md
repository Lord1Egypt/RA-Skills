# K8sSkill - Kubernetes Intelligent Diagnostic Assistant

Kubernetes intelligent diagnostic tool based on SRE best practices, supports natural language conversation diagnosis within IDE.

## Quick Start

### 1. Install Dependencies

```bash
cd <skill directory>
pip install -r requirements.txt
```

For example, if skill is placed in a directory:
```bash
cd <skill directory>
pip install -r requirements.txt
```

### 2. Configure Kubernetes Connection

**Option A: Use project-included kubeconfig (already configured)**

The project has configured kubeconfig file in `config/` directory:
- `config/k8s-Test-admin.conf`

**Option B: Manually configure to default location**
```bash
# Copy kubeconfig to default location
copy C:\path\to\your\kubeconfig C:\Users\%USERNAME%\.kube\config
```

**Option C: Set environment variable**
```powershell
# Set KUBECONFIG environment variable pointing to skill directory config file
$env:KUBECONFIG="<skill directory>\config\k8s-Test-admin.conf"
```

### 3. Use in IDE

**No need to manually execute any commands!** Just describe the problem you want to check in the Trae IDE conversation.

### Example Conversation

**You:** "Check why my Pod is crashing"

**AI:** Automatically calls k8sskill for diagnosis and returns results

**Supported Query Types:**
- **Pod Issues**: "Check why Pod is crashing" / "Why is Pod restarting"
- **Deployment Issues**: "What happened to deployment" / "deployment rollout stuck"
- **Service Issues**: "Why can't I access service" / "Can't access my service"
- **Node Issues**: "Node has issues" / "Check node health status"
- **Storage Issues**: "Storage binding failed" / "PVC cannot mount"
- **Event Logs**: "View recent events" / "What warnings does cluster have"
- **Full Check**: "What problems does cluster have" / "Check all resources"

### 4. Python API Usage (Advanced)

Developers can directly use k8sskill in Python:

```python
# Execute in scripts/ directory
from orchestrator import AnalyzerOrchestrator, analyze_cluster

# Method 1: Use orchestrator
orchestrator = AnalyzerOrchestrator()
results = orchestrator.analyze("check cluster issues")
print(orchestrator.format_report(results))

# Method 2: Use convenience function
report = analyze_cluster("check why Pod is crashing", "production")
print(report)
```

---

## Troubleshooting

### Connection Failed

```bash
# Check if kubeconfig exists
dir config\

# Manually test connection
python -c "from kubernetes import config; config.load_kube_config('config/k8s-Test-admin.conf'); print('OK')"
```

### Insufficient Permissions

```bash
# Check kubectl permissions
kubectl auth can-i list pods

# Check current context
kubectl config current-context
```

### Module Import Error

```python
# Make sure to execute in scripts/ directory
# Wrong way: from scripts import AnalyzerOrchestrator
# Correct way: from orchestrator import AnalyzerOrchestrator

# Verify if import works
from orchestrator import AnalyzerOrchestrator
print("Import successful!")
```

---

## Features

- **22 Kubernetes Resource Analyzers** - Covers core resources like Pod, Deployment, Service, Node, PVC
- Natural Language Intent Recognition - Diagnose cluster issues directly through conversation
- Chinese and English Support - Full Chinese documentation and error prompts
- Structured Diagnostic Reports - Clear fault classification and fix recommendations
- Modular Design - Load on demand, easy to extend
- Pure Python Implementation - Based on kubernetes-python client
- Automatic kubeconfig Detection - Supports environment variables, default locations, and project configuration

---

## Version History

- **v1.0.0** - Major refactor: Modular architecture upgrade, extracted BaseAnalyzer, added orchestrator.py (21 analyzers)
- **v0.5.2** - Optimized error messages, added verify_k8s_connection() verification function (21 analyzers)
- **v0.4.0** - Added Secret, Gateway, HTTPRoute, Webhook analyzers (21 analyzers)
- **v0.3.0** - Added ReplicaSet, NetworkPolicy, PDB, Storage, Security analyzers (17 analyzers)
- **v0.2.0** - Added StatefulSet, Job, CronJob, HPA, ConfigMap, PVC, Node, Ingress, Event analyzers (12 analyzers)
- **v0.1.0** - Initial version, Pod, Deployment, Service analyzers (3 analyzers)

---

## License

Designed based on Kubernetes best practices and SRE experience
