#!/bin/bash
# Start the Blender MCP server

# Check if uvx is available
if ! command -v uvx &> /dev/null; then
    echo "Error: uvx not found. Please install uv first."
    exit 1
fi

# Start blender-mcp
echo "Starting Blender MCP server..."
uvx blender-mcp
