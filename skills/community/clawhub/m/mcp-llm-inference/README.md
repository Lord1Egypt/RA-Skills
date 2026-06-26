# @blue-trianon/mcp-llm-inference

MCP tool for LLM inference — chat completions, text generation, and model discovery via the L402 API.

## Features

- Chat completions with multi-turn message history
- Single-prompt text generation
- List available models
- Optional streaming support
- Configurable base URL via environment variable
- Powered by L402 micropayments

## MCP Server Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "llm-inference": {
      "command": "npx",
      "args": ["-y", "@blue-trianon/mcp-llm-inference"],
      "env": {
        "NAUTDEV_BASE_URL": "https://api.nautdev.com"
      }
    }
  }
}
```

Or if installed globally:

```json
{
  "mcpServers": {
    "llm-inference": {
      "command": "mcp-llm-inference"
    }
  }
}
```

## Tools

### chat

Send a chat completion request to an LLM.

| Parameter | Type    | Required | Description                                    |
|-----------|---------|----------|------------------------------------------------|
| model     | string  | yes      | Model identifier (e.g. llama3, mistral, gemma) |
| messages  | array   | yes      | Array of {role, content} message objects        |
| stream    | boolean | no       | Stream the response (default: false)           |

### generate

Generate text from a single prompt.

| Parameter | Type    | Required | Description                                    |
|-----------|---------|----------|------------------------------------------------|
| model     | string  | yes      | Model identifier (e.g. llama3, mistral, gemma) |
| prompt    | string  | yes      | Text prompt for generation                     |
| stream    | boolean | no       | Stream the response (default: false)           |

### models

List all available LLM models.

No parameters required.

## Pricing

Requests are metered via L402 micropayments. See [Blue-Trianon-Ventures](https://github.com/Blue-Trianon-Ventures) for pricing details.

## License

MIT
