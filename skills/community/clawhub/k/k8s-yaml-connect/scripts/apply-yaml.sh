#!/bin/bash
# apply-yaml.sh - Apply Kubernetes YAML from stdin or file

set -e

usage() {
    cat << EOF
Usage: $0 [OPTIONS] [FILE]

Apply Kubernetes YAML configuration to the current cluster context.

Options:
  -f, --file FILE     Read YAML from file (default: stdin)
  -d, --dry-run       Validate without applying
  -n, --namespace NS  Apply to specific namespace
  -h, --help          Show this help message

Examples:
  $0 -f deployment.yaml
  $0 -n production -f service.yaml
  cat config.yaml | $0
  $0 -d -f ingress.yaml  # Dry-run validation
EOF
}

# Default values
FILE="-"
DRY_RUN=""
NAMESPACE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--file)
            FILE="$2"
            shift 2
            ;;
        -d|--dry-run)
            DRY_RUN="--dry-run=client"
            shift
            ;;
        -n|--namespace)
            NAMESPACE="-n $2"
            shift 2
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

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed or not in PATH"
    exit 1
fi

# Check cluster connectivity
if ! kubectl cluster-info &> /dev/null; then
    echo "Error: Cannot connect to Kubernetes cluster"
    echo "Current context: $(kubectl config current-context)"
    exit 1
fi

echo "Applying YAML to cluster..."
echo "Context: $(kubectl config current-context)"
if [[ -n "$NAMESPACE" ]]; then
    echo "Namespace: $NAMESPACE"
fi
if [[ -n "$DRY_RUN" ]]; then
    echo "Mode: Dry-run (validation only)"
fi
echo "---"

# Apply the YAML
if [[ "$FILE" == "-" ]]; then
    # Read from stdin
    echo "Reading YAML from stdin..."
    kubectl apply $DRY_RUN $NAMESPACE -f -
else
    # Read from file
    echo "Reading YAML from file: $FILE"
    kubectl apply $DRY_RUN $NAMESPACE -f "$FILE"
fi

if [[ $? -eq 0 ]]; then
    if [[ -n "$DRY_RUN" ]]; then
        echo "✓ YAML validation successful"
    else
        echo "✓ YAML applied successfully"
    fi
else
    echo "✗ Failed to apply YAML"
    exit 1
fi