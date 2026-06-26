#!/bin/bash
# validate-yaml.sh - Validate Kubernetes YAML syntax

set -e

usage() {
    cat << EOF
Usage: $0 [OPTIONS] [FILE]

Validate Kubernetes YAML syntax and configuration.

Options:
  -f, --file FILE     Read YAML from file (default: stdin)
  -s, --strict        Enable strict validation (kubeval)
  -h, --help          Show this help message

Examples:
  $0 -f deployment.yaml
  cat config.yaml | $0
  $0 -s -f ingress.yaml  # Strict validation with kubeval
EOF
}

# Default values
FILE="-"
STRICT=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--file)
            FILE="$2"
            shift 2
            ;;
        -s|--strict)
            STRICT=true
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

echo "Validating Kubernetes YAML..."
echo "---"

# Basic kubectl validation
if [[ "$FILE" == "-" ]]; then
    echo "1. Basic kubectl validation (dry-run):"
    if kubectl apply --dry-run=client -f - &> /dev/null; then
        echo "   ✓ Syntax is valid"
    else
        echo "   ✗ Syntax errors detected"
        exit 1
    fi
else
    echo "1. Basic kubectl validation (dry-run) for file: $FILE"
    if kubectl apply --dry-run=client -f "$FILE" &> /dev/null; then
        echo "   ✓ Syntax is valid"
    else
        echo "   ✗ Syntax errors detected"
        exit 1
    fi
fi

# Strict validation with kubeval if available and requested
if [[ "$STRICT" == true ]]; then
    if command -v kubeval &> /dev/null; then
        echo "2. Strict validation with kubeval:"
        if [[ "$FILE" == "-" ]]; then
            # Save stdin to temp file for kubeval
            TEMP_FILE=$(mktemp)
            cat > "$TEMP_FILE"
            kubeval "$TEMP_FILE"
            rm "$TEMP_FILE"
        else
            kubeval "$FILE"
        fi
    else
        echo "2. kubeval not installed. Install with: brew install kubeval"
        echo "   or see: https://github.com/instrumenta/kubeval"
    fi
fi

# YAML linting if yamllint is available
if command -v yamllint &> /dev/null; then
    echo "3. YAML linting:"
    if [[ "$FILE" == "-" ]]; then
        # Save stdin to temp file for yamllint
        TEMP_FILE=$(mktemp)
        cat > "$TEMP_FILE"
        yamllint "$TEMP_FILE" || true
        rm "$TEMP_FILE"
    else
        yamllint "$FILE" || true
    fi
else
    echo "3. yamllint not installed. Install with: brew install yamllint"
    echo "   or: pip install yamllint"
fi

echo "---"
echo "✓ YAML validation complete"