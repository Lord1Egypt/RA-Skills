# shellcheck shell=bash
# Shared helpers for the Open Agent Guide batch scripts. Source it, don't run it:
#   . "$(dirname "$0")/oag-common.sh"
#
# Requires: bash, curl, jq. Reads $OAG_TOKEN (bearer, prefix oag_) and
# $OAG_BASE_URL (defaults to https://www.openagentguide.com).
: "${OAG_BASE_URL:=https://www.openagentguide.com}"

# Submission mutations are throttled at 20/min + a 5/second burst. Pausing ~3.5s
# between mutating calls keeps a batch under the per-minute ceiling with headroom
# for the automatic retries below; reads are cheaper (120/min) but share the pace.
: "${OAG_MUTATION_PACE_SECONDS:=3.5}"

# Max attempts for 429 back-off and transient validation failures.
: "${OAG_MAX_ATTEMPTS:=5}"
: "${OAG_REQUEST_TIMEOUT:=45}"

# Output variables: oag_api sets these for the caller to read AFTER the call.
# oag_api returns its results through shell globals, so callers must invoke it
# directly — never in a command-substitution subshell (`resp="$(oag_api ...)"`),
# whose child shell discards the assignments and leaves the status empty (the
# "HTTP ?" bug this pair of variables fixes). Read $OAG_LAST_STATUS and
# $OAG_LAST_BODY on the following line instead.
export OAG_LAST_STATUS=""
export OAG_LAST_BODY=""

# Output variable: oag_preflight_urls sets this to the count of redirecting URLs
# for the caller (oag-validate-batch.sh) to gate its exit code on.
export OAG_PREFLIGHT_REDIRECTS=""

oag_require_token() {
  if [ -z "${OAG_TOKEN:-}" ]; then
    echo "OAG_TOKEN is not set. Export your oag_ bearer token first." >&2
    exit 1
  fi
}

# oag_api METHOD PATH [JSON_BODY]
#
# Issues one authenticated request against $OAG_BASE_URL. On a 429 it waits and
# retries up to $OAG_MAX_ATTEMPTS — honoring Retry-After if present, else pausing
# $OAG_MUTATION_PACE_SECONDS. API throttles send integer Retry-After seconds.
# This helper paces only this process; coordinate other workers separately. Always
# returns 0: the caller reads the outcome from $OAG_LAST_STATUS and $OAG_LAST_BODY
# — a 4xx/5xx body is still captured so the caller can inspect the error envelope
# ({ "code", "detail" } or, on the public API, { "errors": {…} }). A transport
# failure surfaces as $OAG_LAST_STATUS "000" (curl's code for no response), which
# no success branch treats as OK.
oag_api() {
  local method path body attempt tmp_headers resp status retry_after wait_s curl_status
  method="$1"
  path="$2"
  body="${3:-}"
  attempt=1

  while :; do
    tmp_headers="$(mktemp)"
    # Curl can retain a 2xx status after timing out mid-body. Preserve its exit
    # code so a partial response never passes the caller's success guard.
    curl_status=0
    if [ -n "$body" ]; then
      resp="$(
        printf '%s' "$body" | curl -sS --max-time "$OAG_REQUEST_TIMEOUT" -X "$method" "$OAG_BASE_URL$path" \
          -D "$tmp_headers" \
          -w '\n%{http_code}' \
          -H "Authorization: Bearer ${OAG_TOKEN}" \
          -H "Content-Type: application/json" \
          --data-binary @-
      )" || curl_status=$?
    else
      resp="$(
        curl -sS --max-time "$OAG_REQUEST_TIMEOUT" -X "$method" "$OAG_BASE_URL$path" \
          -D "$tmp_headers" \
          -w '\n%{http_code}' \
          -H "Authorization: Bearer ${OAG_TOKEN}"
      )" || curl_status=$?
    fi

    # Read the status from curl's -w '%{http_code}', appended as the final line of
    # stdout. It is curl's own view of the response code — reliable across HTTP
    # versions and proxies — whereas parsing the -D header dump returned an empty
    # status in some environments. Split the trailing status line back off the
    # body (append is exactly "\n<code>", so cut on the last newline). The -D dump
    # is kept only for Retry-After, which -w cannot portably surface on older curl.
    status="${resp##*$'\n'}"
    resp="${resp%$'\n'*}"
    retry_after="$(awk 'tolower($1) ~ /^retry-after:/ {print $2}' "$tmp_headers" | tr -d '\r')"
    rm -f "$tmp_headers"
    if [ "$curl_status" -ne 0 ]; then
      status="000"
    fi
    OAG_LAST_STATUS="$status"

    # Validation has no write side effects, so transport/5xx retries are safe.
    if [ "$method" = "POST" ] && [ "$path" = "/api/v1/submissions/validate/" ] \
      && { [ "$status" = "000" ] || [[ "$status" = 5?? ]]; } \
      && [ "$attempt" -lt "$OAG_MAX_ATTEMPTS" ]; then
      echo "HTTP $status on validation; retrying (attempt $attempt/$OAG_MAX_ATTEMPTS)" >&2
      oag_pace
      attempt=$((attempt + 1))
      continue
    fi

    # A 429 is usually the transient throttle, so retrying clears it. The one 429
    # that is NOT transient is the 25-open-submission cap on POST /submissions/ —
    # retrying won't help until reviews drain. Bulk-submitter accounts are exempt
    # from that cap and are the intended path for large batches (see the doc).
    if [ "$status" = "429" ] && [ "$attempt" -lt "$OAG_MAX_ATTEMPTS" ]; then
      wait_s="${retry_after:-$OAG_MUTATION_PACE_SECONDS}"
      echo "429 rate-limited on $method $path; waiting ${wait_s}s (attempt $attempt/$OAG_MAX_ATTEMPTS)" >&2
      sleep "$wait_s"
      attempt=$((attempt + 1))
      continue
    fi

    OAG_LAST_BODY="$resp"
    return 0
  done
}

# Pause between mutating calls to stay under the burst/minute limits.
oag_pace() {
  sleep "$OAG_MUTATION_PACE_SECONDS"
}

# Error responses can be HTML or plain text, including exhausted 429 retries.
oag_error_detail() {
  printf '%s' "$OAG_LAST_BODY" | jq -erc \
    '.detail // .conflict_type // .errors // "unknown error"' 2>/dev/null \
    || printf '%s\n' "${OAG_LAST_BODY:-empty response}"
}

# oag_preflight_urls BATCH_FILE
#
# Probe every bare-URL string value in the batch — the pointer and affordance
# URLs (`url`, `documentation_url`, `source_code_url`, `pricing_url`,
# `program_url`, and the nested mcp_servers / developer_kits /
# command_line_interfaces / agent_skills URLs) — for 3xx redirects WITHOUT
# following them. The submission-pipeline fetcher does not follow redirects, so a
# URL a populator "verified" with `curl -L` that 301s to a different path leaves
# the fetcher with a 404 body — closing the submission on a URL the populator
# just saw working. That was the single highest-yield populator trap in the
# 2026-10-02 enrich run. Surfacing the redirect here, with the canonical target,
# turns a wasted submit->review cycle into a one-line pre-submit fix.
#
# We report `%{redirect_url}`, not `%{url_effective}`: without `-L`, curl's
# url_effective is just the requested URL, so it cannot reveal the hop target.
# redirect_url is the Location target curl *would* follow — the canonical URL to
# submit instead. GET (body discarded) mirrors how the pipeline fetcher probes,
# so a server that only redirects GETs is caught.
#
# Sets OAG_PREFLIGHT_REDIRECTS to the count of redirecting URLs. Reads external
# URLs only (needs no OAG_TOKEN). Set OAG_PREFLIGHT=0 to skip entirely (offline
# or air-gapped validation). Transport failures (curl "000") are reported as a
# soft note, not a redirect — a URL we cannot reach is not a URL we can rewrite.
oag_preflight_urls() {
  local batch_file urls url probe status target total found unreachable
  batch_file="$1"

  if [ "${OAG_PREFLIGHT:-1}" = "0" ]; then
    echo "Preflight: skipped (OAG_PREFLIGHT=0)."
    OAG_PREFLIGHT_REDIRECTS=0
    return 0
  fi

  # Bare-URL string values only: a value that is itself a URL with no embedded
  # whitespace. This picks up every pointer/affordance URL field at any nesting
  # depth without maintaining a key allowlist, and skips prose `description`
  # text (which contains spaces) so evidence URLs mentioned mid-sentence do not
  # trigger false probes.
  urls="$(jq -r '[.. | strings | select(test("^https?://[^[:space:]]+$"))] | unique | .[]' "$batch_file")"
  if [ -z "$urls" ]; then
    echo "Preflight: no URLs to check."
    OAG_PREFLIGHT_REDIRECTS=0
    return 0
  fi

  total="$(printf '%s\n' "$urls" | grep -c .)"
  echo "Preflight: probing $total URL(s) for redirects (no -L)…"
  found=0
  unreachable=0
  while IFS= read -r url; do
    [ -n "$url" ] || continue
    # -o /dev/null discards the body; we only want the status + redirect target.
    # (-s not -sS: any error goes to /dev/null below, so -S would be a no-op.)
    probe="$(curl -s -o /dev/null --max-time "$OAG_REQUEST_TIMEOUT" \
      -w '%{http_code} %{redirect_url}' "$url" 2>/dev/null || true)"
    status="${probe%% *}"
    target="${probe#* }"
    # A redirect is a 3xx that actually carries a Location (curl fills
    # redirect_url). 300 Multiple Choices and 304 Not Modified are 3xx with no
    # target — nothing to rewrite to — so the empty-target guard skips them
    # rather than failing the run on a non-actionable status.
    if [ -n "$target" ] && [ "$status" != "000" ]; then
      found=$((found + 1))
      echo "  REDIRECT $status  $url"
      echo "           -> submit the canonical URL instead: $target"
    elif [ "$status" = "000" ] || [ -z "$status" ]; then
      unreachable=$((unreachable + 1))
      echo "  UNREACHABLE    $url (no response; check it by hand)"
    fi
  done <<EOF
$urls
EOF

  OAG_PREFLIGHT_REDIRECTS="$found"
  if [ "$found" -gt 0 ]; then
    echo "Preflight: $found redirecting URL(s). The pipeline fetcher does NOT follow redirects — replace each with its canonical target above before submitting." >&2
  elif [ "$unreachable" -gt 0 ]; then
    echo "Preflight: no redirects ($unreachable unreachable, flagged above)."
  else
    echo "Preflight: no redirects."
  fi
  return 0
}
