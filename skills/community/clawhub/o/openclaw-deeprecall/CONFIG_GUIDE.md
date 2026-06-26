# DeepRecall Configuration Guide

## Configuration Options

### config.json Structure
```json
{
  "deeprecall": {
    "summarizer": {
      "preferred_provider": "deepseek-reasoner",
      "preferred_model": "deepseek-reasoner",
      "max_content_length": 6000,
      "temperature": 0.1,
      "max_tokens": 4000,
      "timeout_seconds": 180,
      "store_raw_content": true,
      "auto_summarize_cron": "0 2 * * *"
    }
  }
}
```

### Parameter Descriptions

#### `preferred_provider`
**Type**: String or null  
**Default**: null (auto-select)  
**Description**: Provider name from OpenClaw configuration (e.g., "deepseek-reasoner", "qwen").  
**Behavior**: 
- If specified and available: uses this provider
- If not specified: auto-selects first available provider with baseUrl and apiKey
- If not available: uses rule-based extraction fallback

#### `preferred_model`
**Type**: String or null  
**Default**: null (auto-select)  
**Description**: Model ID from the provider's models list.  
**Behavior**:
- If specified and found in provider's model list: uses this model
- If not specified: uses first available model from selected provider

#### `max_content_length`
**Type**: Integer  
**Default**: 6000  
**Description**: Maximum content length to send to LLM (characters). Longer content will be truncated.

#### `temperature`
**Type**: Float (0.0-1.0)  
**Default**: 0.1  
**Description**: LLM temperature, lower = more deterministic responses.

#### `max_tokens`
**Type**: Integer  
**Default**: 4000  
**Description**: Maximum tokens in LLM response.

#### `timeout_seconds`
**Type**: Integer  
**Default**: 180  
**Description**: API timeout in seconds.

#### `store_raw_content`
**Type**: Boolean  
**Default**: true  
**Description**: Whether to store raw content to L2 archive for later reference.

#### `auto_summarize_cron`
**Type**: String  
**Default**: "0 2 * * *" (2 AM daily)  
**Description**: Cron expression for automatic summarization. This is for reference only; actual scheduling requires OpenClaw cron setup.

## Configuration File Search Order

DeepRecall looks for configuration in this order:

1. **Current directory**: `./config.json`
2. **Current directory**: `./deeprecall_config.json`
3. **Parent directory**: `../config.json` (OpenClaw workspace root)
4. **Home directory**: `~/.deeprecall.json`
5. **Default configuration** (if no custom config found)

## Example Configurations

### Using DeepSeek as Preferred Provider
```json
{
  "deeprecall": {
    "summarizer": {
      "preferred_provider": "deepseek-reasoner",
      "preferred_model": "deepseek-reasoner",
      "temperature": 0.1
    }
  }
}
```

### Using Local Qwen Provider
```json
{
  "deeprecall": {
    "summarizer": {
      "preferred_provider": "qwen",
      "preferred_model": "qwen/qwen3.5-9b",
      "temperature": 0.3
    }
  }
}
```

### Auto-Selection with Custom Parameters
```json
{
  "deeprecall": {
    "summarizer": {
      "preferred_provider": null,
      "max_content_length": 8000,
      "temperature": 0.2,
      "max_tokens": 3000
    }
  }
}
```

## Quick Start

1. **Copy example configuration**:
   ```bash
   cp config.example.json config.json
   ```

2. **Edit configuration**:
   ```bash
   nano config.json
   ```

3. **Test configuration**:
   ```bash
   python3 scripts/memory_db_tool.py summarize --test-config
   ```

## Integration with OpenClaw Configuration

DeepRecall automatically reads LLM provider configurations from OpenClaw's `openclaw.json`. Ensure your OpenClaw configuration includes at least one OpenAI-compatible provider with `baseUrl` and `apiKey`.

Example OpenClaw provider configuration:
```json
"models": {
  "providers": {
    "deepseek-reasoner": {
      "baseUrl": "https://api.deepseek.com/v1",
      "apiKey": "sk-...",
      "models": [{"id": "deepseek-reasoner"}]
    }
  }
}
```