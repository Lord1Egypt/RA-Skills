# Stateless Client-Supplied Credentials Architecture (Zero-Storage Security)

## Overview
When orchestrating AI advertising campaigns (OpenAI Ads, Meta Ads, Google Ads, PAPI WhatsApp), the Habilis MCP Gateway enforces a strict **Zero-Knowledge / Zero-Storage** architecture:

1. **Habilis Platform Token (`HABILIS_TOKEN`)**:
   - Passed in the HTTP `Authorization: Bearer <hab_live_...>` header.
   - Validates subscription tier, quotas, rate limits, and unlocks proprietary AI optimization engines, creative generation, and format transformers.

2. **Target Provider API Keys & Tokens (`OPENAI_ADS_API_KEY`, `META_ACCESS_TOKEN`, etc.)**:
   - **MUST be held locally by the client/agent** (in `.env`, local Hermes environment, Claude Desktop config, or Cursor environment).
   - Passed on demand as arguments in tool invocations (e.g. `openai_api_key: "sk-..."`, `meta_access_token: "EAAB..."`).
   - **NEVER persisted or stored** in Habilis databases. Calls are executed statelessly and ephemerally.

## Benefits
- **Zero Liability**: If the central gateway or database is audited or compromised, no customer third-party API keys exist on the server.
- **Client Key Rotation**: The client can rotate, revoke, or cycle OpenAI / Meta keys locally with zero disruption or sync requirement on the backend.
- **Compliance**: Fully aligns with SOC 2 Type II, GDPR, and LGPD data minimization guidelines.
