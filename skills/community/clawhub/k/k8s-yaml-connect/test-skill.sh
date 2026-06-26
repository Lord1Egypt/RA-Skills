#!/bin/bash
# test-skill.sh - Test the k8s-yaml-connect skill

echo "Testing k8s-yaml-connect skill..."
echo "=================================="

# Check if scripts are executable
echo "1. Checking script permissions..."
for script in scripts/*.sh; do
    if [[ -x "$script" ]]; then
        echo "   ✓ $script is executable"
    else
        echo "   ✗ $script is not executable"
        exit 1
    fi
done

# Test YAML validation
echo ""
echo "2. Testing YAML validation..."
if ./scripts/validate-yaml.sh -f examples/nginx-deployment.yaml 2>&1 | grep -q "✓ Syntax is valid"; then
    echo "   ✓ YAML validation passed"
else
    echo "   ✗ YAML validation failed"
    ./scripts/validate-yaml.sh -f examples/nginx-deployment.yaml
fi

# Test dry-run application
echo ""
echo "3. Testing dry-run application..."
if kubectl version --short &> /dev/null; then
    if ./scripts/apply-yaml.sh -d -f examples/nginx-deployment.yaml 2>&1 | grep -q "✓ YAML validation successful"; then
        echo "   ✓ Dry-run application passed"
    else
        echo "   ✗ Dry-run application failed"
        ./scripts/apply-yaml.sh -d -f examples/nginx-deployment.yaml
    fi
else
    echo "   ⚠ kubectl not available or cluster not connected"
    echo "   Skipping application tests"
fi

# Test script help messages
echo ""
echo "4. Testing help messages..."
for script in scripts/*.sh; do
    script_name=$(basename "$script")
    if "$script" --help 2>&1 | grep -q "Usage:"; then
        echo "   ✓ $script_name help works"
    else
        echo "   ✗ $script_name help failed"
    fi
done

echo ""
echo "=================================="
echo "Skill test completed!"
echo ""
echo "To use this skill in OpenClaw:"
echo "1. The skill directory is ready at: $(pwd)"
echo "2. You can publish it to ClawHub with: clawhub publish"
echo "3. Or use it locally by referencing the SKILL.md file"
echo ""
echo "Example usage in OpenClaw:"
echo "  When the user provides Kubernetes YAML, use the scripts to:"
echo "  - Validate the YAML first"
echo "  - Apply it to the cluster"
echo "  - Manage kubeconfig if needed"