# nano-gpt-plugin

NanoGPT provider plugin for OpenClaw

## Features

- Dynamic model catalog from `https://nano-gpt.com/api/v1/models?detailed=true`
- Auto-populates model capabilities (vision, reasoning, context window, pricing)
- Handles `NANOGPT_API_KEY` environment variable
- Provides `openclaw onboard --nano-gpt-api-key <key>` flow
- Fix usage tracking by adding include_usage: true to all outgoing requests.
- Subscription usage tracking via `/api/subscription/v1/usage`
- Balance checking via `/api/check-balance`
- Supports all NanoGPT model families: OpenAI, Anthropic, Google, xAI, DeepSeek, Moonshot, Qwen, Groq, and 50+ more

## Installation

### From npm (if published)

```bash
npm install @openclaw/nano-gpt
```

### Local development

Clone this repository and link it:

```bash
git clone <this-repo>
cd nano-gpt-plugin
npm install
npm run build
```

Then, in your OpenClaw workspace, you can use the plugin by referencing the built `dist` directory.

## Usage

### Onboarding

To add your NanoGPT API key:

```bash
openclaw onboard --nano-gpt-api-key <your-key>
```

This will store the key in your OpenClaw configuration.

### Using models

Once onboarded, you can use any model from NanoGPT by referencing it with the `nano-gpt/` prefix:

```bash
openclaw chat --model nano-gpt/openai/gpt-5.2 "Hello, world!"
```

Or in your agent configuration:

```json
{
  "model": "nano-gpt/anthropic/claude-opus-4.6"
}
```

### Usage and balance

To check your usage and balance:

```bash
openclaw status
```

This will show your daily/monthly token usage and remaining balance.

## Configuration

The plugin does not require any additional configuration beyond the API key.

## Development

### Building

```bash
npm run build
```

### Testing

```bash
npm test
```

### Linting

(If you add a linter)

```bash
npm run lint
```

## License

MIT
