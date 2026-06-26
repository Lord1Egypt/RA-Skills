#!/usr/bin/env bash
set -euo pipefail

REPO_NAME="openclaw-backup"
OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
BACKUP_DIR="${BACKUP_DIR:-$OPENCLAW_DIR/backups}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ARCHIVE_PATH=""
MANIFEST_PATH=""
SECRETS_PATH=""

usage() {
  cat <<'EOF'
Usage: push-to-github.sh [repo-name] --archive /path/to/openclaw-backup-YYYY-MM-DD.tar.gz --manifest /path/to/manifest.json [--secrets /path/to/openclaw-secrets-YYYY-MM-DD.tar.gz.age]

Push an operational OpenClaw backup set to a private GitHub repo using gh.
Refuses to push any unencrypted secrets archive.
EOF
}

warn() { printf 'WARNING: %s\n' "$*" >&2; }
info() { printf '%s\n' "$*"; }
die() { warn "$*"; exit 1; }

POSITIONAL=()
while [ "$#" -gt 0 ]; do
  case "$1" in
    --archive)
      [ "$#" -ge 2 ] || die "--archive requires a path"
      ARCHIVE_PATH="$2"
      shift 2
      ;;
    --manifest)
      [ "$#" -ge 2 ] || die "--manifest requires a path"
      MANIFEST_PATH="$2"
      shift 2
      ;;
    --secrets)
      [ "$#" -ge 2 ] || die "--secrets requires a path"
      SECRETS_PATH="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --*)
      die "Unknown argument: $1"
      ;;
    *)
      POSITIONAL+=("$1")
      shift
      ;;
  esac
done

if [ "${#POSITIONAL[@]}" -gt 1 ]; then
  die "Only one repo name may be provided"
elif [ "${#POSITIONAL[@]}" -eq 1 ]; then
  REPO_NAME="${POSITIONAL[0]}"
fi

command -v gh >/dev/null 2>&1 || die "gh CLI is required"
command -v python3 >/dev/null 2>&1 || die "python3 is required"
gh auth status >/dev/null 2>&1 || die "gh CLI is not authenticated"

if [ -z "$ARCHIVE_PATH" ] || [ -z "$MANIFEST_PATH" ]; then
  LATEST_MANIFEST="$(find "$BACKUP_DIR" -type f -name 'manifest.json' | sort | tail -n 1)"
  if [ -n "$LATEST_MANIFEST" ] && [ -z "$MANIFEST_PATH" ]; then
    MANIFEST_PATH="$LATEST_MANIFEST"
  fi
  if [ -n "$MANIFEST_PATH" ] && [ -z "$ARCHIVE_PATH" ]; then
    ARCHIVE_PATH="$(python3 - "$MANIFEST_PATH" <<'PY'
import json, os, sys
path = sys.argv[1]
base = os.path.dirname(path)
manifest = json.load(open(path, encoding='utf-8'))
print(os.path.join(base, manifest['archives']['operational']['file']))
PY
)"
  fi
fi

[ -n "$ARCHIVE_PATH" ] || die "No operational archive found"
[ -n "$MANIFEST_PATH" ] || die "No manifest found"
[ -f "$ARCHIVE_PATH" ] || die "Archive not found: $ARCHIVE_PATH"
[ -f "$MANIFEST_PATH" ] || die "Manifest not found: $MANIFEST_PATH"

if [ -n "$SECRETS_PATH" ]; then
  [ -f "$SECRETS_PATH" ] || die "Secrets archive not found: $SECRETS_PATH"
  [[ "$SECRETS_PATH" == *.age ]] || die "Refusing to push unencrypted secrets archive: $SECRETS_PATH"
else
  EXPECTED_SECRETS="$(python3 - "$MANIFEST_PATH" <<'PY'
import json, os, sys
manifest = json.load(open(sys.argv[1], encoding='utf-8'))
name = manifest.get('archives', {}).get('secrets', {}).get('file') or ''
base = os.path.dirname(sys.argv[1])
print(os.path.join(base, name) if name else '')
PY
)"
  if [ -n "$EXPECTED_SECRETS" ] && [ -f "$EXPECTED_SECRETS" ]; then
    SECRETS_PATH="$EXPECTED_SECRETS"
    [[ "$SECRETS_PATH" == *.age ]] || die "Refusing to push unencrypted secrets archive: $SECRETS_PATH"
  fi
fi

OWNER="$(gh api user --jq .login)"
REMOTE="https://github.com/$OWNER/$REPO_NAME.git"
WORK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/openclaw-github.XXXXXX")"
trap 'rm -rf "$WORK_DIR"' EXIT

if gh repo view "$OWNER/$REPO_NAME" >/dev/null 2>&1; then
  info "Using existing repo: $OWNER/$REPO_NAME"
  gh repo clone "$OWNER/$REPO_NAME" "$WORK_DIR/$REPO_NAME" >/dev/null
else
  info "Creating private repo: $OWNER/$REPO_NAME"
  gh repo create "$REPO_NAME" --private --clone --description "OpenClaw backup archives" "$WORK_DIR/$REPO_NAME" >/dev/null
fi

REPO_DIR="$WORK_DIR/$REPO_NAME"
mkdir -p "$REPO_DIR/archives"

if [ ! -f "$REPO_DIR/.gitignore" ]; then
  cp "$SKILL_DIR/templates/.gitignore" "$REPO_DIR/.gitignore"
fi

cp "$ARCHIVE_PATH" "$REPO_DIR/archives/$(basename "$ARCHIVE_PATH")"
cp "$MANIFEST_PATH" "$REPO_DIR/archives/$(basename "$MANIFEST_PATH")"
if [ -n "$SECRETS_PATH" ]; then
  cp "$SECRETS_PATH" "$REPO_DIR/archives/$(basename "$SECRETS_PATH")"
fi

(
  cd "$REPO_DIR"
  git add .gitignore archives/*
  if git diff --cached --quiet; then
    info "No changes to commit."
  else
    git commit -m "Backup $(basename "$ARCHIVE_PATH")" >/dev/null
    git push origin HEAD >/dev/null
    info "Pushed backup to $REMOTE"
  fi
)
