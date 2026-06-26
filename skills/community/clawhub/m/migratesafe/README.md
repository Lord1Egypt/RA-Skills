# MigrateSafe

**Catch destructive database migrations before they reach production.**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Shell](https://img.shields.io/badge/shell-bash-orange)

MigrateSafe is a static analysis tool that scans your database migration files for destructive operations -- DROP TABLE, column removals, risky type changes, missing rollbacks, lock hazards, and more. It works with raw SQL, Rails, Django, Knex.js, Prisma, Flyway, and Liquibase migrations. Everything runs locally. No code leaves your machine.

## Quick Start

```bash
# Scan your migrations directory
migratesafe scan .

# Scan a specific file
migratesafe scan db/migrate/20240115_add_users.sql

# Install pre-commit hooks (Pro)
migratesafe hooks install
```

## What It Catches

| Category | Examples | Severity |
|----------|----------|----------|
| Table Drops | `DROP TABLE`, `drop_table`, `DeleteModel`, `dropTable` | Critical |
| Truncation | `TRUNCATE TABLE`, unconditional `DELETE FROM` | Critical |
| Column Drops | `DROP COLUMN`, `remove_column`, `RemoveField`, `dropColumn` | High |
| Type Changes | `ALTER COLUMN...TYPE`, `change_column`, `AlterField` | High |
| Constraint Removal | `DROP CONSTRAINT`, `DROP INDEX`, `RemoveConstraint` | High |
| NOT NULL Additions | `SET NOT NULL` without `DEFAULT` | Medium |
| Missing Transactions | Migrations not wrapped in `BEGIN`/`COMMIT` | Medium |
| Lock Hazards | `CREATE INDEX` without `CONCURRENTLY` | Medium |
| Cascade Deletes | `ON DELETE CASCADE` changes | Medium |
| Column Renames | `RENAME COLUMN`, `rename_column`, `RenameField` | Low |

Over 50 patterns across 7 frameworks.

## Supported Frameworks

| Framework | File Pattern | Detection |
|-----------|-------------|-----------|
| **Raw SQL** | `*.sql` | Full SQL pattern matching |
| **Rails** | `db/migrate/*.rb` | `remove_column`, `drop_table`, `change_column`, etc. |
| **Django** | `migrations/*.py` | `RemoveField`, `DeleteModel`, `AlterField`, etc. |
| **Knex.js** | `migrations/*.js/*.ts` | `dropTable`, `dropColumn`, `.raw.*DROP`, etc. |
| **Prisma** | `prisma/migrations/*.sql` | Full SQL pattern matching |
| **Flyway** | `sql/V*.sql` | Full SQL pattern matching + versioned undo detection |
| **Liquibase** | `*.xml` changesets | `dropTable`, `dropColumn`, `modifyDataType`, etc. |

Framework is auto-detected from file extension and directory structure.

## How It Works

1. **Detect** -- MigrateSafe finds migration files in your project and identifies the framework (Rails, Django, SQL, etc.)
2. **Scan** -- Each file is analyzed against 50+ destructive operation patterns with severity scoring
3. **Report** -- Results are displayed with file, line number, severity, description, and remediation advice

Exit code `0` means safe. Exit code `1` means destructive operations were found. Plug it into any CI/CD pipeline.

## Commands

| Command | Tier | Description |
|---------|------|-------------|
| `scan [file\|dir]` | Free | Scan migrations for destructive operations (3 file limit) |
| `hooks install` | Pro | Install lefthook pre-commit hooks |
| `hooks uninstall` | Pro | Remove MigrateSafe hooks |
| `rollback-check [dir]` | Pro | Verify every migration has a rollback |
| `diff <file1> <file2>` | Pro | Compare two schema files for dangerous changes |
| `history [dir]` | Team | Migration risk timeline across all migrations |
| `report [dir]` | Team | Generate full compliance report (markdown) |
| `status` | Free | Show license and config info |

## Pre-Commit Hooks

MigrateSafe integrates with [lefthook](https://github.com/evilmartians/lefthook) to automatically scan staged migration files before every commit. If destructive operations are detected, the commit is blocked with actionable advice.

```bash
# Install hooks (requires Pro license)
migratesafe hooks install

# Now every git commit scans staged migration files automatically
git add db/migrate/20240120_remove_users.sql
git commit -m "remove users table"
# => BLOCKED: DROP TABLE detected. Run 'migratesafe scan' for details.
```

## Comparison

| Feature | MigrateSafe | Flyway Teams | Atlas | sqitch |
|---------|------------|--------------|-------|--------|
| Destructive operation detection | Yes | Limited | Yes | No |
| Multi-framework support | 7 frameworks | SQL only | SQL only | SQL only |
| Risk scoring | 0-100 scale | No | Basic | No |
| Pre-commit hooks | Yes | No | Yes | No |
| Rollback verification | Yes | Basic | Yes | Yes |
| Compliance reports | Yes | Enterprise | No | No |
| Offline / local only | Yes | No | No | Yes |
| Price | From $0 | $500/yr | $99/mo | Free |

## Pricing

| | Free | Pro | Team |
|---|---|---|---|
| **Price** | $0 | $19/user/month | $39/user/month |
| Migration scanning | 3 files | Unlimited | Unlimited |
| Pre-commit hooks | -- | Yes | Yes |
| Rollback verification | -- | Yes | Yes |
| Schema diff | -- | Yes | Yes |
| Risk timeline | -- | -- | Yes |
| Compliance reports | -- | -- | Yes |

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "migratesafe": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY",
        "config": {
          "severityThreshold": "high",
          "migrationDirs": ["db/migrate", "migrations", "prisma/migrations", "sql"],
          "ignorePatterns": ["**/test/**", "**/seed/**"],
          "requireRollbacks": true,
          "blockOnCritical": true
        }
      }
    }
  }
}
```

Or set the environment variable:

```bash
export MIGRATESAFE_LICENSE_KEY="your-jwt-license-key"
```

## Part of the ClawHub Ecosystem

MigrateSafe is a [ClawHub](https://clawhub.dev) skill -- an AI-native developer tool that works with the OpenClaw CLI. Other skills in the ecosystem:

- **APIShield** -- API endpoint security auditor
- **EnvGuard** -- Environment variable leak prevention
- **DepGuard** -- Dependency vulnerability scanner
- **DocSync** -- Documentation drift detector
- **GitPulse** -- Git workflow analytics

## License

MIT
