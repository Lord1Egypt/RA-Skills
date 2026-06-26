---
name: hume-evi-langgraph
description: Integrate Hume EVI voice AI with LangGraph using interrupt/resume patterns. Use when building voice-based AI agents that need Twilio call handling, Hume EVI persona creation, transcript fetching with emotion extraction, and LangGraph state management across the call lifecycle. Covers dynamic Hume config creation, TwiML generation, webhook handling, chat_group event fetching, and emotion timeline extraction.
---

# Hume EVI + LangGraph Integration

## Architecture

Single LangGraph StateGraph with interrupt/resume:

```
receive_call → verify_pin → select_persona → create_hume_config → generate_twiml
    → await_call_end [INTERRUPT] → fetch_transcript → analyze → coach → store → END
```

The interrupt boundary separates pre-call (synchronous) from post-call (webhook-triggered).

## Critical Patterns

### 1. Interrupt/Resume for Async Calls

```python
from langgraph.types import interrupt, Command

def await_call_end(state):
    resume_data = interrupt({"reason": "waiting_for_webhook"})
    return {**state, "chat_id": resume_data["chat_id"]}

# In webhook handler:
graph.invoke(Command(resume={"chat_id": "xxx"}), config)
```

### 2. Hume Config Creation

Create dynamic EVI configs per call. Set temperature low (0.6) to prevent default enthusiasm:

```python
request_body = {
    "evi_version": "3",
    "name": f"Session-{persona_name}-{timestamp}",
    "prompt": {"text": voice_prompt},
    "voice": {"provider": "HUME_AI", "name": "KORA"},  # or "ITO" for male
    "language_model": {
        "model_provider": "OPEN_AI",
        "model_resource": "gpt-4o-mini",
        "temperature": 0.6,  # CRITICAL: default is too warm/eager
    },
    "event_messages": {"on_new_chat": {"enabled": True, "text": first_message}},
    "webhooks": [{"events": ["chat_ended"], "url": webhook_url}],
}
resp = httpx.post("https://api.hume.ai/v0/evi/configs", json=request_body, headers=headers)
```

### 3. TwiML Redirect (not Stream)

```python
twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Matthew">Connecting now.</Say>
    <Redirect>https://api.hume.ai/v0/evi/twilio?config_id={config_id}&amp;api_key={api_key}</Redirect>
</Response>'''
```

Use `&amp;` not `&` — this is inside XML.

### 4. Transcript Fetching (⚠️ Known Bug Zone)

Hume's `/chats/{id}/events` returns 404. Must use chat_groups:

```python
# Step 1: Get chat_group_id
chat_resp = httpx.get(f"https://api.hume.ai/v0/evi/chats/{chat_id}", headers=headers)
chat_group_id = chat_resp.json().get("chat_group_id")

# Step 2: Fetch events via chat_group
events_resp = httpx.get(
    f"https://api.hume.ai/v0/evi/chat_groups/{chat_group_id}/events",
    headers=headers, params={"page_size": 100}
)
events = events_resp.json().get("events_page", [])
```

Field names are **snake_case**: `message_text`, `emotion_features` (not `messageText`).

### 5. Emotion Extraction

```python
for msg in messages:
    ef = msg.get("emotion_features")  # dict of ~48 emotions with float scores
    if ef and msg.get("role") == "USER":  # USER = the human caller
        top = sorted(ef.items(), key=lambda x: x[1], reverse=True)[:5]
        emotion_timeline.append({"turn": n, "text": text, "top_emotions": dict(top)})
```

### 6. Webhook Session Resolution

Hume `chat_ended` webhook does NOT include `call_sid`. Use config_id mapping:

```python
config_to_thread: dict[str, str] = {}  # hume_config_id → langgraph_thread_id

# On config creation:
config_to_thread[config_id] = thread_id

# On webhook:
thread_id = config_to_thread.pop(body["config_id"])
```

## Prevention Rules

See `references/bug-prevention.md` for the full bug registry and prevention checklist.
