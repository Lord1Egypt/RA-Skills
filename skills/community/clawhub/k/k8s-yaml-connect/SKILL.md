---
name: k8s-yaml-connect
description: Connect to Kubernetes clusters using YAML configuration files. Use when you need to apply, validate, or manage Kubernetes resources via kubectl with YAML input. Handles kubeconfig creation, context switching, and resource deployment from YAML content.
---

# Kubernetes YAML Connect Skill

This skill enables connection to Kubernetes clusters using YAML configuration files as input. It provides tools to apply, validate, and manage Kubernetes resources through kubectl commands.

## When to Use

Use this skill when:
- You have Kubernetes YAML configuration files that need to be applied to a cluster
- You need to validate YAML syntax before deployment
- You want to create or update kubeconfig from YAML input
- You need to switch between Kubernetes contexts
- You want to check cluster status and resources

## Prerequisites

### Required
- `kubectl` must be installed and available in PATH
- Kubernetes cluster accessible (local or remote)
- Appropriate permissions for the target cluster

### Installing kubectl
If kubectl is not installed, you can install it using:

**macOS:**
```bash
# Using Homebrew
brew install kubectl

# Or download directly
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

**Linux:**
```bash
# Using package manager (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y kubectl

# Or download directly
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

**Windows:**
```powershell
# Using Chocolatey
choco install kubernetes-cli

# Or download from official release
```

**Verify installation:**
```bash
kubectl version --client
```

## Core Workflow

### 1. Validate YAML Syntax
Before applying any YAML, always validate the syntax:

```bash
kubectl apply --dry-run=client -f - <<'EOF'
[YAML_CONTENT]
EOF
```

### 2. Apply YAML to Cluster
Apply validated YAML to the current context:

```bash
kubectl apply -f - <<'EOF'
[YAML_CONTENT]
EOF
```

### 3. Create/Update Kubeconfig from YAML
If you have kubeconfig YAML, save it and update context:

```bash
# Save kubeconfig
cat > /tmp/kubeconfig.yaml <<'EOF'
[KUBECONFIG_YAML]
EOF

# Set KUBECONFIG environment variable
export KUBECONFIG=/tmp/kubeconfig.yaml

# Verify connection
kubectl cluster-info
```

### 4. Context Management
List and switch contexts:

```bash
# List available contexts
kubectl config get-contexts

# Switch to specific context
kubectl config use-context [CONTEXT_NAME]

# Get current context
kubectl config current-context
```

## Common Operations

### Deploy a Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```

### Create a Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: LoadBalancer
```

### Create a ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
```

## Error Handling

### Check for Common Issues
```bash
# Check if kubectl is installed
command -v kubectl

# Check cluster connectivity
kubectl version --short

# Check if context is set
kubectl config view --minify
```

### Validate YAML Before Applying
Always use dry-run first to catch errors:
```bash
kubectl apply --dry-run=client -f [FILE_OR_STDIN]
```

## Security Considerations

1. **Never commit sensitive data** in YAML files (use Secrets or external config)
2. **Validate YAML from untrusted sources** before applying
3. **Use namespaces** to isolate resources
4. **Apply least privilege** RBAC permissions

## Examples

### Example 1: Apply Simple Deployment
```bash
# YAML content as variable
YAML_CONTENT=$(cat <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: test
  template:
    metadata:
      labels:
        app: test
    spec:
      containers:
      - name: test
        image: nginx:alpine
EOF
)

# Apply to cluster
kubectl apply -f - <<< "$YAML_CONTENT"
```

### Example 2: Multi-resource YAML
```bash
kubectl apply -f - <<'EOF'
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  key: value
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:latest
        envFrom:
        - configMapRef:
            name: app-config
EOF
```

## References

For more detailed information, see:
- [Kubernetes Official Documentation](https://kubernetes.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [YAML Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)

## Troubleshooting

### Common Issues

1. **Connection refused**: Check if cluster is running and accessible
2. **Unauthorized**: Verify kubeconfig and permissions
3. **YAML syntax error**: Validate YAML with `kubectl apply --dry-run`
4. **Resource already exists**: Use `kubectl apply` for updates or `kubectl replace` for forced updates

### Debug Commands
```bash
# Get detailed error information
kubectl describe [RESOURCE_TYPE] [RESOURCE_NAME]

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Check pod logs
kubectl logs [POD_NAME]
```

Remember: Always test YAML in a non-production environment first when possible.