---
credentials:
  - name: OPENHOOK_API_KEY
    description: API key from openhook.dev (Settings > API Keys). Starts with oh_live_ or oh_test_.
    required: true
    url: https://openhook.dev/settings
---

# openhook CLI

Use the openhook CLI to receive real-time events from external platforms and communicate with other agents through channels.

## When to use

- Receiving webhook events from GitHub, Stripe, Linear, Vercel, Slack
- Listening for external platform events in real-time
- Sending messages to other agents through channels
- Coordinating multi-agent workflows

## Installation

```bash
brew tap openhook-dev/openhook && brew install openhook
```

## Authentication

Requires an API key from openhook. The user must:
1. Sign up at https://openhook.dev/signup
2. Go to Settings > API Keys
3. Create a new API key (starts with `oh_live_` or `oh_test_`)

Then authenticate:

```bash
openhook auth login --key oh_live_xxxxxxxx

# Verify authentication worked
openhook whoami
```

## Receiving Events

### Subscribe to platform events

```bash
# GitHub
openhook subscribe github --repo owner/repo --events push,pull_request,issues

# Stripe
openhook subscribe stripe --events payment_intent.succeeded,customer.created

# Linear
openhook subscribe linear --events issue.created,issue.updated
```

### Listen for events

```bash
# Interactive output
openhook listen

# JSON output (for parsing)
openhook listen --json

# Pipe to your processing script
openhook listen --json | jq '.payload'
```

### Background daemon

```bash
openhook daemon start
openhook daemon status
openhook daemon logs -f
openhook daemon stop
```

## Channels (Agent-to-Agent Communication)

Channels let agents send messages to each other. Each agent subscribes to a channel with a unique name, then messages can be sent to specific agents or broadcast to all.

### Create a channel

```bash
openhook channel create <name> [--description "..."]

# Example
openhook channel create deploy-team --description "Deployment coordination"
```

### Subscribe to a channel

Each subscription needs:
- `--endpoint`: The HTTP endpoint ID that will receive messages
- `--name`: A unique alias for this agent in the channel

```bash
openhook channel subscribe <channel-id> --endpoint <endpoint-id> --name <alias>

# Example: Subscribe the "deployer" agent
openhook channel subscribe ch_abc123 --endpoint ep_xyz789 --name deployer
```

### List channel members

```bash
openhook channel members <channel-id>
openhook channel members <channel-id> --json
```

### Send messages

```bash
# Send to specific agent
openhook channel send <channel-id> "<message>" --to <agent-name>

# Broadcast to all agents
openhook channel send <channel-id> "<message>" --to all

# Include sender info
openhook channel send <channel-id> "<message>" --to <agent-name> --from <your-name>
```

### Channel workflow example

```bash
# 1. Create coordination channel
openhook channel create release-v2 --description "v2.0 release coordination"

# 2. Agents join with their endpoints
openhook channel subscribe ch_xxx --endpoint ep_builder --name builder
openhook channel subscribe ch_xxx --endpoint ep_tester --name tester
openhook channel subscribe ch_xxx --endpoint ep_deployer --name deployer

# 3. Coordinate the release
openhook channel send ch_xxx "build v2.0.0" --to builder --from coordinator
openhook channel send ch_xxx "run integration tests" --to tester --from builder
openhook channel send ch_xxx "deploy to staging" --to deployer --from tester
openhook channel send ch_xxx "v2.0.0 deployed successfully" --to all --from deployer
```

## Managing subscriptions

```bash
# List all subscriptions
openhook list

# View event history
openhook events

# Remove subscription
openhook unsubscribe <subscription-id>
```

## Common patterns

### Wait for specific event

```bash
# Listen until you get the event you need
openhook listen --json | while read -r event; do
  type=$(echo "$event" | jq -r '.event_type')
  if [ "$type" = "push" ]; then
    echo "$event" | jq '.payload'
    break
  fi
done
```

### React to GitHub push

```bash
openhook subscribe github --repo myorg/myrepo --events push
openhook listen --json | jq -c 'select(.event_type == "push") | .payload.commits'
```

## Reference

| Command | Description |
|---------|-------------|
| `openhook whoami` | Show authenticated user |
| `openhook subscribe <platform>` | Subscribe to platform events |
| `openhook list` | List subscriptions |
| `openhook unsubscribe <id>` | Remove subscription |
| `openhook listen [--json]` | Listen for events |
| `openhook events` | View event history |
| `openhook channel create <name>` | Create channel |
| `openhook channel list` | List channels |
| `openhook channel subscribe <ch> --endpoint <ep> --name <alias>` | Join channel |
| `openhook channel members <ch>` | List members |
| `openhook channel send <ch> <msg> --to <name\|all>` | Send message |

## Links

- Website: https://openhook.dev
- Dashboard: https://openhook.dev/dashboard
- GitHub: https://github.com/openhook-dev/openhook-cli
