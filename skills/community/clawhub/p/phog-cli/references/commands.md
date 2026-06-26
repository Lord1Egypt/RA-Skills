# PostHog CLI — Complete Command Reference

## activity

Quick analytics commands.

```bash
# Full product summary (recommended starting point)
posthog activity summary
posthog activity summary --date-from -90d

# Active users
posthog activity users                            # weekly (default)
posthog activity users --period daily
posthog activity users --period monthly
posthog activity users --date-from -90d

# Top events by volume
posthog activity events
posthog activity events --date-from -30d --limit 20

# Pageview trends
posthog activity pageviews
posthog activity pageviews --date-from -7d --interval hour
posthog activity pageviews --interval week
```

## auth

```bash
posthog auth login                                # auto-detect US/EU cloud
posthog auth login --host https://posthog.co.com  # self-hosted
posthog auth status                               # show current auth
posthog auth logout                               # remove credentials
```

## org

```bash
posthog org list                                  # list organizations
posthog org get <org-id>                          # organization details
```

## project

```bash
posthog project list                              # list all projects
posthog project current                           # show active project
posthog project switch <project-id>               # set active project
```

## flag

```bash
# List
posthog flag list
posthog flag list --active                        # only active flags
posthog flag list --search "keyword"

# CRUD
posthog flag get <flag-id>
posthog flag create --key <key> --name "Name"
posthog flag create --key <key> --name "Name" --rollout-percentage 50
posthog flag update <flag-id> --active            # enable
posthog flag update <flag-id> --no-active         # disable
posthog flag update <flag-id> --rollout-percentage 100
posthog --yes flag delete <flag-id>
```

## experiment

```bash
# List and get
posthog experiment list
posthog experiment get <id>

# Create (draft)
posthog experiment create --name "Name" --feature-flag-key <key>

# Lifecycle
posthog experiment update <id> --launch
posthog experiment update <id> --end

# Results
posthog experiment results <id>
posthog experiment results <id> --refresh

# Delete
posthog --yes experiment delete <id>
```

## survey

```bash
# List and get
posthog survey list
posthog survey get <survey-id>

# Create
posthog survey create --name "Name" --questions-json '[{"type": "open", "question": "Feedback?"}]'
posthog survey create --name "Name" --from-file survey.json
posthog survey create --name "Name" --type api --questions-json '[...]'

# Lifecycle
posthog survey update <survey-id> --start
posthog survey update <survey-id> --stop
posthog survey update <survey-id> --name "New Name"
posthog survey update <survey-id> --data-json '{"key": "value"}'

# Stats
posthog survey stats <survey-id>
posthog survey stats <survey-id> --date-from 2024-01-01 --date-to 2024-12-31

# Delete
posthog --yes survey delete <survey-id>
```

## dashboard

```bash
posthog dashboard list
posthog dashboard get <id>
posthog dashboard create --name "Name"
posthog dashboard update <id> --name "New Name"
posthog dashboard add-insight <dashboard-id> --insight-id <insight-id>
posthog --yes dashboard delete <id>
```

## insight

```bash
posthog insight list
posthog insight get <id>
posthog insight query <id>                        # execute saved query
posthog insight query <id> --refresh              # force refresh
posthog insight create --name "Name" --query-json '{"kind": "TrendsQuery", ...}'
posthog insight update <id> --name "New Name"
posthog --yes insight delete <id>
```

## error

```bash
posthog error list
posthog error list --limit 100
posthog error list --status active                # active, resolved, archived
posthog error list --search "TypeError"
posthog error get <issue-id>
posthog error update <issue-id> --status resolved
posthog error update <issue-id> --assignee <user-id>
```

## log

```bash
posthog log query
posthog log query --date-from -1d
posthog log attributes                            # list filterable attributes
```

## query

```bash
# HogQL (SQL-like)
posthog query run --hogql "SELECT event, count() FROM events GROUP BY event ORDER BY count() DESC LIMIT 10"

# From JSON file (InsightVizNode, TrendsQuery, FunnelsQuery, etc.)
posthog query run --from-file query.json

# Natural language to HogQL
posthog query generate "top 10 countries by pageviews last month"
```

## search

```bash
posthog search persons --search "john@example.com"
posthog search events --search "checkout"
posthog search groups
posthog search properties
```

## api

Raw API escape hatch. All requests scoped to active project.

```bash
posthog api get <path>
posthog api post <path> --data '<json>'
posthog api patch <path> --data '<json>'
posthog --yes api delete <path>
```

Examples:

```bash
posthog api get /surveys/
posthog api post /query/ --data '{"query": {"kind": "HogQLQuery", "query": "SELECT 1"}}'
posthog api patch /feature_flags/123/ --data '{"active": false}'
```
