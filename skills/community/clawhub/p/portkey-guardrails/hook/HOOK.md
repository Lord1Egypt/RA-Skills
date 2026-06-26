---
name: portkey-guardrails
description: "Applies Portkey-style guardrails to inbound/outbound OpenClaw messages and records audit events"
metadata:
  openclaw:
    emoji: "🛡️"
    events:
      - "message:received"
      - "message:preprocessed"
      - "message:sending"
      - "message:sent"
    requires:
      bins:
        - "node"
---

# Portkey Guardrails

This workspace hook connects the Portkey Gateway Integration implementation to the live OpenClaw gateway.

## What it does

- Runs pre-dispatch guardrails on inbound chat content before it reaches the agent loop
- Runs output guardrails on outbound messages when the gateway exposes a pre-send hook
- Writes guardrail audit entries through the shared implementation in `projects/portkey-gateway-integration/implementation`
- Preserves the existing OpenClaw gateway flow when no guardrail fires

## Notes

- Inbound enforcement is the primary live integration path.
- Output redaction is applied when the gateway exposes a cancellable send event; otherwise it is logged for audit only.
- This hook is intentionally conservative and should fail open if the Portkey module cannot be loaded.
