# @h-ear/openclaw

OpenClaw skill for [H-ear World](https://h-ear.world) audio classification. Sound intelligence in WhatsApp, Telegram, Slack, Discord, and Teams.

## Install

```bash
npm install @h-ear/openclaw
```

Or via ClawHub — search for `h-ear` or paste `https://github.com/Badajoz95/h-ear-openclaw`.

## Setup

Set `HEAR_API_KEY` to your H-ear Enterprise API key:

```bash
export HEAR_API_KEY=ncm_sk_your_key
```

## Commands

| Command | Description |
|---------|-------------|
| `classify <url>` | Classify audio from a URL |
| `classify batch <url1> <url2>...` | Batch classify multiple audio URLs |
| `sounds [search]` | List supported sound classes (521+) |
| `usage` | Show API usage statistics |
| `jobs [last N]` | List recent classification jobs |
| `job <id>` | Show detailed job results |
| `alerts on <sound>` | Register a simple sound alert via webhook |
| `alerts off <sound>` | Remove a sound alert |
| `webhook list` | List enterprise webhook registrations |
| `webhook detail <id>` | Webhook details with filter config |
| `webhook create <url>` | Create enterprise webhook (returns signing secret once) |
| `webhook ping <id>` | Test webhook connectivity |
| `webhook deliveries <id>` | Delivery audit trail |
| `health` | Check API status |

## Example

In any connected messaging channel:

```
> classify https://example.com/city-noise.mp3

**Audio Classification Complete**
Duration: 45.2s | 15 noise events detected

| Sound      | Confidence | Category |
|------------|-----------|----------|
| Car horn   | 94%       | Vehicle  |
| Speech     | 87%       | Human    |
| Dog bark   | 72%       | Animal   |
```

## Programmatic Use

```typescript
import { createSkill, classifyCommand } from '@h-ear/openclaw';

const { client } = createSkill();
const result = await classifyCommand(client, 'https://example.com/audio.mp3');
console.log(result);
```

## Supported Formats

MP3, WAV, FLAC, OGG, M4A

## Get an API Key

Visit [h-ear.world](https://h-ear.world) to create an account and generate an API key.

## License

MIT
