#!/usr/bin/env bash
# MigrateSafe — Destructive Migration Pattern Definitions
# Each pattern: REGEX | SEVERITY | CATEGORY | DESCRIPTION | RECOMMENDATION
#
# Severity levels:
#   critical — Irreversible data loss (DROP TABLE, TRUNCATE)
#   high     — Significant data/schema loss (DROP COLUMN, type change)
#   medium   — Potential issues (NOT NULL without default, missing CONCURRENTLY)
#   low      — Minor concerns (renames, reordering)
#
# IMPORTANT: All regexes must use POSIX ERE syntax (grep -E compatible).

set -euo pipefail

# ─── SQL Patterns ────────────────────────────────────────────────────────────
# Raw SQL destructive operations — applies to .sql files, Prisma, Flyway

declare -a MIGRATESAFE_SQL_PATTERNS=()

# CRITICAL: Irreversible data destruction
MIGRATESAFE_SQL_PATTERNS+=(
  'DROP[[:space:]]+TABLE[[:space:]]+(IF[[:space:]]+EXISTS[[:space:]]+)?[A-Za-z_"`\[]+|critical|drop_table|DROP TABLE — Permanently deletes table and all data|Add a backup step before dropping. Consider renaming the table first (e.g. _deprecated_tablename) and dropping after a soak period.'
  'TRUNCATE[[:space:]]+(TABLE[[:space:]]+)?[A-Za-z_"`\[]+|critical|truncate|TRUNCATE — Removes all rows instantly without logging individual deletes|Use DELETE with a WHERE clause for selective removal. If full truncate is needed, ensure a backup exists and wrap in a transaction.'
  'DELETE[[:space:]]+FROM[[:space:]]+[A-Za-z_"`\[]+[[:space:]]*;|critical|delete_no_where|DELETE FROM without WHERE clause — Deletes all rows in the table|Add a WHERE clause to limit deletion scope. If intentional, use TRUNCATE explicitly and document the reason.'
  'DROP[[:space:]]+DATABASE[[:space:]]+(IF[[:space:]]+EXISTS[[:space:]]+)?[A-Za-z_"`\[]+|critical|drop_database|DROP DATABASE — Destroys entire database|This should almost never appear in a migration. Remove this statement and handle database lifecycle separately.'
  'DROP[[:space:]]+SCHEMA[[:space:]]+(IF[[:space:]]+EXISTS[[:space:]]+)?[A-Za-z_"`\[]+|critical|drop_schema|DROP SCHEMA — Destroys entire schema and all objects|Remove this statement. Schema drops should be handled outside of migration files.'
)

# HIGH: Significant data/schema loss
MIGRATESAFE_SQL_PATTERNS+=(
  'ALTER[[:space:]]+TABLE[[:space:]]+[A-Za-z_"`\[]+[[:space:]]+DROP[[:space:]]+COLUMN[[:space:]]+|high|drop_column|DROP COLUMN — Permanently removes column and its data|Create the column as nullable/deprecated first. Migrate reads away from the column. Drop after verification period.'
  'ALTER[[:space:]]+TABLE[[:space:]]+[A-Za-z_"`\[]+[[:space:]]+DROP[[:space:]]+CONSTRAINT[[:space:]]+|high|drop_constraint|DROP CONSTRAINT — Removes integrity constraint|Verify no application logic depends on this constraint. Document the reason and ensure data integrity is maintained by application code.'
  'ALTER[[:space:]]+TABLE[[:space:]]+[A-Za-z_"`\[]+[[:space:]]+ALTER[[:space:]]+COLUMN[[:space:]]+[A-Za-z_"`\[]+[[:space:]]+(SET[[:space:]]+DATA[[:space:]]+)?TYPE[[:space:]]+|high|type_change|Column type change — May cause data truncation or conversion errors|Test the type change on a copy of production data first. Add explicit USING clause for safe conversion. Consider a staged migration.'
  'ALTER[[:space:]]+TABLE[[:space:]]+[A-Za-z_"`\[]+[[:space:]]+MODIFY[[:space:]]+COLUMN[[:space:]]+|high|modify_column|MODIFY COLUMN — Column definition change that may alter data|Verify the new definition is compatible with existing data. Test on production-like data before deploying.'
  'DROP[[:space:]]+INDEX[[:space:]]+(IF[[:space:]]+EXISTS[[:space:]]+)?(CONCURRENTLY[[:space:]]+)?[A-Za-z_"`\[]+|high|drop_index|DROP INDEX — Removes index, may cause severe query performance degradation|Verify no queries depend on this index. Consider the query performance impact. Drop during low-traffic periods.'
  'ALTER[[:space:]]+TABLE[[:space:]]+[A-Za-z_"`\[]+[[:space:]]+RENAME[[:space:]]+TO[[:space:]]+|high|rename_table|RENAME TABLE — Breaks all queries referencing the old name|Deploy application code changes first to handle both names. Use a view with the old name as a bridge.'
)

# MEDIUM: Potential issues
MIGRATESAFE_SQL_PATTERNS+=(
  'ALTER[[:space:]]+TABLE[[:space:]]+[A-Za-z_"`\[]+[[:space:]]+ALTER[[:space:]]+COLUMN[[:space:]]+[A-Za-z_"`\[]+[[:space:]]+SET[[:space:]]+NOT[[:space:]]+NULL|medium|set_not_null|SET NOT NULL without DEFAULT — Will fail if any existing rows have NULL values|Add a DEFAULT value first, backfill NULLs, then add the NOT NULL constraint. Or use a CHECK constraint instead.'
  'ALTER[[:space:]]+TABLE[[:space:]]+[A-Za-z_"`\[]+[[:space:]]+ADD[[:space:]]+COLUMN[[:space:]]+[A-Za-z_"`\[]+[[:space:]]+[A-Za-z]+[^;]*NOT[[:space:]]+NULL[^;]*;|medium|add_not_null_column|Adding NOT NULL column — Requires DEFAULT or backfill for existing rows|Add the column as nullable first, backfill data, then set NOT NULL. Or provide a DEFAULT value.'
  'CREATE[[:space:]]+INDEX[[:space:]]+[A-Za-z_"`\[]+|medium|index_no_concurrent|CREATE INDEX without CONCURRENTLY — Acquires exclusive lock, blocks writes|Use CREATE INDEX CONCURRENTLY to avoid blocking writes during index creation (PostgreSQL). For MySQL, consider pt-online-schema-change.'
  'ON[[:space:]]+DELETE[[:space:]]+CASCADE|medium|cascade_delete|ON DELETE CASCADE — Automatic cascade deletes can cause unexpected data loss|Verify cascade behavior is intended. Consider ON DELETE RESTRICT or ON DELETE SET NULL. Add application-level soft-delete logic.'
  'REPLACE[[:space:]]+INTO[[:space:]]+|medium|replace_into|REPLACE INTO — Deletes then re-inserts, losing auto-increment values and triggers|Use INSERT...ON CONFLICT UPDATE (PostgreSQL) or INSERT...ON DUPLICATE KEY UPDATE (MySQL) instead.'
  'ON[[:space:]]+DELETE[[:space:]]+SET[[:space:]]+NULL|medium|on_delete_set_null|ON DELETE SET NULL — May cause data integrity issues in referencing rows|Verify that NULL is a valid state for the foreign key column. Consider using ON DELETE RESTRICT instead.'
)

# LOW: Minor concerns
MIGRATESAFE_SQL_PATTERNS+=(
  'ALTER[[:space:]]+TABLE[[:space:]]+[A-Za-z_"`\[]+[[:space:]]+RENAME[[:space:]]+COLUMN[[:space:]]+|low|rename_column|RENAME COLUMN — Application code must be updated to use new name|Deploy application code changes first that handle both old and new column names. Use a phased rollout.'
  'ALTER[[:space:]]+TABLE[[:space:]]+[A-Za-z_"`\[]+[[:space:]]+ALTER[[:space:]]+COLUMN[[:space:]]+[A-Za-z_"`\[]+[[:space:]]+SET[[:space:]]+DEFAULT|low|change_default|SET DEFAULT — Changes default value for new rows|Verify the new default is correct for all application code paths. Existing rows are not affected.'
  'ALTER[[:space:]]+TABLE[[:space:]]+[A-Za-z_"`\[]+[[:space:]]+DROP[[:space:]]+DEFAULT|low|drop_default|DROP DEFAULT — Removes default value from column|Ensure all INSERT statements explicitly provide a value for this column.'
)

# ─── Rails Patterns ──────────────────────────────────────────────────────────
# Ruby on Rails migration methods (db/migrate/*.rb)

declare -a MIGRATESAFE_RAILS_PATTERNS=()

MIGRATESAFE_RAILS_PATTERNS+=(
  'drop_table[[:space:]]*[:(]|critical|drop_table|drop_table — Permanently deletes table and all data|Use safety_assured block if intentional. Consider renaming table first with a deprecation period.'
  'remove_column[[:space:]]*[:(]|high|drop_column|remove_column — Permanently removes column and its data|Mark column as ignored in model first (self.ignored_columns). Deploy. Then remove in a separate migration.'
  'change_column[[:space:]]*[:(]|high|type_change|change_column — Column type or constraint change that may alter data|Use change_column_default or change_column_null for specific changes. Test type conversion on production data copy.'
  'remove_index[[:space:]]*[:(]|high|drop_index|remove_index — Removes database index|Verify no queries depend on this index. Check EXPLAIN plans for affected queries.'
  'rename_table[[:space:]]*[:(]|high|rename_table|rename_table — Breaks ActiveRecord and all queries using old name|Deploy code changes first. Consider creating a view with the old name as a bridge.'
  'change_column_null[[:space:]]*[:(].*false|medium|set_not_null|change_column_null to NOT NULL — Will fail if existing rows have NULL values|Backfill NULL values first in a separate migration. Then add the NOT NULL constraint.'
  'remove_foreign_key[[:space:]]*[:(]|medium|drop_constraint|remove_foreign_key — Removes referential integrity constraint|Verify application logic maintains integrity. Document reason for removal.'
  'remove_reference[[:space:]]*[:(]|high|drop_column|remove_reference — Removes column and associated index/foreign key|Mark as ignored in model first. Deploy. Remove in separate migration.'
  'rename_column[[:space:]]*[:(]|low|rename_column|rename_column — Application code must be updated to use new name|Deploy model alias first (alias_attribute). Then rename in a separate migration.'
  'execute[[:space:]]*[("'"'"']|medium|raw_sql|execute with raw SQL — Bypasses ActiveRecord safety checks|Review raw SQL carefully. Ensure it is idempotent and has a reversible counterpart.'
)

# ─── Django Patterns ─────────────────────────────────────────────────────────
# Django migration operations (migrations/*.py)

declare -a MIGRATESAFE_DJANGO_PATTERNS=()

MIGRATESAFE_DJANGO_PATTERNS+=(
  'DeleteModel|critical|drop_table|DeleteModel — Permanently deletes table and all data|Add a deprecation period. Remove all foreign keys to this model first in a separate migration.'
  'RemoveField|high|drop_column|RemoveField — Permanently removes column and its data|Remove field usage from all code first. Deploy. Then remove field in separate migration.'
  'AlterField|high|type_change|AlterField — Field type or constraint change|Verify the alteration is backward-compatible. Test with production data. Consider a multi-step migration.'
  'RemoveConstraint|high|drop_constraint|RemoveConstraint — Removes database constraint|Verify no logic depends on this constraint. Document the reason for removal.'
  'RemoveIndex|high|drop_index|RemoveIndex — Removes database index|Check query performance impact. Verify no queries depend on this index.'
  'RenameModel|high|rename_table|RenameModel — Renames table, breaks queries using old name|Update all references in code first. Deploy. Then rename in a separate migration.'
  'RenameField|low|rename_column|RenameField — Renames column, code must use new name|Update all field references in code first. Deploy. Then rename in a separate migration.'
  'RunSQL|medium|raw_sql|RunSQL — Executes raw SQL, bypasses Django ORM safety|Review SQL carefully. Provide reverse_sql for rollback support.'
  'RunPython|medium|raw_python|RunPython — Executes arbitrary Python code in migration|Ensure function is idempotent. Provide reverse_code for rollback. Test thoroughly.'
  'AlterModelOptions|low|alter_options|AlterModelOptions — Changes model Meta options|Verify ordering, permissions, and other meta changes are backward-compatible.'
)

# ─── Knex.js Patterns ────────────────────────────────────────────────────────
# Knex.js migration methods (migrations/*.js or *.ts)

declare -a MIGRATESAFE_KNEX_PATTERNS=()

MIGRATESAFE_KNEX_PATTERNS+=(
  '\.dropTable[[:space:]]*\(|critical|drop_table|dropTable — Permanently deletes table and all data|Consider renaming the table first. Add a soak period before dropping.'
  'dropTableIfExists[[:space:]]*\(|critical|drop_table|dropTableIfExists — Drops table if it exists|Ensure this is intentional and data has been migrated. Add backup verification.'
  '\.dropColumn[[:space:]]*\(|high|drop_column|dropColumn — Permanently removes column and its data|Remove column usage from application code first. Deploy. Then drop in a separate migration.'
  '\.dropColumns[[:space:]]*\(|high|drop_column|dropColumns — Removes multiple columns at once|Remove usage from code first. Consider dropping columns individually in separate migrations.'
  '\.renameTable[[:space:]]*\(|high|rename_table|renameTable — Renames table, breaks queries using old name|Update all references in application code first. Deploy. Then rename.'
  '\.renameColumn[[:space:]]*\(|low|rename_column|renameColumn — Renames column, code must use new name|Update column references in code first. Deploy. Then rename.'
  '\.dropForeign[[:space:]]*\(|medium|drop_constraint|dropForeign — Removes foreign key constraint|Verify application maintains referential integrity. Document the reason.'
  '\.dropIndex[[:space:]]*\(|high|drop_index|dropIndex — Removes database index|Check query performance impact before removing.'
  '\.dropUnique[[:space:]]*\(|medium|drop_constraint|dropUnique — Removes unique constraint|Verify application logic prevents duplicates. Document the reason.'
  '\.dropPrimary[[:space:]]*\(|critical|drop_constraint|dropPrimary — Removes primary key constraint|This is extremely dangerous. Verify thoroughly before proceeding.'
  '\.raw[[:space:]]*\([^)]*DROP|high|raw_drop|raw SQL with DROP statement|Review raw SQL carefully. Prefer using Knex schema builder methods.'
  '\.raw[[:space:]]*\([^)]*TRUNCATE|critical|raw_truncate|raw SQL with TRUNCATE statement|Avoid truncating via raw SQL. Use proper delete operations with backups.'
)

# ─── Liquibase Patterns ──────────────────────────────────────────────────────
# Liquibase XML changeset operations

declare -a MIGRATESAFE_LIQUIBASE_PATTERNS=()

MIGRATESAFE_LIQUIBASE_PATTERNS+=(
  '<dropTable[[:space:]]|critical|drop_table|dropTable changeset — Permanently deletes table|Add a precondition to check table is empty. Consider cascadeConstraints=false.'
  '<dropColumn[[:space:]]|high|drop_column|dropColumn changeset — Removes column and data|Remove column usage from code first. Deploy. Then drop column.'
  '<modifyDataType[[:space:]]|high|type_change|modifyDataType changeset — Column type change|Verify data compatibility. Test on production data copy.'
  '<dropIndex[[:space:]]|high|drop_index|dropIndex changeset — Removes database index|Verify query performance is acceptable without this index.'
  '<dropForeignKeyConstraint[[:space:]]|medium|drop_constraint|dropForeignKeyConstraint — Removes FK constraint|Verify application maintains integrity without this constraint.'
  '<dropUniqueConstraint[[:space:]]|medium|drop_constraint|dropUniqueConstraint — Removes unique constraint|Verify application prevents duplicates without this constraint.'
  '<dropPrimaryKey[[:space:]]|critical|drop_constraint|dropPrimaryKey — Removes primary key|This is extremely dangerous. Verify thoroughly.'
  '<addNotNullConstraint[[:space:]]|medium|set_not_null|addNotNullConstraint — May fail if NULLs exist|Provide defaultNullValue attribute to handle existing NULLs.'
  '<renameTable[[:space:]]|high|rename_table|renameTable — Breaks references to old table name|Update all code references first.'
  '<renameColumn[[:space:]]|low|rename_column|renameColumn — Code must use new column name|Update all code references first.'
  '<delete[[:space:]]|medium|delete_data|delete changeset — Deletes data rows|Ensure WHERE clause limits scope. Verify this is not a mass delete.'
)

# ─── Utility: get pattern count by framework ─────────────────────────────────

migratesafe_pattern_count() {
  local framework="${1:-all}"
  case "$framework" in
    sql)        echo "${#MIGRATESAFE_SQL_PATTERNS[@]}" ;;
    rails)      echo "${#MIGRATESAFE_RAILS_PATTERNS[@]}" ;;
    django)     echo "${#MIGRATESAFE_DJANGO_PATTERNS[@]}" ;;
    knex)       echo "${#MIGRATESAFE_KNEX_PATTERNS[@]}" ;;
    liquibase)  echo "${#MIGRATESAFE_LIQUIBASE_PATTERNS[@]}" ;;
    all)
      local total=0
      total=$(( ${#MIGRATESAFE_SQL_PATTERNS[@]} + ${#MIGRATESAFE_RAILS_PATTERNS[@]} + ${#MIGRATESAFE_DJANGO_PATTERNS[@]} + ${#MIGRATESAFE_KNEX_PATTERNS[@]} + ${#MIGRATESAFE_LIQUIBASE_PATTERNS[@]} ))
      echo "$total"
      ;;
  esac
}

# ─── Utility: list patterns by severity ──────────────────────────────────────

migratesafe_list_patterns() {
  local filter_severity="${1:-all}"
  local filter_framework="${2:-all}"

  local -a pattern_sets=()
  case "$filter_framework" in
    sql)       pattern_sets=("SQL") ;;
    rails)     pattern_sets=("RAILS") ;;
    django)    pattern_sets=("DJANGO") ;;
    knex)      pattern_sets=("KNEX") ;;
    liquibase) pattern_sets=("LIQUIBASE") ;;
    all)       pattern_sets=("SQL" "RAILS" "DJANGO" "KNEX" "LIQUIBASE") ;;
  esac

  for set_name in "${pattern_sets[@]}"; do
    local -n patterns_ref="MIGRATESAFE_${set_name}_PATTERNS"
    for entry in "${patterns_ref[@]}"; do
      IFS='|' read -r regex severity category description recommendation <<< "$entry"
      if [[ "$filter_severity" == "all" || "$filter_severity" == "$severity" ]]; then
        printf "%-10s %-15s %-20s %s\n" "$severity" "$set_name" "$category" "$description"
      fi
    done
  done
}

# ─── Utility: severity to numeric level ──────────────────────────────────────

severity_to_risk() {
  case "$1" in
    critical) echo 40 ;;
    high)     echo 25 ;;
    medium)   echo 10 ;;
    low)      echo 5 ;;
    *)        echo 0 ;;
  esac
}

# ─── Utility: get patterns array for a framework ────────────────────────────

get_patterns_for_framework() {
  local framework="$1"
  case "$framework" in
    sql|prisma|flyway) echo "MIGRATESAFE_SQL_PATTERNS" ;;
    rails)             echo "MIGRATESAFE_RAILS_PATTERNS" ;;
    django)            echo "MIGRATESAFE_DJANGO_PATTERNS" ;;
    knex)              echo "MIGRATESAFE_KNEX_PATTERNS" ;;
    liquibase)         echo "MIGRATESAFE_LIQUIBASE_PATTERNS" ;;
    *)                 echo "MIGRATESAFE_SQL_PATTERNS" ;;
  esac
}
