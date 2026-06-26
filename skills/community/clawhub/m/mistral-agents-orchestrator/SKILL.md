---
name: mistral-agents-orchestrator
description: Multi-agent orchestration via Mistral's Agents API — register agents, manage conversations, delegate via handoffs, bind function calling tools. Use when building multi-agent systems with Mistral models, coordinating specialist agents, or implementing agent-to-agent delegation patterns. Requires MISTRAL_API_KEY.
version: 1.0.1
metadata:
  {
      "openclaw": {
            "emoji": "\ud83e\udd16",
            "requires": {
                  "bins": [],
                  "env": [
                        "MISTRAL_API_KEY"
                  ]
            },
            "primaryEnv": "MISTRAL_API_KEY",
            "network": {
                  "outbound": true,
                  "reason": "Calls Mistral Agents API (api.mistral.ai) for agent registration, conversations, and handoff delegation."
            },
            "security_notes": "base64 used for encoding message payloads in API requests — standard format. UploadFile is a FastAPI type used for document ingestion to agent tools. 'system prompt' refers to Mistral agent configuration field — a standard API parameter, not prompt injection."
      }
}
---

# Mistral Agents Orchestrator

Production-tested multi-agent orchestration using Mistral's Agents API. Implements the orchestrator-delegate pattern where a lead agent coordinates specialist agents via Conversations and Handoffs.

## Architecture

```
Orchestrator (Papa Bois pattern)
├── Registers specialist agents via Agents API
├── Creates conversations with handoff configuration
├── Delegates tasks by naming the target agent
└── Collects results from completed handoffs

Specialists (Anansi, Devi, Firefly patterns)
├── Receive delegated tasks with full conversation context
├── Execute their speciality (story gen, audio, code)
└── Return results to the orchestrator conversation
```

## Key Concepts

**Agents:** Pre-registered on Mistral platform with specific system prompts and model configs. Each agent has a unique ID (`ag_...`).

**Conversations:** Multi-turn threads that preserve context across handoffs. The child's name, language, and prompt all carry through without re-injection.

**Handoffs:** The orchestrator names a specialist agent; Mistral routes the conversation to that agent. Context is preserved automatically.

**Function Calling:** Tools (like TTS, SFX) are bound to the orchestrator agent, not the delegates. Tools follow the conversation context.

## Quick Start

```python
from mistralai import Mistral

client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

# Register agents (one-time setup)
orchestrator = client.beta.agents.create(
    model="mistral-large-latest",
    name="orchestrator",
    instructions="You coordinate specialist agents...",
)

specialist = client.beta.agents.create(
    model="mistral-large-latest",
    name="writer",
    instructions="You write content when delegated to...",
)

# Create conversation with handoff
response = client.beta.conversations.create(
    agent_id=orchestrator.id,
    inputs="Write a blog post about AI agents",
    handoffs=[{"agent_id": specialist.id, "name": "writer"}],
)
```

## Patterns Learned

- **Handoffs preserve conversation context** — no need to re-inject background info
- **Tools bind to the orchestrator**, not delegates — delegates can request tool calls but execution happens in the orchestrator's context
- **4 agents is the sweet spot for hackathon scope** — more agents = more API calls = more coordination overhead without proportional value
- **JSON mode on delegates** forces structured output reliably — without it, Mistral Large sometimes returns prose instead of scene arrays

## Files

- `scripts/orchestrator.py` — Full orchestrator implementation with agent registration, conversation management, and handoff delegation
- `references/agent-patterns.md` — Common multi-agent patterns and when to use each

## Security Notes

This skill uses patterns that may trigger automated security scanners:
- **base64**: Used for encoding audio/binary data in API responses (standard practice for media APIs)
- **UploadFile**: FastAPI's built-in file upload parameter for STT/voice isolation endpoints
- **"system prompt"**: Refers to configuring agent instructions, not prompt injection
