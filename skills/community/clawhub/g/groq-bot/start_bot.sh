#!/bin/bash

# Start Groq Bot als Sub-Agent
openclaw sessions_spawn \
  --task "Analysiere die NFT-Preise für Sorare, liste Karten auf, recherchiere Preise und baue ein Preis-Tracking ein." \
  --taskName "sorare-nft-analyzer" \
  --agentId groq-bot \
  --runtime subagent \
  --model qwen/qwen3-32b \
  --timeoutSeconds 300 \
  --cwd /home/silas/.openclaw/workspace/groq-bot

echo "Groq Bot gestartet! PID: $?"