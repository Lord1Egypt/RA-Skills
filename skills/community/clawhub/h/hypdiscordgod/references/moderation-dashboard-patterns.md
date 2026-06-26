# Moderation Dashboard Patterns

Use this reference when building a web UI for moderation settings or actions.

## Good First Views

- guild moderation settings
- warning history lookup
- ticket/mod-log search
- action presets for timeout, warn, or role policy
- audit log view for dashboard-triggered actions

## Safe Rules

- require strong auth and guild permission checks
- separate read-only views from mutating actions
- log moderator identity for dashboard-triggered actions
- confirm destructive actions before execution
- keep dashboard action execution auditable even if the bot performs the final Discord-side step

## Good Shared Data

- guild moderation config
- warning records
- escalation thresholds
- channel/role mappings
- audit logs
