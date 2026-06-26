#!/bin/bash
# Check and start Ollama service
# Usage: ./start_ollama.sh

echo "🔍 Checking Ollama status..."

# Check if installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed!"
    echo "   Run: ./scripts/install_ollama.sh"
    exit 1
fi

echo "✅ Ollama is installed: $(ollama --version)"

# Check if running
if curl -s http://localhost:11434/api/tags &> /dev/null; then
    echo "✅ Ollama service is running"
else
    echo "🔄 Starting Ollama service..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # Try launchctl first
        launchctl start com.ollama.ollama 2>/dev/null || ollama serve &
    else
        ollama serve &
    fi
    
    # Wait for service to start
    echo "⏳ Waiting for service..."
    sleep 3
    
    if curl -s http://localhost:11434/api/tags &> /dev/null; then
        echo "✅ Ollama service started successfully"
    else
        echo "❌ Failed to start Ollama service"
        exit 1
    fi
fi

# Check models
echo ""
echo "📦 Installed models:"
ollama list

# Check if nomic-embed-text is installed
if ollama list | grep -q "nomic-embed-text"; then
    echo ""
    echo "✅ nomic-embed-text is ready!"
else
    echo ""
    echo "⚠️ nomic-embed-text is not installed"
    echo "   Run: ./scripts/download_accelerator.sh"
fi
