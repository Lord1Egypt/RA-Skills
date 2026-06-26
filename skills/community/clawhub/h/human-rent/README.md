# Human-Rent - Human-as-a-Service for AI Agents

**Enable AI agents to interact with the physical world through verified human workers**

[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](https://github.com/ZhenRobotics/openclaw-human-rent)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![ClawHub](https://img.shields.io/badge/clawhub-human--rent-purple.svg)](https://clawhub.ai/zhenstaff/human-rent)

## What is Human-Rent?

Human-Rent is the world's first "Human-as-a-Service" platform designed specifically for AI agents. It enables AI to dispatch real human workers to perform physical world tasks that cannot be accomplished digitally:

- Take photos and videos
- Verify physical addresses
- Inspect equipment and facilities
- Make phone calls
- Scan documents
- Check product availability

## Features

- **Self-Contained**: No external dependencies after installation
- **User Confirmation**: Explicit consent required before dispatching humans
- **Secure**: HMAC-SHA256 authentication, integrity verification
- **Async-First**: Non-blocking task execution
- **Type-Safe**: Full TypeScript support
- **CLI-Friendly**: Easy command-line interface
- **Production-Ready**: Real API integration with ZhenRent platform

## Installation

```bash
clawhub install human-rent
```

## Quick Start

### 1. Get API Credentials

Visit https://www.zhenrent.com/api/keys to get your credentials.

### 2. Configure Environment

```bash
export ZHENRENT_API_KEY="your-api-key-here"
export ZHENRENT_API_SECRET="your-api-secret-here"
```

### 3. Test Connection

```bash
human-rent test
```

### 4. Dispatch Your First Task

```bash
human-rent dispatch "Take a photo of the Golden Gate Bridge" \
  --location="37.8199,-122.4783"
```

You'll be prompted to confirm before the task is dispatched.

### 5. Check Task Status

```bash
human-rent status <task_id>
```

## Usage Examples

### Example 1: Address Verification

```bash
human-rent dispatch "Verify the address 123 Main St exists and take a photo of the entrance" \
  --location="37.7749,-122.4194" \
  --budget="$20"
```

### Example 2: Equipment Inspection

```bash
human-rent dispatch "Inspect the HVAC system on the roof and report its condition" \
  --location="40.7128,-74.0060" \
  --budget="$40" \
  --timeout=60
```

### Example 3: Phone Verification

```bash
human-rent dispatch "Call (555) 123-4567 and confirm the business hours" \
  --budget="$15" \
  --type="voice_verification"
```

## Command Reference

```bash
# Dispatch a task
human-rent dispatch <instruction> [options]

# Check task status
human-rent status <task_id> [--wait]

# List available workers
human-rent humans [--location=<lat,lng>] [--radius=<meters>]

# Test API connection
human-rent test

# Show help
human-rent help
```

## Dispatch Options

- `--location=<lat,lng>` - Location coordinates (e.g., "37.7749,-122.4194")
- `--budget=<amount>` - Budget in dollars (e.g., "$20" or "$15-25")
- `--priority=<level>` - Priority: low, normal, high, urgent
- `--timeout=<minutes>` - Task timeout in minutes (default: 30)
- `--type=<task_type>` - Task type (auto-detected if not specified)

## Task Types

| Type | Description | Typical Cost | Typical Time |
|------|-------------|--------------|--------------|
| `photo_verification` | Take photos | $10-20 | 5-15 min |
| `address_verification` | Verify address | $15-25 | 10-20 min |
| `document_scan` | Scan documents | $15-25 | 10-20 min |
| `visual_inspection` | Detailed inspection | $20-40 | 15-30 min |
| `voice_verification` | Phone calls | $10-20 | 5-10 min |
| `purchase_verification` | Check availability | $20-40 | 15-30 min |

## Security Features

### User Confirmation Required

Every task dispatch requires explicit user confirmation. You'll see:

```
========================================
DISPATCH CONFIRMATION REQUIRED
========================================

Task Details:
  Description: Take a photo of 123 Main St
  Location: 37.7749,-122.4194
  Estimated Cost: $15-20
  Estimated Time: 15 minutes

This will dispatch a real human worker to perform a physical task.
You will be charged for this service.

Dispatch human worker? [y/N]:
```

### Integrity Verification

All files are verified on startup to ensure no tampering:

```javascript
// Checksums verified automatically
✓ Integrity check passed
```

### Secure Authentication

All API requests use HMAC-SHA256 signing:

```
message = method + path + timestamp + body
signature = HMAC-SHA256(message, api_secret)
```

## Environment Variables

### Required

- `ZHENRENT_API_KEY` - Your API key from https://www.zhenrent.com/api/keys
- `ZHENRENT_API_SECRET` - Your API secret (keep this secure!)

### Optional

- `ZHENRENT_BASE_URL` - API base URL (default: https://www.zhenrent.com/api/v1)
- `HUMAN_RENT_AUTO_CONFIRM` - Set to 'true' to skip confirmation prompts (use with caution)

## Architecture

### Self-Contained Design

Unlike v0.1.0 which required cloning a GitHub repository, v0.2.0 is completely self-contained:

```
human-rent-v0.2.0/
├── bin/
│   ├── human-rent          # Self-contained CLI
│   └── checksums.txt       # Integrity verification
├── lib/
│   ├── api-client.js       # ZhenRent API client
│   ├── dispatch.js         # Task dispatch logic
│   ├── status.js           # Status checking
│   ├── humans.js           # Worker management
│   └── confirmation.js     # User confirmation prompts
├── _meta.json              # Credential declarations
├── SKILL.md                # OpenClaw skill documentation
└── package.json            # Package metadata
```

No external dependencies. No git clone required. Just install and run.

### Async-First Architecture

Human tasks are inherently asynchronous:

1. **Dispatch** - Create task and assign to worker (< 1 second)
2. **Execution** - Human performs task (5-60 minutes)
3. **Verification** - Results are verified (automatic or manual)
4. **Retrieval** - Agent retrieves results

Your agent can continue working while humans execute tasks.

## API Integration

### ZhenRent Platform

Human-Rent integrates with the ZhenRent platform:

- **Backend**: https://www.zhenrent.com/api/v1
- **Worker Portal**: https://www.zhenrent.com/worker/hall
- **Business Model**: AI agents post tasks → Human workers complete → Agents verify results

### REST API Endpoints

```
POST   /tasks/              Create new task
GET    /tasks/{id}          Get task status
GET    /workers/            List available workers
POST   /tasks/{id}/cancel   Cancel task
```

## Pricing

### Per-Task Pricing

- Quick verification: $10-20
- Standard tasks: $15-25
- Detailed inspection: $20-40
- Expert consultation: $50-100+

### Platform Fee

20% platform fee on all transactions (already included in task quotes)

### Subscription (Coming Soon)

- Free: 5 tasks/month
- Pro: $99/month, unlimited tasks
- Enterprise: Custom pricing

## Troubleshooting

### "Missing credentials"

Set your environment variables:

```bash
export ZHENRENT_API_KEY="your-key"
export ZHENRENT_API_SECRET="your-secret"
```

Get credentials at: https://www.zhenrent.com/api/keys

### "No suitable humans found"

- Try increasing search radius: `--radius=10000`
- Try increasing budget: `--budget="$30"`
- Check if location is in a supported area
- Try different time of day (more workers during business hours)

### "Task timed out"

- Increase timeout: `--timeout=60`
- Check if task is reasonable and achievable
- Verify location is accessible
- Consider increasing budget for complex tasks

### "Cannot prompt for confirmation in non-interactive mode"

If running in a script or automated environment:

```bash
export HUMAN_RENT_AUTO_CONFIRM=true
```

Note: Use with caution. This bypasses the safety confirmation.

## Development

### Running Tests

```bash
npm test
# or
human-rent test
```

### Building from Source

```bash
git clone https://github.com/ZhenRobotics/openclaw-human-rent.git
cd openclaw-human-rent
npm install
```

### Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Roadmap

### v0.3.0 (Next Release)

- [ ] Real-time progress updates via websockets
- [ ] Multi-language support
- [ ] Photo quality verification
- [ ] Worker rating system

### v1.0.0 (Future)

- [ ] Expert-on-call marketplace
- [ ] Multi-city support (NY, LA, SF, Chicago, Boston)
- [ ] Video streaming from workers
- [ ] AR glasses integration

## Support

- **Documentation**: https://github.com/ZhenRobotics/openclaw-human-rent
- **Issues**: https://github.com/ZhenRobotics/openclaw-human-rent/issues
- **Email**: support@zhenrent.com
- **Discord**: https://discord.gg/zhenrent

## License

MIT License - see [LICENSE](LICENSE) for details

## Credits

Built by [@ZhenStaff](https://github.com/ZhenRobotics) for the OpenClaw ecosystem.

Powered by [ZhenRent Platform](https://www.zhenrent.com) - "Agent local + Human cloud"

## Links

- **ClawHub**: https://clawhub.ai/zhenstaff/human-rent
- **GitHub**: https://github.com/ZhenRobotics/openclaw-human-rent
- **ZhenRent**: https://www.zhenrent.com
- **API Docs**: https://www.zhenrent.com/api/docs

---

Make AI agents that can touch the physical world.
