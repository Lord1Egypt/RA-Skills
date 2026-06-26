# Skill Lifecycle Model

```
Install → First use → Active → Declining → Zombie → Uninstall
```

| Stage | Trigger | Behavior |
|-------|---------|----------|
| Install | Skill directory exists | Record install time |
| First use | First invocation | Measure activation delay |
| Active | ≥2 calls in 7 days | Compute frequency |
| Declining | This week < 50% of last | Internal flag |
| Zombie | No call in 30 days | Surface in `clean` |
| Uninstall | User-triggered | Backup to `trash/` |

Activation rate = `active_skills / total_installed` (report as %)

## Privacy model: consent-first

Mapick asks for network consent **before** any remote call. On first install, `recommend` / `search` / `bundle` / `security` / `report` require the user to explicitly choose one of:
- **Allow & remember** (`network_consent: always`) — all future calls proceed without prompting
- **This time only** (`network_consent: once`) — one call, then ask again next time
- **Local only** (`network_consent: declined`) — no remote calls; local features only

Without explicit consent, the skill operates in local-only mode: `status`, `diagnose`, `doctor`, `scan`, `clean` (heuristic), and `security` (local pattern scan) all work offline. No data is sent to api.mapick.ai until the user agrees.

To audit outbound requests: `/mapick privacy log`. To withdraw consent: `/mapick privacy consent-decline`.

## Decline / re-enable flow

If the user runs `/mapick privacy consent-decline`:
- CONFIG.md gets `consent_declined: true`.
- Remote commands (`recommend` / `search` / `bundle install` / `recommend:track` / `privacy trust` / `report` / `share` / `security` / `security:report` / `clean:track` / `workflow` / `daily` / `weekly`) are refused **client-side** with `error: "disabled_in_local_mode"`.
- Local commands (`status` / `scan` / `clean` reading local mtime only / `uninstall` / `privacy status` / `privacy delete-all` / `privacy log`) keep working.
- `notify` cron is not re-registered on subsequent inits.

To resume data sharing, run `/mapick privacy consent-agree`. Clears the declined flag, re-registers the notify cron, and remote commands work again.

## Auto-trigger on new conversation

When AI detects a new Mapick session, it may auto-run `bash shell init` (idempotent, 30-min cooldown). This only performs **local** operations:
- `first_install` → render the Welcome card per `reference/rendering.md#first_install`.
- `rescanned`, `changed: true` → briefly mention what changed.
- `rescanned`, `changed: false` / `skip` → silent.

**No remote calls are made during auto-init.** The `init` handler does not call any external API. Network-consent gated commands (`recommend`, `search`, etc.) are only invoked when the user explicitly asks for them, and the consent gate blocks them until the user agrees.

The `notify` cron is only registered when the user explicitly runs `privacy consent-agree` — the consent agreement handler includes the cron registration plan. If consent is declined, the cron is never registered and is removed on subsequent inits.
