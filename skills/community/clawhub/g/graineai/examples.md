# NoddyAI API — Request Body Examples

---

## Create Voice Agent (full)

```json
{
  "agent_name": "Sales Agent",
  "agent_welcome_message": "Hello! How can I help you today?",
  "agent_type": "other",
  "org_id": "<ORG_ID>",
  "webhook_url": "https://your-server.com/webhook",
  "tasks": [
    {
      "task_type": "conversation",
      "toolchain": {
        "execution": "parallel",
        "pipelines": [["transcriber", "llm", "synthesizer"]]
      },
      "tools_config": {
        "transcriber": {
          "provider": "deepgram",
          "model": "nova-2",
          "language": "en",
          "stream": true
        },
        "llm_agent": {
          "provider": "openai",
          "model": "gpt-4o-mini",
          "max_tokens": 150,
          "temperature": 0.2,
          "agent_flow_type": "streaming",
          "use_fallback": true
        },
        "synthesizer": {
          "provider": "elevenlabs",
          "voice_id": "EXAVITQu4vr4xnSDxMaL",
          "model": "eleven_turbo_v2_5",
          "stream": true,
          "buffer_size": 40
        },
        "input":  { "provider": "default", "format": "pcm" },
        "output": { "provider": "default", "format": "pcm" }
      },
      "task_config": {
        "agent_memory": false,
        "voicemail": true,
        "hangup_after_silence": 15,
        "call_terminate": 120,
        "incremental_delay": 100
      }
    }
  ],
  "agent_prompts": {
    "task_1": {
      "system_prompt": "You are a helpful sales agent. Customer name: {{customer_name}}."
    }
  }
}
```

---

## Update Agent — Change Synthesizer Voice

```json
{
  "tasks": [{
    "task_type": "conversation",
    "tools_config": {
      "synthesizer": {
        "provider": "elevenlabs",
        "voice_id": "<NEW_VOICE_ID>",
        "model": "eleven_turbo_v2_5",
        "stream": true
      }
    }
  }]
}
```

## Update Agent — Cartesia Synthesizer (Hindi)

```json
{
  "tasks": [{
    "task_type": "conversation",
    "tools_config": {
      "synthesizer": {
        "provider": "cartesia",
        "voice_id": "a0e99841-438c-4a64-b679-ae501e7d6091",
        "model": "sonic-2",
        "stream": true,
        "language": "hi",
        "audio_format": "pcm_8000"
      }
    }
  }]
}
```

## Update Agent — Deepgram Transcriber (Hindi)

```json
{
  "tasks": [{
    "task_type": "conversation",
    "tools_config": {
      "transcriber": {
        "provider": "deepgram",
        "model": "nova-2",
        "language": "hi",
        "stream": true,
        "endpointing": 200
      }
    }
  }]
}
```

## Update Agent — Azure OpenAI LLM

```json
{
  "tasks": [{
    "task_type": "conversation",
    "tools_config": {
      "llm_agent": {
        "provider": "azure",
        "model": "azure/gpt-4.1-mini",
        "max_tokens": 200,
        "temperature": 0.1,
        "agent_flow_type": "streaming"
      }
    }
  }]
}
```

## Update Agent — System Prompt

```json
{
  "agent_prompts": {
    "task_1": {
      "system_prompt": "You are a polite insurance advisor. Customer: {{customer_name}}. Policy: {{policy_number}}."
    }
  }
}
```

## Add API Tools (Skills) to Agent

```json
{
  "tasks": [{
    "task_type": "conversation",
    "tools_config": {
      "api_tools": {
        "tools": [
          {
            "name": "check_availability",
            "description": "Check appointment availability for a given date",
            "parameters": {
              "type": "object",
              "properties": {
                "date": { "type": "string", "description": "Date in YYYY-MM-DD format" },
                "slot": { "type": "string", "description": "Preferred time slot (morning/afternoon/evening)" }
              },
              "required": ["date"]
            },
            "url": "https://your-api.com/availability",
            "method": "GET",
            "param_in_query": true,
            "timeout": 5
          },
          {
            "name": "book_appointment",
            "description": "Book an appointment for the customer",
            "parameters": {
              "type": "object",
              "properties": {
                "customer_name": { "type": "string" },
                "phone": { "type": "string" },
                "date": { "type": "string" },
                "slot": { "type": "string" }
              },
              "required": ["customer_name", "phone", "date", "slot"]
            },
            "url": "https://your-api.com/appointments",
            "method": "POST",
            "param_in_body": true
          }
        ]
      }
    }
  }]
}
```

---

## Outbound Call — Auto provider

```json
{
  "recipient": "+911234567890",
  "agent_id": "<AGENT_ID>",
  "org_id": "<ORG_ID>",
  "webhook_url": "https://your-server.com/webhook",
  "metadata": {
    "customer_name": "Rahul Sharma",
    "policy_number": "POL-12345",
    "call_reason": "Policy renewal"
  }
}
```

## Outbound Call — Jambonz

```json
{
  "recipient": "+911234567890",
  "agent_id": "<AGENT_ID>",
  "org_id": "<ORG_ID>",
  "provider": "jambonz",
  "from_number": "+10987654321",
  "record": true,
  "timeout": 30,
  "webhook_url": "https://your-server.com/webhook",
  "metadata": {
    "customer_name": "Priya Patel",
    "account_id": "ACC-789"
  }
}
```

## Outbound Call — Exotel

```json
{
  "recipient": "+911234567890",
  "agent_id": "<AGENT_ID>",
  "org_id": "<ORG_ID>",
  "provider": "exotel",
  "from_number": "0XXXXXXXXXX",
  "webhook_url": "https://your-server.com/webhook",
  "metadata": {
    "customer_name": "Amit Singh"
  }
}
```

---

## Batch Call

```json
{
  "agent_id": "<AGENT_ID>",
  "org_id": "<ORG_ID>",
  "contacts": [
    { "phone": "+911234567890", "name": "Rahul Sharma", "policy_no": "POL-001" },
    { "phone": "+919876543210", "name": "Priya Patel",  "policy_no": "POL-002" }
  ],
  "scheduled_time": "2026-03-10T09:00:00Z",
  "max_retries": 2,
  "provider": "jambonz"
}
```
