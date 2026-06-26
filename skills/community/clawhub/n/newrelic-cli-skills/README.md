# newrelic-cli-skills

An [OpenClaw](https://openclaw.ai) agent skill for monitoring, querying, and managing New Relic observability data via the `newrelic` CLI.

## What It Does

- **Performance triage** — identify slow transactions, DB bottlenecks, and error spikes
- **NRQL queries** — run ad-hoc queries against your New Relic account from the terminal
- **Deployment markers** — record releases so you can correlate deploys with performance changes
- **Alert management** — create and manage alert policies, conditions, and channels, including condition deletion workflows
- **Infrastructure monitoring** — host CPU, memory, disk, and process metrics
- **Agent diagnostics** — validate agent config and connectivity

## Requirements

- [`newrelic` CLI](https://github.com/newrelic/newrelic-cli) installed
- `NEW_RELIC_API_KEY` — User key (starts with `NRAK-`)
- `NEW_RELIC_ACCOUNT_ID` — Numeric account ID

## Install CLI

Use a package manager or install the binary manually from the official New Relic CLI releases page.

### Option 1: Homebrew (macOS)

```bash
brew install newrelic-cli
```

### Option 2: Manual install from official releases

1. Open https://github.com/newrelic/newrelic-cli/releases
2. Download the archive for your OS/architecture
3. Extract it
4. Move the `newrelic` binary into a directory on your `PATH`
5. Verify with:

```bash
newrelic --version
```

## Setup

```bash
newrelic profile add \
  --profile default \
  --apiKey $NEW_RELIC_API_KEY \
  --accountId $NEW_RELIC_ACCOUNT_ID \
  --region US

newrelic profile default --profile default
```

## Sub-skills

| Sub-skill | Purpose |
|---|---|
| `apm/` | Performance triage — slow transactions, DB analysis, error rates |
| `nrql/` | NRQL query patterns and ad-hoc data exploration |
| `deployments/` | Deployment markers and release tracking |
| `alerts/` | Alert policies, conditions, channels |
| `infrastructure/` | Host metrics — CPU, memory, disk, processes |
| `diagnostics/` | Agent health, config validation, connectivity |

## Scripts

| Script | Purpose |
|---|---|
| `check-performance.sh` | Health check across all apps |
| `deployment-marker.sh` | Record a deployment event |
| `top-slow-transactions.sh` | Find the 10 slowest transactions |
| `error-report.sh` | Recent errors with messages and counts |

## License

MIT
