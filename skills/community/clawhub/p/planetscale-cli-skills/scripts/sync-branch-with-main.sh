#!/bin/bash
set -e

# sync-branch-with-main.sh
# Create a fresh branch from main/base to resolve schema drift

show_help() {
  cat << EOF
Usage: $(basename "$0") [OPTIONS]

Create a replacement development branch from the current base branch.

OPTIONS:
  --database <name>       Database name (required)
  --branch <name>         Existing branch with changes to reapply (required)
  --new-branch <name>     Replacement branch to create from base (required)
  --from <source>         Base branch to create from (default: main)
  --org <name>            Organization name (optional; alphanumeric, hyphens, underscores, dots only)
  -h, --help              Show this help message

EXAMPLES:
  # Create a replacement branch from main
  $(basename "$0") --database my-database --branch feature-branch \\
    --new-branch feature-branch-rebased

  # With organization
  $(basename "$0") --database my-db --branch dev-branch \\
    --new-branch dev-branch-rebased --org my-org

WHAT IT DOES:
  PlanetScale does not merge production schema changes into an existing branch.
  To resolve schema conflicts, create a new branch from the current base branch,
  reapply your schema changes, review the diff, and create a new deploy request.
  This script creates that replacement branch and prints the next commands.

EXIT CODES:
  0   Success
  1   Error (missing args, invalid input, pscale command failed)
EOF
}

require_option_value() {
  local option="$1"
  local value="${2-}"
  if [[ -z "$value" ]] || [[ "$value" == --* ]]; then
    echo "❌ Error: $option requires a value"
    echo "Run with --help for usage"
    exit 1
  fi
}

# Validate that a value contains only safe characters for PlanetScale names
validate_safe_name() {
  local value="$1"
  local param="$2"
  if [[ ! "$value" =~ ^[a-zA-Z0-9._-]+$ ]]; then
    echo "❌ Error: $param contains invalid characters. Only alphanumeric, hyphens, underscores, and dots are allowed."
    exit 1
  fi
}

# Parse arguments
DATABASE=""
BRANCH=""
NEW_BRANCH=""
FROM="main"
ORG=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --database)
      require_option_value "$1" "${2-}"
      DATABASE="$2"
      shift 2
      ;;
    --branch)
      require_option_value "$1" "${2-}"
      BRANCH="$2"
      shift 2
      ;;
    --new-branch)
      require_option_value "$1" "${2-}"
      NEW_BRANCH="$2"
      shift 2
      ;;
    --from)
      require_option_value "$1" "${2-}"
      FROM="$2"
      shift 2
      ;;
    --org)
      require_option_value "$1" "${2-}"
      ORG="$2"
      shift 2
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo "❌ Unknown option: $1"
      echo "Run with --help for usage"
      exit 1
      ;;
  esac
done

# Validate required arguments
if [[ -z "$DATABASE" ]] || [[ -z "$BRANCH" ]] || [[ -z "$NEW_BRANCH" ]]; then
  echo "❌ Error: --database, --branch, and --new-branch are required"
  echo "Run with --help for usage"
  exit 1
fi

if [[ "$BRANCH" == "$NEW_BRANCH" ]]; then
  echo "❌ Error: --new-branch must be different from --branch"
  exit 1
fi

# Validate inputs to prevent shell injection
validate_safe_name "$DATABASE" "--database"
validate_safe_name "$BRANCH" "--branch"
validate_safe_name "$NEW_BRANCH" "--new-branch"
validate_safe_name "$FROM" "--from"
[[ -n "$ORG" ]] && validate_safe_name "$ORG" "--org"

# Build org args array (safe: no eval, no string interpolation into commands)
ORG_ARGS=()
[[ -n "$ORG" ]] && ORG_ARGS=(--org "$ORG")

echo "🔄 Creating replacement branch from base..."
echo "  Database: $DATABASE"
echo "  Existing branch: $BRANCH"
echo "  New branch: $NEW_BRANCH"
echo "  From: $FROM"
[[ -n "$ORG" ]] && echo "  Org: $ORG"
echo ""

# Create a fresh branch from the current base schema. PlanetScale documents this
# re-branch workflow for resolving schema conflicts with the base branch.
pscale branch create "$DATABASE" "$NEW_BRANCH" --from "$FROM" "${ORG_ARGS[@]}"

echo ""
echo "✅ Replacement branch created!"
echo ""
echo "Next steps:"
echo "  1. Reapply the schema changes from $BRANCH onto $NEW_BRANCH."
echo ""
echo "  2. Verify diff against $FROM:"
echo "     pscale branch diff $DATABASE $NEW_BRANCH ${ORG_ARGS[*]}"
echo ""
echo "  3. Create a new deploy request:"
echo "     pscale deploy-request create $DATABASE $NEW_BRANCH ${ORG_ARGS[*]}"
