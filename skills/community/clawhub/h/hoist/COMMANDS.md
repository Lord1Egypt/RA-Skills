# Hoist CLI - Full Command Reference

Hoist is AI-native. All commands output structured JSON and skip interactive prompts automatically when called from an agent (non-TTY). No flags needed.

## Init

```bash
hoist init                                # Auto-detects HOIST_*_API_KEY env vars, falls back to interactive
```

If any of these env vars are set, init auto-configures the provider (no prompts):
- `HOIST_HETZNER_API_KEY`
- `HOIST_VULTR_API_KEY`
- `HOIST_DIGITALOCEAN_API_KEY`
- `HOIST_HOSTINGER_API_KEY`
- `HOIST_LINODE_API_KEY`
- `HOIST_SCALEWAY_API_KEY`

## Providers

```bash
hoist provider add --type <type>                         # Reads API key from HOIST_*_API_KEY env var
hoist provider list
hoist provider test [label]
hoist provider update [label]
hoist provider set-default [label]
hoist provider delete [label]
```

## Servers

```bash
hoist server create                                    # Auto: random name, cheapest type, first region
hoist server create --name <n> --provider <p> --type <t> --region <r>  # Explicit
hoist server import --ip <ip>                          # Auto: random name
hoist server import --name <n> --ip <ip> [--user <user>]
hoist server list [--provider <p>]
hoist server status <name> [--provider <p>]
hoist server regions [--provider <p>]                   # List available regions
hoist server types [--provider <p>]                     # List available server types
hoist server stats <name> [--provider <p>]              # CPU, memory, disk stats
hoist server ssh <name> [--provider <p>]
hoist server destroy <name> [--provider <p>]
```

## Deploy & Rollback

```bash
hoist deploy                                           # Deploys all app services
hoist deploy --service <name>                          # Deploy a specific service
hoist deploy --repo <url> [--branch <branch>]          # From Git repo
hoist rollback --service <name>                        # Server auto-resolved from hoist.json
```

## Templates (Databases & Services)

```bash
hoist deploy --template <type> --server <s>             # Create a database (postgres, mysql, redis, etc.)
hoist deploy --template <type> --server <s> --public    # Create with public access enabled
hoist template list                                     # Available template types
hoist template info <name>                              # Template details
hoist template services [--server <s>]                  # Running template services
hoist template inspect <name> [--server <s>]            # Connection string, status
hoist template backup <name> [--server <s>] [--output <path>]
hoist template destroy <name> [--server <s>] [--delete-volumes]
hoist template stop <name> [--server <s>]
hoist template start <name> [--server <s>]
hoist template restart <name> [--server <s>]
hoist template public <name> [--server <s>]             # Enable public access (opens firewall port)
hoist template private <name> [--server <s>]            # Disable public access (closes firewall port)
```

Supported types: `postgres`, `mysql`, `mariadb`, `redis`, `mongodb`

## Domains & SSL

```bash
hoist domain add <domain>                              # Auto-selects service if only one app
hoist domain add <domain> --service <name>             # Auto-SSL via Let's Encrypt
hoist domain list                                      # www/non-www handled automatically
hoist domain delete <domain>
```

Custom domains auto-redirect between www and non-www. User must point DNS A records for BOTH `example.com` AND `www.example.com` to the server IP.

## Environment Variables

```bash
hoist env set <service> KEY=VAL KEY2=VAL2              # Server auto-resolved from hoist.json
hoist env get <service> <key>
hoist env list <service>                               # Returns real values in JSON mode
hoist env delete <service> <key>
hoist env import <service> .env
hoist env export <service>
```

## Observability & Health

```bash
hoist logs <service> --lines 200                       # Application logs
hoist logs traefik --lines 200                         # Reverse proxy logs (502s, ACME errors, TLS issues)
hoist logs <service> --follow                          # Stream logs in real-time
hoist status                                           # Project-wide status + drift detection
hoist doctor                                           # Infrastructure health (SSH, Docker, Traefik, firewall)
```

### Troubleshooting escalation: `logs <service>` -> `logs traefik` -> `doctor` -> `status`

## SSH Keys & Config

```bash
hoist keys show
hoist keys rotate
hoist config validate
```

## Skills

```bash
hoist skills sync                                      # Sync global agent skill files
hoist skills export [dir]                              # Build a publishable skill bundle
```

## Utility

```bash
hoist --status                     # Quick overview: version, auth, providers
npm install -g hoist-cli@latest    # Update to latest version
```
