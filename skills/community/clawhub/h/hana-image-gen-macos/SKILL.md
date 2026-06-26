---
name: hana-image-gen
description: MacOS Gemini image gen via OpenRouter for OpenClaw agents. Auto-wait, gen, send image.
---

# Hana Image Gen Pro (MacOS)

## Agent Workflow
1. message action=send text="⏳ Generating image for: \$prompt"
2. cd scripts && OPENROUTER_API_KEY=\$OPENROUTER_API_KEY python3 gen.py "\$prompt"
3. IMAGE=\$(cat ../output.json | jq -r .paths[0])
4. message action=send media=\$IMAGE caption="Generated: \$prompt 😏"
NO_REPLY.

## Required Env
OPENROUTER_API_KEY, TELEGRAM_BOT_TOKEN (global .env)
