# Joplin Server API Skill for OpenClaw

An [OpenClaw](https://github.com/openclaw/openclaw) skill that enables AI-powered management of your Joplin notes via the Joplin Server REST API.

## About

This skill allows OpenClaw to interact with your self-hosted [Joplin Server](https://joplinapp.org/) to create, read, edit, search, and delete notes and notebooks.

### Credits

The JavaScript API client is a port of [joppy](https://github.com/marph91/joppy), the excellent Python library for Joplin's API by [@marph91](https://github.com/marph91).

### API Compatibility

This skill uses the **unofficial Joplin Server REST API** (undocumented). The API is reverse-engineered from the Joplin client behavior and may change without notice. It has been tested with Joplin Server 2.x and 3.x.

## Features

- Create, read, update, and delete notes
- Create and manage notebooks
- Search notes by title or content
- Automatic sync lock handling (prevents conflicts with other Joplin clients)
- Support for markdown notes and TODO items
- Works with self-hosted Joplin Server instances

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw)
- Node.js 16+
- A self-hosted Joplin Server instance

## Installation

1. Clone this repository to your OpenClaw skills directory:

```bash
git clone https://github.com/slavaboiko/joplin-api-openclaw-skill.git ~/.openclaw/skills/joplin
```

2. Configure credentials using one of the methods below.

## Configuration

### Option A: Config File

Create `~/.joplin-server-config`:

```bash
JOPLIN_SERVER_URL=https://your-joplin-server.com
JOPLIN_EMAIL=your-email@example.com
JOPLIN_PASSWORD=your-password
# Optional: skip TLS verification for self-signed certificates
# JOPLIN_SKIP_TLS_VERIFY=true
```

Secure the file:

```bash
chmod 600 ~/.joplin-server-config
```

### Option B: 1Password Integration

If you use [1Password](https://1password.com/) with OpenClaw, the skill can retrieve credentials automatically via the `op` CLI. Store your Joplin server credentials in 1Password, then the skill will prompt you for the vault/item path on first use.

Example 1Password references:
```
op://Private/Joplin Server/url
op://Private/Joplin Server/username
op://Private/Joplin Server/password
```

The skill will create the config file for you using:

```bash
JOPLIN_URL=$(op read "op://VAULT/ITEM/url")
JOPLIN_EMAIL=$(op read "op://VAULT/ITEM/username")
JOPLIN_PASS=$(op read "op://VAULT/ITEM/password")
```

## Usage

Once installed, invoke the skill:

```
/joplin
```

Then ask to manage your notes:

- "List all my notebooks"
- "Create a new note called 'Meeting Notes' in my Work notebook"
- "Search for notes about project planning"
- "Show me my TODO for today"
- "Add a task to my daily TODO"

## Available Commands

| Command | Description |
|---------|-------------|
| `ping` | Health check (no auth required) |
| `login` | Authenticate and verify connection |
| `list-notebooks` | List all notebooks |
| `list-notes` | List all notes |
| `get-note <id>` | Get note content |
| `add-notebook <title>` | Create a new notebook |
| `add-note <title> [parent_id] [body]` | Create a new note |
| `modify-note <id> <field> <value>` | Modify a note field |
| `delete-note <id>` | Delete a note |
| `search <query>` | Search notes by title/content |

## How It Works

The skill bundles a standalone JavaScript API client (`scripts/joplin-server-api.js`) that communicates directly with your Joplin Server using its REST API. All operations are performed through JSON requests, and the client handles:

- Authentication and session management
- Joplin's item serialization format
- Sync lock protocol (acquire/release locks for write operations)

## Security

- Credentials are stored locally in `~/.joplin-server-config` (with `chmod 600` permissions)
- With 1Password integration, secrets are fetched from 1Password and written to the config file
- TLS certificate validation is enabled by default; set `JOPLIN_SKIP_TLS_VERIFY=true` only for self-signed certificates
- All communication with your Joplin Server uses HTTPS
- No data is sent to third parties

## Troubleshooting

**Connection refused**: Verify your `JOPLIN_SERVER_URL` is correct and the server is running.

**Authentication failed**: Check your email and password in the config file.

**Sync target has exclusive lock**: Another Joplin client is currently syncing. Wait a moment and try again.

## License

MIT

## Related Projects

- [Joplin](https://joplinapp.org/) - The open source note-taking app
- [Joplin Server](https://github.com/laurent22/joplin/tree/dev/packages/server) - Self-hosted sync server
- [joppy](https://github.com/marph91/joppy) - Python library for Joplin API (original inspiration)
- [OpenClaw](https://github.com/openclaw/openclaw) - AI assistant framework
- [ClawHub](https://clawhub.com/) - OpenClaw skills registry
