# 2.0.1 storage isolation repair candidate

Fix the confirmed cross-tenant storage-exhaustion finding in 2.0.0. Tenant reservations cover event counts and UTF-8 event-body bytes across all sessions. Their combined budgets are validated against fixed store ceilings. Configuration is operator-only and persisted, unknown tenants cannot allocate capacity, and conflicting worker policies fail closed. SQLite transactions preserve capacity and replay identifiers across rejected batches, concurrent connections, and restarts.

Before upgrading an existing service, stop all 2.0.0 writers, back up the database and configure every stored/writing tenant. Read SECURITY.md for migration and operational limits. Existing events are never automatically deleted. This candidate still requires ClawHub re-review.

# 2.0.0 repair candidate

Breaking security migration: authenticated endpoints, bounded input, exact dependency locks, verified or explicitly unsigned events, and corrected trust claims. See SECURITY.md and the combined REPAIR_REPORT.md.
