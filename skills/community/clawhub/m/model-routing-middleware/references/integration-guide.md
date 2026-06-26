# Model Routing — Integration Guide

## Integration Approaches

### Phase 1: Standalone Module (Simplest)

The router works as an importable Python package. No changes to your existing stack needed.

```python
# Add to your Python path
import sys
sys.path.insert(0, "/path/to/model-routing/scripts")

from router import route_request, check_escalation, check_context_status

# Route a prompt
route = route_request("Write a Python function to sort a list")
print(f"Model: {route.model}, Think: {route.think}, Task: {route.task_type}")

# Check escalation
result = check_escalation("I'm not sure about that answer", "fast-local")
if result.should_escalate:
    print(f"Escalating to: {result.next_model_key}")

# Check context
status = check_context_status(messages, context_limit=131072)
print(f"Action: {status.action}, Usage: {status.usage_percent:.1%}")
```

### Phase 2: Gateway Middleware

Use the router as middleware between your API gateway and model providers:

```python
from router import ModelRouter

router = ModelRouter(config_path="/path/to/config.yaml")

def handle_request(prompt, context_messages=None):
    # Route the prompt
    route = router.route_request(prompt, context_messages=context_messages)
    
    # Use route.model to select the model provider
    # Use route.think to enable/disable reasoning mode
    
    # After getting response, check for escalation
    # ...
```

### Phase 3: OpenClaw Plugin

For OpenClaw integration, add models to your configuration:

```json
{
  "models": {
    "providers": {
      "ollama": {
        "api": "ollama",
        "baseUrl": "http://127.0.0.1:11434",
        "models": [
          {"id": "YOUR_CODE_MODEL:latest", "contextWindow": 131072, "reasoning": true},
          {"id": "YOUR_FAST_MODEL:latest", "contextWindow": 131072, "reasoning": false}
        ]
      }
    }
  }
}
```

## Configuration

The router reads from `config.yaml` in the same directory. Key sections:

1. **models** — Define all available models with metadata
2. **routing** — Map task types to models and think modes
3. **context** — Set thresholds for compaction and large-context override
4. **escalation** — Configure confidence detection and retry chain
5. **logging** — Enable routing decision logs

## Testing

Run the test suite:

```bash
cd /path/to/model-routing/scripts
python -m pytest tests/ -v
```

Expected: All tests passing (83 tests covering classification, routing, and escalation).