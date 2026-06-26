#!/bin/bash

# ========================================
#   OpenClaw Direct Setup (Linux/Mac)
# ========================================

set -e

echo "========================================"
echo "  OpenClaw Direct Setup"
echo "========================================"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "[ERROR] Running as root detected!"
    echo ""
    echo "DO NOT run this script as root/sudo."
    echo "OpenClaw should run under your standard user account for security."
    echo ""
    echo "Please close this window and run normally."
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Check Node.js
echo "[1/6] Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js not found. Install from https://nodejs.org"
    read -p "Press Enter to exit..."
    exit 1
fi
echo "OK: $(node --version)"

# Check npm
echo ""
echo "[2/6] Checking npm..."
if ! command -v npm &> /dev/null; then
    echo "ERROR: npm not found"
    read -p "Press Enter to exit..."
    exit 1
fi
echo "OK: $(npm --version)"

# Check Ollama
echo ""
echo "[3/6] Checking Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "Ollama not found. Installing..."
    if command -v curl &> /dev/null; then
        curl -fsSL https://ollama.com/install.sh | sh
    else
        echo "ERROR: curl not found. Install Ollama manually from https://ollama.com"
        read -p "Press Enter to exit..."
        exit 1
    fi
fi
echo "OK: Ollama found"

# Check VRAM
echo ""
echo "[4/6] Checking VRAM..."
if command -v nvidia-smi &> /dev/null; then
    VRAM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1)
    echo "GPU Memory: ${VRAM} MB"
    if [ "$VRAM" -lt 12000 ]; then
        echo "WARNING: Less than 12GB VRAM detected"
        echo "For local models, you need at least 12GB VRAM"
        echo "Cloud LLMs will work, but local inference may be slow"
    fi
    echo "OK"
elif command -v rocm-smi &> /dev/null; then
    VRAM=$(rocm-smi --showmeminfo V | grep -oP '\d+' | head -1)
    echo "GPU Memory: ${VRAM} MB"
    if [ "$VRAM" -lt 12000 ]; then
        echo "WARNING: Less than 12GB VRAM detected"
    fi
    echo "OK"
else
    echo "INFO: Could not detect GPU VRAM (no nvidia-smi or rocm-smi)"
    echo "Assuming system has sufficient memory"
fi

# Configuration
echo ""
echo "[5/6] Configuration"
echo "-------------------------"
PORT="${PORT:-18789}"
LLM_URL="${LLM_URL:-http://localhost:11434/v1}"
MODEL="${MODEL:-ServiceNow-AI/Apriel-1.6-15b-Thinker:Q4_K_M}"

read -p "Port [$PORT]: " CUSTOM_PORT
[ -n "$CUSTOM_PORT" ] && PORT="$CUSTOM_PORT"

read -p "Ollama URL [$LLM_URL]: " CUSTOM_LLM
[ -n "$CUSTOM_LLM" ] && LLM_URL="$CUSTOM_LLM"

read -p "Model name [$MODEL]: " CUSTOM_MODEL
[ -n "$CUSTOM_MODEL" ] && MODEL="$CUSTOM_MODEL"

# Check/Install model
echo ""
echo "Checking Ollama model: $MODEL"
if ollama list | grep -q "$MODEL"; then
    echo "OK: Model already installed"
else
    echo "Model not found. Pulling from Ollama library..."
    ollama pull "$MODEL"
    echo "OK: Model installed"
fi

# Install OpenClaw
echo ""
echo "[6/6] Installing OpenClaw..."
npm install -g openclaw
echo "OK"

# Install ClawHub and skills
echo ""
echo "[7/7] Installing ClawHub and skills..."
npm install -g clawhub
clawhub install ningtoba/pc-assistant
clawhub install event-monitor
echo "OK"

# Create config
echo ""
echo "Creating config..."
export PORT LLM MODEL
node "$(dirname "$0")/create-config.js"
echo "OK"

# Optional: Configure firewall for additional security
echo ""
echo "========================================"
echo "  Security Hardening (Optional)"
echo "========================================"
echo ""
echo "Gateway is configured for localhost-only binding (127.0.0.1)"
echo "This means only your browser on this machine can access OpenClaw"
echo ""

read -p "Add firewall rule to block external access? (y/n, default: y): " -n 1 -r FIREWALL
echo ""
if [ -z "$FIREWALL" ] || [ "$FIREWALL" = "y" ] || [ "$FIREWALL" = "Y" ]; then
    # Detect OS and apply appropriate firewall rule
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux - try ufw first, then firewall-cmd
        if command -v ufw &> /dev/null; then
            sudo ufw deny from any to any port $PORT proto tcp 2>/dev/null && \
                echo "[OK] UFW rule added - external access blocked" || \
                echo "[WARNING] Could not create UFW rule (localhost binding still protects)"
        elif command -v firewall-cmd &> /dev/null; then
            sudo firewall-cmd --permanent --add-port=$PORT/tcp 2>/dev/null && \
                sudo firewall-cmd --reload && \
                echo "[OK] firewalld rule added" || \
                echo "[WARNING] Could not create firewalld rule"
        else
            echo "[INFO] No firewall tool detected (ufw/firewalld)"
            echo "Localhost binding still provides protection"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS - use pf or socketfilterfw
        if [ -f /usr/libexec/ApplicationFirewall/socketfilterfw ]; then
            echo "[INFO] macOS Application Firewall detected"
            echo "Manual configuration may be needed in System Preferences > Security > Firewall"
            echo "Localhost binding still provides protection"
        else
            echo "[INFO] Localhost binding provides protection"
        fi
    fi
else
    echo "[INFO] Skipping firewall configuration"
    echo "Localhost binding still protects from external access"
fi

# Start Ollama and OpenClaw
echo ""
echo "========================================"
echo "  DONE!"
echo "========================================"
echo "URL: http://localhost:$PORT"
echo ""

# Check if Ollama is already running
echo "Checking Ollama status..."
if curl -s --connect-timeout 2 http://localhost:11434/api/version > /dev/null 2>&1; then
    echo "[OK] Ollama is already running"
else
    # Check if port 11434 is in use
    if command -v lsof &> /dev/null; then
        if lsof -i :11434 > /dev/null 2>&1; then
            echo "[ERROR] Port 11434 is already in use by another process"
            echo "Please stop the process using port 11434"
            read -p "Press Enter to exit..."
            exit 1
        fi
    elif command -v netstat &> /dev/null; then
        if netstat -tuln | grep -q ":11434"; then
            echo "[ERROR] Port 11434 is already in use by another process"
            echo "Please stop the process using port 11434"
            read -p "Press Enter to exit..."
            exit 1
        fi
    fi
    
    echo "Starting Ollama..."
    ollama serve &
    sleep 5
fi

# Verify Ollama is responding
if curl -s --connect-timeout 5 http://localhost:11434/api/version > /dev/null 2>&1; then
    echo "[OK] Ollama is responding"
else
    echo "[WARNING] Ollama may not be fully ready yet"
fi

echo "Starting OpenClaw Gateway..."
openclaw gateway &

echo ""
echo "All set! OpenClaw is running"

# Open dashboard in browser
if command -v xdg-open &> /dev/null; then
    xdg-open "http://localhost:$PORT"
elif command -v open &> /dev/null; then
    open "http://localhost:$PORT"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    start "http://localhost:$PORT"
fi

echo "Opening OpenClaw dashboard..."

read -p "Press Enter to exit..."