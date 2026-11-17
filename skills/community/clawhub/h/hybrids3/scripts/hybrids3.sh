#!/usr/bin/env bash
# Thin curl wrapper for the hybrids3 plain HTTP API: put / get / list / delete
# objects and list buckets against a running instance. S3-SDK and MCP callers
# don't need this; it exists so shell users don't hand-write Bearer headers.
#
# Usage:
#   hybrids3.sh put     <bucket> <key> <local-file> [content-type]
#   hybrids3.sh get     <bucket> <key> [out-file]        # object bytes → stdout if out-file omitted
#   hybrids3.sh info    <bucket> <key>                   # HEAD: metadata headers only
#   hybrids3.sh list    <bucket> [prefix] [max-keys]
#   hybrids3.sh delete  <bucket> <key>
#   hybrids3.sh buckets                                  # list buckets (master key → all)
#   hybrids3.sh presign <bucket> <key> [GET|PUT] [expires-seconds]
#   hybrids3.sh health
#
# Environment:
#   HYBRIDS3_URL   Base URL of the instance (default: http://localhost:8080).
#                  Include any reverse-proxy path prefix, e.g. http://host/storage.
#   HYBRIDS3_KEY   Bearer token: a bucket's private key, or the master key.
#                  Required for writes, private-bucket reads, presign, and the
#                  buckets command. Public-bucket reads work without it.
#   LOG_FILE       Where diagnostic (stderr) log lines are tee'd (default: /tmp/hybrids3.log).
#   DEBUG          Set non-empty to emit DEBUG log lines.
#
# Output contract: object bytes / JSON responses go to stdout (pipeable);
# all diagnostics go to stderr as JSON. Exit 0 on HTTP 2xx, 1 on non-2xx
# (response body printed to stderr), 2 on usage/arg errors.

set -euo pipefail
trap 'log ERROR "command failed exit=$? line=${LINENO}"' ERR

readonly DEFAULT_URL="http://localhost:8080"
readonly EXIT_USAGE=2
readonly EXIT_HTTP_FAIL=1

LOG_FILE="${LOG_FILE:-/tmp/$(basename "$0" .sh).log}"
readonly LOG_FILE

log() {
	local level="$1"
	shift
	[[ "$level" == "DEBUG" && -z "${DEBUG:-}" ]] && return 0
	local ts file line func
	ts="$(date -u '+%Y-%m-%dT%H:%M:%S.%3NZ')"
	file="${BASH_SOURCE[1]##*/}"
	line="${BASH_LINENO[0]}"
	func="${FUNCNAME[1]:-main}"
	printf '{"time":"%s","level":"%s","file":"%s","line":%d,"func":"%s","msg":"%s"}\n' \
		"$ts" "$level" "$file" "$line" "$func" "$*" | tee -a "$LOG_FILE" >&2
}

die() {
	log ERROR "$*"
	exit "$EXIT_USAGE"
}

usage() {
	# Reproduce the header comment block (lines 2-30) as help text.
	sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'
	exit "$EXIT_USAGE"
}

HYBRIDS3_URL="${HYBRIDS3_URL:-$DEFAULT_URL}"
HYBRIDS3_URL="${HYBRIDS3_URL%/}"
readonly HYBRIDS3_URL

auth_args=()
if [[ -n "${HYBRIDS3_KEY:-}" ]]; then
	# Value comes from env and is never echoed; it does not enter any log line.
	auth_args=(-H "Authorization: Bearer ${HYBRIDS3_KEY}")
fi

# Run a curl request; on 2xx print the body to stdout and return 0. On non-2xx,
# print the body to stderr and return EXIT_HTTP_FAIL so the caller/trap surfaces it.
# Args: <curl args...> (the URL last).
request() {
	local body code
	body="$(mktemp)"
	# shellcheck disable=SC2064  # expand $body now so the trap removes THIS temp file
	trap "rm -f '$body'" RETURN
	code="$(curl -s -o "$body" -w '%{http_code}' "$@" || echo 000)"
	if [[ "$code" =~ ^2[0-9][0-9]$ ]]; then
		cat "$body"
		log DEBUG "request ok http=$code"
		return 0
	fi
	log ERROR "request failed http=$code"
	cat "$body" >&2 || true
	printf '\n' >&2
	return "$EXIT_HTTP_FAIL"
}

require_key() {
	[[ -n "${HYBRIDS3_KEY:-}" ]] || die "$1 requires HYBRIDS3_KEY"
}

cmd_put() {
	[[ $# -ge 3 ]] || die "put needs: <bucket> <key> <local-file> [content-type]"
	require_key put
	local bucket="$1" key="$2" file="$3" ctype="${4:-}"
	[[ -f "$file" ]] || die "local file not found: $file"
	local ct_args=()
	[[ -n "$ctype" ]] && ct_args=(-H "Content-Type: ${ctype}")
	log INFO "put bucket=$bucket key=$key file=$file"
	request -X PUT "${auth_args[@]}" "${ct_args[@]}" \
		--data-binary @"$file" "$HYBRIDS3_URL/$bucket/$key"
}

cmd_get() {
	[[ $# -ge 2 ]] || die "get needs: <bucket> <key> [out-file]"
	local bucket="$1" key="$2" out="${3:-}"
	log INFO "get bucket=$bucket key=$key out=${out:-<stdout>}"
	if [[ -z "$out" ]]; then
		request "${auth_args[@]}" "$HYBRIDS3_URL/$bucket/$key"
		return
	fi
	local code
	code="$(curl -s -o "$out" -w '%{http_code}' "${auth_args[@]}" \
		"$HYBRIDS3_URL/$bucket/$key" || echo 000)"
	if [[ ! "$code" =~ ^2[0-9][0-9]$ ]]; then
		rm -f "$out"
		die "download failed http=$code"
	fi
	log INFO "wrote out=$out"
}

cmd_info() {
	[[ $# -ge 2 ]] || die "info needs: <bucket> <key>"
	log INFO "info bucket=$1 key=$2"
	# HEAD → headers are the payload the user wants; emit to stdout.
	curl -sI "${auth_args[@]}" "$HYBRIDS3_URL/$1/$2"
}

cmd_list() {
	[[ $# -ge 1 ]] || die "list needs: <bucket> [prefix] [max-keys]"
	local bucket="$1" prefix="${2:-}" maxkeys="${3:-}" q=""
	[[ -n "$prefix" ]] && q="prefix=${prefix}"
	[[ -n "$maxkeys" ]] && q="${q:+$q&}max-keys=${maxkeys}"
	log INFO "list bucket=$bucket prefix=${prefix:-<none>}"
	request "${auth_args[@]}" "$HYBRIDS3_URL/$bucket${q:+?$q}"
}

cmd_delete() {
	[[ $# -ge 2 ]] || die "delete needs: <bucket> <key>"
	require_key delete
	log INFO "delete bucket=$1 key=$2"
	request -X DELETE "${auth_args[@]}" "$HYBRIDS3_URL/$1/$2"
}

cmd_buckets() {
	require_key buckets
	log INFO "list buckets"
	request "${auth_args[@]}" "$HYBRIDS3_URL/"
}

cmd_presign() {
	[[ $# -ge 2 ]] || die "presign needs: <bucket> <key> [GET|PUT] [expires-seconds]"
	require_key presign
	local bucket="$1" key="$2" method="${3:-GET}" expires="${4:-3600}"
	log INFO "presign bucket=$bucket key=$key method=$method expires=$expires"
	request -X POST "${auth_args[@]}" \
		"$HYBRIDS3_URL/presign/$bucket/$key?method=${method}&expires=${expires}"
}

cmd_health() {
	log INFO "health check url=$HYBRIDS3_URL"
	request "$HYBRIDS3_URL/health"
}

main() {
	local cmd="${1:-}"
	[[ -n "$cmd" ]] || usage
	shift || true

	case "$cmd" in
	put) cmd_put "$@" ;;
	get) cmd_get "$@" ;;
	info) cmd_info "$@" ;;
	list) cmd_list "$@" ;;
	delete) cmd_delete "$@" ;;
	buckets) cmd_buckets "$@" ;;
	presign) cmd_presign "$@" ;;
	health) cmd_health "$@" ;;
	-h | --help | help) usage ;;
	*) die "unknown command: $cmd (try: put get info list delete buckets presign health)" ;;
	esac
}

main "$@"
