#!/usr/bin/env bash

set -u

usage() {
  cat >&2 <<USAGE
Usage:
  $0 METHOD /path [json-body]
  $0 AUTH /path json-body
  $0 UPLOAD /path file context

Methods: GET, POST, PUT, PATCH, DELETE

Environment:
  HOF_API_URL       API origin including the /api prefix.
  HOF_TOKEN         Optional bearer token; takes precedence over HOF_TOKEN_FILE.
  HOF_TOKEN_FILE    Optional private token file used for persistent agent auth.
USAGE
  exit 64
}

[[ $# -ge 2 ]] || usage

method=$(printf '%s' "$1" | tr '[:lower:]' '[:upper:]')
path=$2

case "$method" in
  GET | POST | PUT | PATCH | DELETE)
    [[ $# -ge 2 && $# -le 3 ]] || usage
    ;;
  AUTH)
    [[ $# -eq 3 ]] || usage
    ;;
  UPLOAD)
    [[ $# -eq 4 ]] || usage
    ;;
  *) usage ;;
esac

if [[ -z ${HOF_API_URL:-} ]]; then
  printf 'HOF_API_URL is required.\n' >&2
  exit 64
fi

if [[ $path != /* ]]; then
  printf 'API path must begin with /.\n' >&2
  exit 64
fi

base_url=${HOF_API_URL%/}
auth_config=''
response_file=''

token=${HOF_TOKEN:-}
if [[ -z $token && -n ${HOF_TOKEN_FILE:-} && -f $HOF_TOKEN_FILE ]]; then
  token=$(<"$HOF_TOKEN_FILE")
fi

cleanup() {
  if [[ -n $auth_config && -f $auth_config ]]; then
    rm -f -- "$auth_config"
  fi

  if [[ -n $response_file && -f $response_file ]]; then
    rm -f -- "$response_file"
  fi
}
trap cleanup EXIT

curl_args=(
  --silent
  --show-error
  --fail-with-body
  --header 'Accept: application/json'
)

if [[ $method != AUTH && -n $token ]]; then
  auth_config=$(mktemp)
  chmod 600 "$auth_config"
  printf 'header = "Authorization: Bearer %s"\n' "$token" >"$auth_config"
  curl_args+=(--config "$auth_config")
fi

case "$method" in
  AUTH)
    if [[ -z ${HOF_TOKEN_FILE:-} ]]; then
      printf 'HOF_TOKEN_FILE is required for AUTH so the returned token can be persisted securely.\n' >&2
      exit 64
    fi

    body=$3
    response_file=$(mktemp)
    chmod 600 "$response_file"

    if ! curl "${curl_args[@]}" \
      --request POST \
      --header 'Content-Type: application/json' \
      --data-raw "$body" \
      --output "$response_file" \
      "${base_url}${path}"; then
      cat "$response_file"
      exit 22
    fi

    mkdir -p -- "$(dirname -- "$HOF_TOKEN_FILE")"

    node - "$response_file" "$HOF_TOKEN_FILE" <<'NODE'
const fs = require('node:fs')

const [, , responsePath, tokenPath] = process.argv
const payload = JSON.parse(fs.readFileSync(responsePath, 'utf8'))

if (typeof payload.token !== 'string' || payload.token.length === 0) {
  process.stdout.write(`${JSON.stringify(payload)}\n`)
  process.stderr.write('Authentication response did not contain a top-level token.\n')
  process.exit(65)
}

fs.writeFileSync(tokenPath, `${payload.token}\n`, { mode: 0o600 })
fs.chmodSync(tokenPath, 0o600)

delete payload.token
payload.token_saved = true
process.stdout.write(`${JSON.stringify(payload)}\n`)
NODE
    node_status=$?
    if [[ $node_status -ne 0 ]]; then
      exit "$node_status"
    fi
    ;;

  UPLOAD)
    file=$3
    context=$4

    if [[ ! -f $file ]]; then
      printf 'Upload file does not exist: %s\n' "$file" >&2
      exit 66
    fi

    case "$context" in
      post | status) ;;
      *)
        printf 'Upload context must be post or status.\n' >&2
        exit 64
        ;;
    esac

    curl "${curl_args[@]}" \
      --request POST \
      --form "file=@${file}" \
      --form "context=${context}" \
      "${base_url}${path}"
    ;;

  *)
    request_args=(--request "$method")

    if [[ $# -eq 3 ]]; then
      request_args+=(--header 'Content-Type: application/json' --data-raw "$3")
    fi

    curl "${curl_args[@]}" "${request_args[@]}" "${base_url}${path}"
    ;;
esac
