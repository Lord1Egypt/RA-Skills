#!/bin/bash
# Ollama Model Download Accelerator
# Solves slow download issue by auto-restarting every 60 seconds
# Usage: ./download_accelerator.sh [model_name]
# Example: ./download_accelerator.sh nomic-embed-text

MODEL_NAME="${1:-nomic-embed-text}"

echo "🚀 Ollama Download Accelerator"
echo "================================"
echo "Model: $MODEL_NAME"
echo ""
echo "💡 Tip: This script auto-restarts download every 60 seconds"
echo "       to prevent speed degradation during long downloads"
echo ""

# Check if model already exists
if ollama list | grep -q "$MODEL_NAME"; then
    echo "✅ Model '$MODEL_NAME' is already downloaded!"
    exit 0
fi

# Download loop
while true; do
    # Check if model exists now
    if ollama list | grep -q "$MODEL_NAME"; then
        echo ""
        echo "🎉 SUCCESS! Model '$MODEL_NAME' is ready!"
        exit 0
    fi
    
    echo "[$(date '+%H:%M:%S')] 📥 Downloading $MODEL_NAME..."
    
    # Start download in background
    ollama pull "$MODEL_NAME" &
    PID=$!
    
    # Wait 60 seconds then kill to force restart
    sleep 60
    
    # Check if still running
    if kill -0 $PID 2>/dev/null; then
        echo "[$(date '+%H:%M:%S')] 🔄 Killing and restarting (download was slow)..."
        kill $PID 2>/dev/null
        sleep 2
    else
        # Download finished
        wait $PID
        EXIT_CODE=$?
        
        if [ $EXIT_CODE -eq 0 ]; then
            echo ""
            echo "🎉 SUCCESS! Download completed!"
            exit 0
        else
            echo "[$(date '+%H:%M:%S')] ⚠️ Download interrupted, restarting..."
        fi
    fi
    
    echo ""
done
