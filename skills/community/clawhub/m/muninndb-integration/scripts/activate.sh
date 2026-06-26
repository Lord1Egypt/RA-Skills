#!/bin/bash

# Activate MuninnDB integration

# Test connection
echo "Testing MuninnDB connection..."
if ! curl -s http://localhost:8475/health > /dev/null 2>&1; then
    echo "ERROR: MuninnDB not running"
    exit 1
fi

echo "MuninnDB connection OK"

# Create Hermes vault if needed
if ! mbpc --host localhost:8475 --command list_vaults | grep -q hermes-agent; then
    echo "Creating vault 'hermes-agent'..."
    mbpc --host localhost:8475 --command create_vault --vault hermes-agent
fi

echo "Integration activated!"