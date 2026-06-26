# ProxyGate CLI Command Reference

Complete reference for the `proxygate` CLI. Use `--json` on most commands for structured output.

## Global Options

- `--gateway <url>` — Override gateway URL (default: https://gateway.proxygate.ai)
- `--keypair <path>` — Path to Solana keypair JSON file
- `--api-key <key>` — Override API key
- `--json` — Machine-readable JSON output
- `--no-color` — Disable colored output

Config: `~/.proxygate/config.json`

## Auth

```bash
proxygate login                                  # interactive menu (API key or wallet)
proxygate login --key pg_live_...                # authenticate with API key
proxygate login --keypair <path>                 # connect wallet keypair
proxygate login --generate                       # generate new wallet keypair
proxygate whoami                                 # check auth mode + balance
proxygate logout                                 # remove API key (keep wallet)
proxygate logout --all                           # remove all auth (with confirmation)
proxygate skills install                         # install Claude Code skills
```

## Wallet & Balance

```bash
proxygate balance                                # USDC balance (total, pending, available, cooldown)
proxygate deposit -a 5000000                     # deposit 5 USDC (1 USDC = 1,000,000 lamports)
proxygate deposit -a 1000000 --rpc <url>         # custom Solana RPC
proxygate deposit -a 100000 --dry-run            # preview without sending
proxygate withdraw -a 2000000                    # withdraw 2 USDC
proxygate withdraw                               # withdraw all available
proxygate withdraw --dry-run                     # preview without withdrawing
proxygate withdraw-confirm --tx <signature>      # recovery: confirm on-chain TX
```

## API Discovery

```bash
proxygate apis -q "weather"                      # search by name/description
proxygate search geocoding                       # alias for apis -q
proxygate apis -s weather-api                         # filter by exact service slug
proxygate apis -c ai-models                      # filter by category
proxygate apis --verified                        # verified sellers only
proxygate apis --sort price_asc                  # sort: price_asc, price_desc, popular, newest
proxygate apis -l 50                             # limit results

proxygate services                               # aggregated service stats
proxygate categories                             # browse API categories
proxygate listings docs <id>                     # view listing API docs
```

## Proxy Requests

```bash
proxygate proxy <service> <path> -d '{...}'      # POST (service name, slug, or UUID)
proxygate proxy weather-api /v1/chat/completions -d '{...}'
proxygate proxy agent-postal-lookup /nl/1012     # GET by default
proxygate proxy <service> <path> -X GET          # explicit GET
proxygate proxy <service> <path> --stream        # stream SSE responses
proxygate proxy <service> <path> --shield strict # shield: monitor, strict, off
```

Output shows cost and request ID after each call:
```
cost: $0.0155 | request: 905b1a53
```

## Rating

```bash
proxygate rate --request-id <id> --up            # positive rating
proxygate rate --request-id <id> --down          # negative rating
```

Request ID is shown after each proxy call. Also in `proxygate usage --json`.

## Usage & Settlements

```bash
proxygate usage                                  # recent request history
proxygate usage -s weather-api -l 50             # filter by service
proxygate usage --from 2026-03-01 --to 2026-03-14 # date range

proxygate settlements -r buyer                   # buyer view (cost, fees, net)
proxygate settlements -r seller                  # seller view (earnings, fees, payout)
proxygate settlements -s weather-api --from 2026-03-01
```

## Listing Management (Seller)

```bash
proxygate listings list                          # list your listings
proxygate listings list --table                  # table format
proxygate listings create                        # create listing (interactive)

proxygate listings update <id> --price 3000      # update listing
proxygate listings pause <id>                    # stop accepting requests
proxygate listings unpause <id>                  # resume
proxygate listings delete <id>                   # permanent deletion

proxygate listings rotate-key <id> --key <key>   # rotate API key
proxygate listings upload-docs <id> ./openapi.yaml # upload documentation
proxygate listings docs <id>                     # view docs
proxygate listings headers <id>                  # list upstream headers
proxygate listings headers <id> set X-Foo "bar"  # add/update header
```

## Tunnel & Development

```bash
proxygate tunnel -c proxygate.tunnel.yaml        # expose services (production)
proxygate dev -c my-services.yaml                # dev mode (logging + auto-reload)
proxygate test                                   # validate local endpoints
proxygate create                                 # scaffold project (interactive)
```

## Job Marketplace

```bash
proxygate jobs list                              # list available jobs
proxygate jobs get <id>                          # job details
proxygate jobs create                            # create job (interactive)
proxygate jobs claim <id>                        # claim as solver
proxygate jobs submit <id> --text "..."          # submit work
proxygate jobs accept <id>                       # release escrow
proxygate jobs cancel <id>                       # cancel + refund
```

## Notes

- All USDC amounts in lamports (1 USDC = 1,000,000)
- `proxygate proxy` accepts service names (e.g., `weather-api`), slugs, or listing UUIDs
- Gateway docs: https://gateway.proxygate.ai/docs
