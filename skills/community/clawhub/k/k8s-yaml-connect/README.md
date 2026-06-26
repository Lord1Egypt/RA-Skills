# Kubernetes YAML Connect Skill

A skill for connecting to Kubernetes clusters using YAML configuration files as input.

## Features

- **Apply YAML to clusters** - Deploy resources from YAML files or stdin
- **Validate YAML syntax** - Check YAML before applying to catch errors early
- **Manage kubeconfig** - Create and switch contexts from YAML configuration
- **Context switching** - Easily switch between different Kubernetes contexts
- **Dry-run support** - Test deployments without actually applying them

## Prerequisites

- `kubectl` installed and available in PATH
- Access to a Kubernetes cluster (local or remote)
- Basic understanding of Kubernetes YAML manifests

## Installation

```bash
# Make scripts executable
chmod +x scripts/*.sh
```

## Usage Examples

### Apply YAML to Cluster
```bash
# From file
./scripts/apply-yaml.sh -f deployment.yaml

# From stdin
cat service.yaml | ./scripts/apply-yaml.sh

# Dry-run (validation only)
./scripts/apply-yaml.sh -d -f ingress.yaml
```

### Validate YAML Syntax
```bash
# Basic validation
./scripts/validate-yaml.sh -f config.yaml

# Strict validation with kubeval
./scripts/validate-yaml.sh -s -f deployment.yaml
```

### Set Kubeconfig from YAML
```bash
# Load kubeconfig and switch context
./scripts/set-kubeconfig.sh -f kubeconfig.yaml -c production

# Use temporary config
./scripts/set-kubeconfig.sh -t -f temp-config.yaml
```

## Scripts

### `apply-yaml.sh`
Apply Kubernetes YAML to the current cluster context.

**Options:**
- `-f, --file FILE` - Read YAML from file (default: stdin)
- `-d, --dry-run` - Validate without applying
- `-n, --namespace NS` - Apply to specific namespace

### `validate-yaml.sh`
Validate Kubernetes YAML syntax and configuration.

**Options:**
- `-f, --file FILE` - Read YAML from file (default: stdin)
- `-s, --strict` - Enable strict validation with kubeval

### `set-kubeconfig.sh`
Set Kubernetes kubeconfig from YAML file or stdin.

**Options:**
- `-f, --file FILE` - Read kubeconfig YAML from file (default: stdin)
- `-c, --context CTX` - Switch to specific context after loading
- `-t, --temp` - Use temporary file

## Integration with OpenClaw

This skill can be used within OpenClaw to:
1. Automate Kubernetes deployments
2. Validate configuration files
3. Switch between different cluster contexts
4. Manage resources through YAML input

## Security Considerations

1. **Never commit sensitive data** in YAML files
2. **Validate YAML from untrusted sources** before applying
3. **Use namespaces** to isolate resources
4. **Apply least privilege** RBAC permissions
5. **Use Secrets** for sensitive configuration

## Troubleshooting

### Common Issues

1. **kubectl not found**: Install kubectl and ensure it's in PATH
2. **Connection refused**: Check if cluster is running and accessible
3. **Unauthorized**: Verify kubeconfig and permissions
4. **YAML syntax error**: Use validation scripts before applying

### Debug Commands
```bash
# Check kubectl version
kubectl version --short

# Check current context
kubectl config current-context

# List all contexts
kubectl config get-contexts

# Test cluster connection
kubectl cluster-info
```

## License

MIT