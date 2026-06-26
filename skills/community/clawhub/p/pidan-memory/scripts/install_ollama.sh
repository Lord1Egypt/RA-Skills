#!/bin/bash
# Install Ollama and download embedding model
# Usage: ./install_ollama.sh

set -e

echo "🦙 Installing Ollama..."

# Check if already installed
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is already installed"
    ollama --version
else
    # Install Ollama (macOS)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "📦 Installing Ollama for macOS..."
        brew install ollama
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "📦 Installing Ollama for Linux..."
        curl -fsSL https://ollama.ai/install.sh | sh
    else
        echo "❌ Unsupported OS: $OSTYPE"
        exit 1
    fi
fi

# Start Ollama service
echo "🚀 Starting Ollama service..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS: use launchctl
    launchctl start com.ollama.ollama 2>/dev/null || ollama serve &
else
    ollama serve &
fi

# Wait for service to start
echo "⏳ Waiting for Ollama to start..."
sleep 3

# Download embedding model
echo "📥 Downloading nomic-embed-text model (274MB)..."
ollama pull nomic-embed-text

echo "✅ Ollama installation complete!"
echo ""
echo "📋 Summary:"
echo "   - Ollama version: $(ollama --version)"
echo "   - Model: nomic-embed-text"
echo "   - Storage: ~/.ollama/models"
