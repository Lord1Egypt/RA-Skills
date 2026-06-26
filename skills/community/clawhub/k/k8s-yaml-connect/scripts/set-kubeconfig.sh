#!/bin/bash
# set-kubeconfig.sh - Set kubeconfig from YAML

set -e

usage() {
    cat << EOF
Usage: $0 [OPTIONS] [FILE]

Set Kubernetes kubeconfig from YAML file or stdin.

Options:
  -f, --file FILE     Read kubeconfig YAML from file (default: stdin)
  -c, --context CTX   Switch to specific context after loading
  -t, --temp          Use temporary file (won't modify default kubeconfig)
  -h, --help          Show this help message

Examples:
  $0 -f kubeconfig.yaml
  cat kubeconfig.yaml | $0
  $0 -f prod-config.yaml -c production
  $0 -t -f temp-config.yaml  # Use temporary config
EOF
}

# Default values
FILE="-"
CONTEXT=""
TEMP=false
KUBECONFIG_FILE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--file)
            FILE="$2"
            shift 2
            ;;
        -c|--context)
            CONTEXT="$2"
            shift 2
            ;;
        -t|--temp)
            TEMP=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            # Assume it's a file if not an option
            if [[ -f "$1" ]]; then
                FILE="$1"
            else
                echo "Error: Unknown option or file not found: $1"
                usage
                exit 1
            fi
            shift
            ;;
    esac
done

# Create kubeconfig file
if [[ "$TEMP" == true ]]; then
    KUBECONFIG_FILE=$(mktemp)
    echo "Using temporary kubeconfig: $KUBECONFIG_FILE"
else
    KUBECONFIG_FILE="$HOME/.kube/config-$(date +%Y%m%d-%H%M%S)"
    echo "Creating new kubeconfig: $KUBECONFIG_FILE"
fi

# Write kubeconfig
if [[ "$FILE" == "-" ]]; then
    echo "Reading kubeconfig YAML from stdin..."
    cat > "$KUBECONFIG_FILE"
else
    echo "Reading kubeconfig YAML from file: $FILE"
    cp "$FILE" "$KUBECONFIG_FILE"
fi

# Set KUBECONFIG environment variable
export KUBECONFIG="$KUBECONFIG_FILE"
echo "KUBECONFIG set to: $KUBECONFIG_FILE"

# Check if kubectl can read the config
if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed or not in PATH"
    exit 1
fi

echo "---"
echo "Available contexts:"
kubectl config get-contexts

# Switch to specified context
if [[ -n "$CONTEXT" ]]; then
    echo "Switching to context: $CONTEXT"
    if kubectl config use-context "$CONTEXT" &> /dev/null; then
        echo "✓ Switched to context: $CONTEXT"
    else
        echo "✗ Failed to switch to context: $CONTEXT"
        echo "Available contexts:"
        kubectl config get-contexts | tail -n +2
        exit 1
    fi
fi

echo "---"
echo "Current context: $(kubectl config current-context)"

# Test cluster connection
echo "Testing cluster connection..."
if kubectl cluster-info &> /dev/null; then
    echo "✓ Successfully connected to cluster"
    kubectl cluster-info | head -2
else
    echo "✗ Cannot connect to cluster"
    echo "Please check your kubeconfig and network connectivity"
    exit 1
fi

echo "---"
echo "To use this kubeconfig in current shell:"
echo "export KUBECONFIG=\"$KUBECONFIG_FILE\""
echo ""
echo "To make it permanent, add to your shell profile:"
echo "echo 'export KUBECONFIG=\"$KUBECONFIG_FILE\"' >> ~/.zshrc"
echo "or merge with existing config:"
echo "KUBECONFIG=\"$KUBECONFIG_FILE:~/.kube/config\" kubectl config view --flatten > ~/.kube/config.new && mv ~/.kube/config.new ~/.kube/config"