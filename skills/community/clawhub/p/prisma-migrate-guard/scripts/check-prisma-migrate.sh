#!/usr/bin/env bash
set -euo pipefail

SCHEMA_PATH="${PRISMA_SCHEMA_PATH:-prisma/schema.prisma}"
DB_ENV_KEY="${PRISMA_MIGRATE_DB_URL_ENV:-DATABASE_URL}"
ALLOW_UNAPPLIED="${PRISMA_MIGRATE_GUARD_ALLOW_UNAPPLIED:-0}"
ALLOW_DRIFT="${PRISMA_MIGRATE_GUARD_ALLOW_DRIFT:-0}"

fail() {
  echo "FAIL: $1" >&2
  exit 1
}

warn() {
  echo "WARN: $1"
}

pass() {
  echo "PASS: $1"
}

command -v npx >/dev/null 2>&1 || fail "npx not found"
command -v node >/dev/null 2>&1 || fail "node not found"

if [[ ! -f "$SCHEMA_PATH" ]]; then
  fail "schema file not found at '$SCHEMA_PATH' (set PRISMA_SCHEMA_PATH)"
fi

if [[ -z "${!DB_ENV_KEY:-}" ]]; then
  fail "${DB_ENV_KEY} is not set"
fi

if [[ "${!DB_ENV_KEY}" =~ localhost|127\.0\.0\.1|template1|\$\{|\$[A-Z_] ]]; then
  fail "${DB_ENV_KEY} looks like placeholder/local value"
fi

STATUS_OUTPUT=""
if ! STATUS_OUTPUT="$(npx --yes prisma migrate status --schema "$SCHEMA_PATH" 2>&1)"; then
  echo "$STATUS_OUTPUT"
  fail "prisma migrate status failed"
fi

echo "$STATUS_OUTPUT"

normalized="$(echo "$STATUS_OUTPUT" | tr '[:upper:]' '[:lower:]')"

if echo "$normalized" | grep -Eq "failed migration|has failed"; then
  fail "failed migration detected"
fi

if echo "$normalized" | grep -Eq "drift detected|drift"; then
  if [[ "$ALLOW_DRIFT" == "1" ]]; then
    warn "drift detected but allowed by PRISMA_MIGRATE_GUARD_ALLOW_DRIFT=1"
  else
    fail "schema drift detected"
  fi
fi

if echo "$normalized" | grep -Eq "following migration\(s\) have not yet been applied|not yet applied"; then
  if [[ "$ALLOW_UNAPPLIED" == "1" ]]; then
    warn "unapplied migration files detected but allowed by PRISMA_MIGRATE_GUARD_ALLOW_UNAPPLIED=1"
  else
    fail "unapplied migration files detected"
  fi
fi

if echo "$normalized" | grep -Eq "no migration table|_prisma_migrations"; then
  warn "migration history table not detected yet; verify this is expected for fresh DBs"
fi

pass "prisma migration state is deploy-safe"
