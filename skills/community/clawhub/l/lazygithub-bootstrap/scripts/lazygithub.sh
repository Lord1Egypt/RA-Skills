#!/usr/bin/env bash
set -euo pipefail

NAME=""
DESCRIPTION=""
HOMEPAGE=""
TOPICS=""
VISIBILITY="public"
ADD_LOCAL_README="true"

usage() {
  cat <<'EOF'
Usage:
  ./lazygithub.sh --name NAME --description TEXT [options]

Options:
  --name NAME             Repository name
  --description TEXT      Repository description
  --homepage URL          Homepage / website URL
  --topics a,b,c          Comma-separated GitHub topics
  --public                Create public repo (default)
  --private               Create private repo
  --no-readme             Skip local README scaffold
  -h, --help              Show help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)
      NAME="$2"
      shift 2
      ;;
    --description)
      DESCRIPTION="$2"
      shift 2
      ;;
    --homepage)
      HOMEPAGE="$2"
      shift 2
      ;;
    --topics)
      TOPICS="$2"
      shift 2
      ;;
    --public)
      VISIBILITY="public"
      shift
      ;;
    --private)
      VISIBILITY="private"
      shift
      ;;
    --no-readme)
      ADD_LOCAL_README="false"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$NAME" ]]; then
  echo "--name is required" >&2
  exit 1
fi

if [[ -z "$DESCRIPTION" ]]; then
  echo "--description is required" >&2
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "gh is not installed." >&2
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "gh is not authenticated. Run: gh auth login" >&2
  exit 1
fi

if [[ "$ADD_LOCAL_README" == "true" ]]; then
  mkdir -p "$NAME"
  if [[ ! -f "$NAME/README.md" ]]; then
    cat > "$NAME/README.md" <<EOF
# $NAME

$DESCRIPTION
EOF
  fi

  if [[ ! -d "$NAME/.git" ]]; then
    git -C "$NAME" init
    git -C "$NAME" add README.md
    git -C "$NAME" commit -m "chore: initial commit"
  fi
fi

CREATE_ARGS=(repo create "$NAME" "--$VISIBILITY" --description "$DESCRIPTION")

if [[ -n "$HOMEPAGE" ]]; then
  CREATE_ARGS+=(--homepage "$HOMEPAGE")
fi

if [[ "$ADD_LOCAL_README" == "true" ]]; then
  CREATE_ARGS+=(--source "$NAME" --remote origin --push)
fi

gh "${CREATE_ARGS[@]}"

if [[ -n "$TOPICS" ]]; then
  IFS=',' read -r -a TOPIC_ARRAY <<< "$TOPICS"
  EDIT_ARGS=(repo edit "$NAME")
  for topic in "${TOPIC_ARRAY[@]}"; do
    trimmed="$(echo "$topic" | xargs)"
    if [[ -n "$trimmed" ]]; then
      EDIT_ARGS+=(--add-topic "$trimmed")
    fi
  done
  gh "${EDIT_ARGS[@]}"
fi

echo
printf 'Done: %s\n' "$NAME"
printf 'Description: %s\n' "$DESCRIPTION"
[[ -n "$HOMEPAGE" ]] && printf 'Homepage: %s\n' "$HOMEPAGE"
[[ -n "$TOPICS" ]] && printf 'Topics: %s\n' "$TOPICS"
