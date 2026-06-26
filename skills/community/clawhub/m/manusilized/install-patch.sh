#!/bin/bash
# Script to apply Manusilized patches to a local OpenClaw installation

echo "🚀 Welcome to the Manusilized Patch Installer!"
echo ""

if [ -z "$1" ]; then
  echo "❌ Error: Please provide the path to your OpenClaw installation."
  echo "Usage: ./install-patch.sh /path/to/openclaw"
  exit 1
fi

OPENCLAW_PATH=$1

if [ ! -d "$OPENCLAW_PATH/src/agents" ]; then
  echo "❌ Error: Could not find src/agents in the provided path ($OPENCLAW_PATH)."
  echo "Are you sure this is the root of the OpenClaw repository?"
  exit 1
fi

echo "📦 Applying patches to $OPENCLAW_PATH..."

# Backup original files
echo "🔄 Backing up original files..."
cp "$OPENCLAW_PATH/src/agents/ollama-stream.ts" "$OPENCLAW_PATH/src/agents/ollama-stream.ts.bak"
cp "$OPENCLAW_PATH/src/agents/ollama-models.ts" "$OPENCLAW_PATH/src/agents/ollama-models.ts.bak"

# Copy patched files
echo "✨ Copying patched files..."
cp ./patches/ollama-stream.ts "$OPENCLAW_PATH/src/agents/ollama-stream.ts"
cp ./patches/ollama-models.ts "$OPENCLAW_PATH/src/agents/ollama-models.ts"

echo ""
echo "✅ Success! Manusilized patches have been applied."
echo "Please navigate to your OpenClaw directory and run 'pnpm build' to compile the changes."
echo "If you encounter any issues, you can restore the backups (.bak files)."
