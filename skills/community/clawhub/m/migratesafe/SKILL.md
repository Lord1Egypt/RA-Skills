---
name: migratesafe
description: Database migration safety checker — catches destructive migrations before they reach production
homepage: https://migratesafe.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83d\uddc4\ufe0f",
      "primaryEnv": "MIGRATESAFE_LICENSE_KEY",
      "requires": {
        "bins": ["git", "bash", "python3", "jq"]
      },
      "configPaths": ["~/.openclaw/openclaw.json"],
      "install": [
        {
          "id": "lefthook",
          "kind": "brew",
          "formula": "lefthook",
          "bins": ["lefthook"],
          "label": "Install lefthook (git hooks manager)"
        }
      ],
      "os": ["darwin", "linux", "win32"]
    }
  }
user-invocable: true
disable-model-invocation: false
---

# MigrateSafe — Database Migration Safety Checker

MigrateSafe analyzes database migration files for destructive operations before they reach production. It detects DROP TABLE, column removals, risky type changes, missing rollbacks, lock hazards, and unsafe ALTER operations across raw SQL, Rails, Django, Knex.js, Prisma, Flyway, and Liquibase migrations. It uses regex-based pattern matching with risk scoring and produces compliance reports.

## Commands

### Free Tier (No license required)

#### `migratesafe scan [file|directory]`
One-shot scan of migration files for destructive operations.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/migratesafe.sh" scan [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Auto-detects migration framework (SQL, Rails, Django, Knex, Prisma, Flyway, Liquibase)
3. Finds all migration files in standard locations (db/migrate, migrations/, prisma/migrations, sql/)
4. Runs 15+ destructive operation patterns against each file
5. Calculates a risk score (0-100) per file and overall
6. Outputs findings with: file, line number, severity, operation, recommendation
7. Exit code 0 if safe, exit code 1 if critical/high risk operations detected
8. Free tier limited to 3 migration files per scan

**Example usage scenarios:**
- "Check my migrations for destructive operations" -> runs `migratesafe scan .`
- "Is this migration safe to deploy?" -> runs `migratesafe scan db/migrate/20240115_add_users.sql`
- "Scan my SQL files for DROP statements" -> runs `migratesafe scan migrations/`

#### `migratesafe help`
Show available commands and usage information.

```bash
bash "<SKILL_DIR>/scripts/migratesafe.sh" help
```

#### `migratesafe version`
Show version information.

```bash
bash "<SKILL_DIR>/scripts/migratesafe.sh" version
```

### Pro Tier ($19/user/month -- requires MIGRATESAFE_LICENSE_KEY)

#### `migratesafe hooks install`
Install git pre-commit hooks that scan staged migration files before every commit.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/migratesafe.sh" hooks install
```

**What it does:**
1. Validates Pro+ license
2. Copies lefthook config to project root
3. Installs lefthook pre-commit hook
4. On every commit: scans all staged migration files, blocks commit if critical/high risk, shows remediation advice

#### `migratesafe hooks uninstall`
Remove MigrateSafe git hooks.

```bash
bash "<SKILL_DIR>/scripts/migratesafe.sh" hooks uninstall
```

#### `migratesafe rollback-check [directory]`
Verify that every UP migration has a corresponding DOWN/rollback migration.

```bash
bash "<SKILL_DIR>/scripts/migratesafe.sh" rollback-check [directory]
```

**What it does:**
1. Validates Pro+ license
2. Scans migration directories for UP migrations
3. Checks for corresponding rollback/down files or reversible blocks
4. Reports missing rollbacks with severity assessment

#### `migratesafe diff <file1> <file2>`
Compare two schema versions and highlight dangerous changes.

```bash
bash "<SKILL_DIR>/scripts/migratesafe.sh" diff schema_v1.sql schema_v2.sql
```

**What it does:**
1. Validates Pro+ license
2. Compares two SQL schema files
3. Identifies dropped tables, removed columns, type changes
4. Shows side-by-side diff with risk annotations

### Team Tier ($39/user/month -- requires MIGRATESAFE_LICENSE_KEY with team tier)

#### `migratesafe history [directory]`
Show migration risk history across all migrations in the project.

```bash
bash "<SKILL_DIR>/scripts/migratesafe.sh" history [directory]
```

**What it does:**
1. Validates Team+ license
2. Scans all migration files chronologically
3. Builds a risk timeline showing when dangerous migrations were introduced
4. Reports cumulative risk score and trends

#### `migratesafe report [directory]`
Generate a full compliance report in markdown format.

```bash
bash "<SKILL_DIR>/scripts/migratesafe.sh" report [directory]
```

**What it does:**
1. Validates Team+ license
2. Runs full scan of all migration files
3. Generates a formatted markdown report from template
4. Includes per-file breakdowns, risk scores, recommendations, rollback status
5. Output suitable for compliance audits and change advisory boards

## Detected Destructive Operations

MigrateSafe detects 15+ destructive patterns across 7 migration frameworks:

| Category | Examples | Severity |
|----------|----------|----------|
| **Table Drops** | DROP TABLE, drop_table, DeleteModel, dropTable | Critical |
| **Truncation** | TRUNCATE TABLE, unconditional DELETE FROM | Critical |
| **Column Drops** | DROP COLUMN, remove_column, RemoveField, dropColumn | High |
| **Type Changes** | ALTER COLUMN...TYPE, change_column, AlterField | High |
| **Constraint Removal** | DROP CONSTRAINT, DROP INDEX, RemoveConstraint, remove_index | High |
| **NOT NULL Additions** | SET NOT NULL (without DEFAULT), add non-null column | Medium |
| **Missing Transactions** | Migrations not wrapped in BEGIN/COMMIT | Medium |
| **Lock Hazards** | CREATE INDEX (without CONCURRENTLY), ALTER TABLE on large tables | Medium |
| **Cascade Deletes** | ON DELETE CASCADE, CASCADE changes | Medium |
| **Column Renames** | RENAME COLUMN, rename_column, RenameField | Low |
| **Data Loss Risk** | REPLACE operations, ON DELETE SET NULL changes | Low |

## Supported Migration Frameworks

| Framework | File Pattern | Detection |
|-----------|-------------|-----------|
| **Raw SQL** | *.sql | Full SQL pattern matching |
| **Rails** | db/migrate/*.rb | remove_column, drop_table, change_column, etc. |
| **Django** | migrations/*.py | RemoveField, DeleteModel, AlterField, etc. |
| **Knex.js** | migrations/*.js/*.ts | dropTable, dropColumn, raw.*DROP, etc. |
| **Prisma** | prisma/migrations/*.sql | Full SQL pattern matching |
| **Flyway** | sql/V*.sql | Full SQL pattern matching |
| **Liquibase** | *.xml changesets | dropTable, dropColumn, modifyDataType, etc. |

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

## Important Notes

- **Free tier** works immediately -- no configuration needed
- **All scanning happens locally** -- no code or schema data sent to external servers
- **License validation is offline** -- no phone-home or network calls
- Supports multiple migration frameworks in the same project
- Risk scores are cumulative -- a file with multiple issues scores higher
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = safe, 1 = dangerous operations detected (for CI/CD integration)

## Error Handling

- If lefthook is not installed and user tries `hooks install`, prompt to install it
- If license key is invalid or expired, show clear message with link to https://migratesafe.pages.dev/renew
- If no migration files found in target, report clean scan with info message
- If a file is binary, skip it automatically with no warning
- If migration framework cannot be determined, fall back to raw SQL pattern matching

## When to Use MigrateSafe

The user might say things like:
- "Check my migrations for destructive operations"
- "Is this migration safe to run?"
- "Scan for DROP TABLE statements"
- "Verify my rollback migrations exist"
- "Generate a migration safety report"
- "Set up pre-commit hooks for migrations"
- "Check if this schema change is dangerous"
- "Block destructive migrations from being committed"
- "Compare two schema versions"
- "Show migration risk history"
