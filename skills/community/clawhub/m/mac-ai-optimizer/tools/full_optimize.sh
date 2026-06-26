#!/bin/bash
# full_optimize.sh - Run all optimizations in sequence
# One command to turn a Mac into an AI server node

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "########################################"
echo "#                                      #"
echo "#     Mac AI Optimizer - Full Run      #"
echo "#                                      #"
echo "########################################"
echo ""
echo "This will optimize your Mac for AI workloads"
echo "(OpenClaw, Docker, Ollama, Agent tasks)"
echo ""

# Step 1: System Report
echo ""
echo "======== Step 1/5: System Report ========"
bash "$SCRIPT_DIR/system_report.sh"

# Step 2: Memory Optimization
echo ""
echo "======== Step 2/5: Memory Optimization ========"
bash "$SCRIPT_DIR/optimize_memory.sh"

# Step 3: UI Optimization
echo ""
echo "======== Step 3/5: UI Optimization ========"
bash "$SCRIPT_DIR/reduce_ui.sh"

# Step 4: Docker Optimization
echo ""
echo "======== Step 4/5: Docker Optimization ========"
bash "$SCRIPT_DIR/docker_optimize.sh"

# Step 5: SSH Setup
echo ""
echo "======== Step 5/5: SSH Setup ========"
bash "$SCRIPT_DIR/enable_ssh.sh"

# Final Report
echo ""
echo "########################################"
echo "#                                      #"
echo "#     Optimization Complete!           #"
echo "#                                      #"
echo "########################################"
echo ""
echo "Summary of changes:"
echo "  [x] Background services reduced"
echo "  [x] UI overhead minimized"
echo "  [x] Docker resource limits configured"
echo "  [x] SSH remote access enabled"
echo ""
echo "Expected results:"
echo "  - macOS idle memory: ~2.5GB (from ~6GB)"
echo "  - Available for AI: ~5.5GB on 8GB Mac"
echo "  - Reduced CPU background load: ~30%"
echo ""
echo "Your Mac is now optimized as an AI server node."
echo ""
echo "Next steps:"
echo "  1. Run OpenClaw: docker compose up -d"
echo "  2. Run Ollama:   ollama serve"
echo "  3. Remote access: ssh $(whoami)@$(hostname)"
echo ""
echo "To monitor: run system_report.sh periodically"
