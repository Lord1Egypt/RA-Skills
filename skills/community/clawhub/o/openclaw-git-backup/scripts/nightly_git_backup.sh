#!/usr/bin/env bash
set -euo pipefail

repo="${1:-${BACKUP_REPO:-$(pwd)}}"
remote="${BACKUP_REMOTE:-origin}"
branch_override="${BACKUP_BRANCH:-}"
timezone="${BACKUP_TZ:-UTC}"
author_name="${BACKUP_AUTHOR_NAME:-OpenClaw Backup}"
author_email="${BACKUP_AUTHOR_EMAIL:-backup@local}"
exclude_csv="${BACKUP_EXCLUDES:-}"

if [[ ! -d "$repo/.git" ]]; then
  echo "ERROR: not a git repo: $repo" >&2
  exit 1
fi

cd "$repo"

trim() {
  local s="$1"
  s="${s#${s%%[![:space:]]*}}"
  s="${s%${s##*[![:space:]]}}"
  printf '%s' "$s"
}

stage_changes() {
  local -a exclude_args=()
  if [[ -n "$exclude_csv" ]]; then
    IFS=',' read -r -a raw_excludes <<< "$exclude_csv"
    for item in "${raw_excludes[@]}"; do
      item="$(trim "$item")"
      [[ -z "$item" ]] && continue
      exclude_args+=(":(exclude)$item")
    done
  fi

  git add -A -- . "${exclude_args[@]}"
}

print_section() {
  local title="$1"
  local count="$2"
  local lines="${3:-}"

  printf '%s(%s)\n' "$title" "$count"
  if [[ -n "$lines" ]]; then
    printf '%s\n' "$lines"
  else
    echo "- none"
  fi
}

stage_changes

did_commit=0
added_count=0
modified_count=0
deleted_count=0
renamed_count=0
status_file=""
body_file=""
trap '[[ -n "$status_file" ]] && rm -f "$status_file"; [[ -n "$body_file" ]] && rm -f "$body_file"' EXIT

if ! git diff --cached --quiet; then
  status_file="$(mktemp)"
  body_file="$(mktemp)"
  git diff --cached --name-status --find-renames > "$status_file"

  added_count=$(awk -F '\t' '$1=="A"{c++} END{print c+0}' "$status_file")
  modified_count=$(awk -F '\t' '$1=="M"{c++} END{print c+0}' "$status_file")
  deleted_count=$(awk -F '\t' '$1=="D"{c++} END{print c+0}' "$status_file")
  renamed_count=$(awk -F '\t' '$1 ~ /^R[0-9]*$/{c++} END{print c+0}' "$status_file")

  added_lines=$(awk -F '\t' '$1=="A"{print "- "$2}' "$status_file")
  modified_lines=$(awk -F '\t' '$1=="M"{print "- "$2}' "$status_file")
  deleted_lines=$(awk -F '\t' '$1=="D"{print "- "$2}' "$status_file")
  renamed_lines=$(awk -F '\t' '$1 ~ /^R[0-9]*$/{print "- "$2" -> "$3}' "$status_file")

  {
    print_section "Added" "$added_count" "$added_lines"
    echo
    print_section "Modified" "$modified_count" "$modified_lines"
    echo
    print_section "Deleted" "$deleted_count" "$deleted_lines"
    if [[ "$renamed_count" -gt 0 ]]; then
      echo
      print_section "Renamed" "$renamed_count" "$renamed_lines"
    fi
  } > "$body_file"

  subject="backup: snapshot $(TZ="$timezone" date "+%F %T %z") | +${added_count} ~${modified_count} -${deleted_count}"
  GIT_AUTHOR_NAME="$author_name" \
  GIT_AUTHOR_EMAIL="$author_email" \
  GIT_COMMITTER_NAME="$author_name" \
  GIT_COMMITTER_EMAIL="$author_email" \
    git commit -m "$subject" -m "$(cat "$body_file")"
  did_commit=1
fi

branch="$branch_override"
if [[ -z "$branch" ]]; then
  branch="$(git rev-parse --abbrev-ref HEAD)"
  if [[ -z "$branch" || "$branch" == "HEAD" ]]; then
    branch="main"
  fi
fi

git push --porcelain "$remote" "HEAD:${branch}"

echo "DID_COMMIT=$did_commit"
echo "HEAD=$(git rev-parse --short HEAD)"
echo "BRANCH=$branch"
git status --short --branch
