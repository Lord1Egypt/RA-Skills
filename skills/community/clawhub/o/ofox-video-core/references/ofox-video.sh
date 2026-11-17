#!/usr/bin/env bash
# ofox-video.sh — Ofox video generation API client: create, poll, download.
#
# Part of the ofox-video-core skill. Dependencies: bash, curl, jq. Nothing else.
#
# OFOX_API_KEY is read from the shell environment. This script never parses a
# dotenv file and never hardcodes the key; if the key lives in a file, the
# caller sources it into this script's environment first. The raw key is never
# printed by this script.
#
# The key only ever goes to one host: whatever API_BASE names. Two ways that
# could have stopped being true, both closed in 1.30.0 and both covered by
# references/test/keyguard.test.sh —
#   - OFOX_API_BASE_URL overrides API_BASE. Still supported (staging), but it
#     must be https (loopback excepted) and the override is announced on
#     stderr, naming the host that will receive the key.
#   - the create response supplies its own polling_url, and the poll loop
#     authenticates to it. It is now followed only when its scheme://host:port
#     matches API_BASE; otherwise the run stops with the job id printed, so
#     the paid job is collected with `poll` instead of being abandoned.
#
# Usage:
#   ofox-video.sh check
#   ofox-video.sh models
#   ofox-video.sh providers [MODEL]   (local/public, no API key)
#   ofox-video.sh generate --prompt "..." [OPTIONS]
#   ofox-video.sh create --prompt "..." [OPTIONS]  (submit only, no waiting)
#   ofox-video.sh batch --prompt "..." --takes N [OPTIONS]
#   ofox-video.sh poll JOB_ID [JOB_ID...] [--out-dir DIR] [--name TEXT] [--max-wait SECONDS] [--poll-interval SECONDS] [--concurrency N]
#   ofox-video.sh chain --shot "..." --shot "..." [OPTIONS]
#   ofox-video.sh contact-sheet VIDEO [VIDEO...] [--out-dir DIR]  (local, no API call)
#   ofox-video.sh last-frame VIDEO [--out-dir DIR]                (local, no API call)
#   ofox-video.sh frame-at VIDEO --at SECONDS [--out-dir DIR]     (local, no API call)
#   ofox-video.sh mux-audio VIDEO AUDIO [--out-dir DIR]           (local, no API call)
#
# generate OPTIONS:
#   --model NAME              default: bytedance/seedance-2.5. This skill has a
#                               default because every scenario built on it
#                               targets Seedance 2.5 specifically; the sibling
#                               ofox-image-core deliberately has none, because
#                               its models differ ~4x in price with no obvious
#                               winner. Run 'models' to see the alternatives —
#                               seedance-2.0-mini is ~5x cheaper for drafts.
#   --prompt TEXT             required
#   --duration N               seconds. Validated against the chosen model's
#                               own range (Seedance 2.5: 4-30, Wan 2.x: 2-15,
#                               HappyHorse: 3-15, Seedance 2.0*: 4-15).
#   --resolution VAL            validated per model, e.g. 480p | 720p | 1080p
#                               for Seedance 2.5; 720p | 1080p for Wan 2.x.
#                               Run 'ofox-video.sh models' to see each one.
#   --aspect-ratio VAL          validated per model, e.g. 21:9 | 16:9 | 4:3 |
#                               1:1 | 3:4 | 9:16 | adaptive for Seedance 2.5;
#                               16:9 | 9:16 | 1:1 for Wan 2.x.
#   --provider SLUG             pin the upstream. Defaults to byteplus for
#                               bytedance/seedance-* (Ofox otherwise routes by
#                               weight and which upstream serves a request is
#                               not predictable). 'auto' sends no pin. Also
#                               settable via OFOX_VIDEO_PROVIDER. Pricing is
#                               identical across upstreams — this is a region
#                               and moderation choice, not a cost one.
#   --dry-run                   validate, resolve the provider, build the
#                               payload and print the cost estimate, then stop
#                               WITHOUT submitting. Nothing is billed. Use this
#                               to quote a price to someone before spending.
#   --approved                  required by generate/create/batch/chain, and
#                               only by those four — they are the only
#                               subcommands that can reach the one billable
#                               request in this file. Without it the command
#                               refuses, having submitted nothing. --dry-run
#                               does not need it and must not: quoting is how
#                               the number being approved is produced.
#                               It records a stance; it cannot prove one. An
#                               agent can pass it without showing anyone a
#                               price. What it changes is that spending
#                               unquoted now has to be typed out rather than
#                               being the default.
#   --print-payload             dump the request body to stderr before sending
#                               (the API key is in a header, not the body)
#   --name TEXT                 short, human-readable name for the output file,
#                               e.g. "convenience store breakup". The file lands
#                               as <name>-<short job id>.mp4 with a matching
#                               .json sidecar. Without it the name is derived
#                               from the prompt, which still beats a bare job id
#                               but reads worse — a caller that knows what the
#                               shot is should say so. Sanitized before use.
#   --size WxH                  e.g. 1280x720 (alternative to --resolution)
#   --generate-audio true|false default: true (server-side default)
#   --seed N                    recorded and re-submittable, NOT reproducible:
#                               an identical request on a fixed seed has been
#                               measured returning a different clip.
#   --frame-first-image URL|PATH image-to-video: first frame. Accepts a remote
#                               http(s):// URL (used as-is) or a local,
#                               readable file path (base64-encoded into a
#                               data: URI automatically). Attaching a frame
#                               affects aspect_ratio: on
#                               bytedance/seedance-2.5 (the default model) it
#                               is FORCED to adaptive, overriding
#                               --aspect-ratio, because the API requires it;
#                               on any other model that lists adaptive it is
#                               only the DEFAULT when you passed no
#                               --aspect-ratio, and an explicit ratio is kept
#                               as you wrote it. Every one of those paths
#                               prints a notice — none of them is silent.
#   --frame-last-image URL|PATH  image-to-video: last frame (same URL/local
#                               file support and aspect_ratio behavior)
#   --real-person true|false
#   --callback-url URL          must be https://
#   --extra-json JSON           a JSON OBJECT merged into the request body,
#                               for fields with no flag of their own
#                               (input_references, provider.options, ...).
#                               Three things it will not do, each of which
#                               used to be possible and expensive:
#                                 - be empty. An explicit --extra-json ""
#                                   is an error, because it used to be
#                                   indistinguishable from not passing the
#                                   flag: every check skipped, nothing
#                                   merged, job billed without your fields.
#                                 - not be an object. It is merged with jq's
#                                   `*`, which only works between objects.
#                                 - set a field that has a flag (model,
#                                   prompt, duration, resolution,
#                                   aspect_ratio, size, generate_audio, seed,
#                                   real_person, callback_url, frame_images,
#                                   provider.type). Those are validated and
#                                   priced from the flags, and this merge
#                                   happens after the estimate is printed.
#   --out-dir DIR                default: current directory
#   --max-wait SECONDS           default: 540 (9 minutes)
#   --poll-interval SECONDS      default: 6
#
# batch / poll OPTIONS:
#   --concurrency N             how many jobs to WAIT for at once. Default 4,
#                               ceiling 10, also settable via
#                               OFOX_POLL_CONCURRENCY. A polling job issues one
#                               request per --poll-interval, so at the default
#                               6s each one spends 10 of the account's measured
#                               100 requests/minute: 4 is 40% of the budget, 10
#                               is all of it. Submission is never concurrent —
#                               see cmd_batch's header for why.
#
# Exit codes:
#   0  success — job completed, video downloaded
#   1  usage / parameter validation error (no network call made) — including
#      a billable subcommand run without --approved
#   2  environment error (missing curl/jq/OFOX_API_KEY)
#   3  API rejected the request, or the job ended failed/cancelled/expired
#   4  timed out waiting for a terminal state — the job is still running
#      upstream. Re-run: ofox-video.sh poll JOB_ID  (batch and a multi-id poll
#      return this only when nothing worse happened: a take that FAILED after
#      submission is exit 3, since a failure needs a new prompt and a timeout
#      needs another poll.)
#      Do NOT re-run 'generate' for the same request — that creates a
#      duplicate, separately billed job.
#   5  the create call had an ambiguous network failure (no HTTP response was
#      received at all). We cannot tell whether the job was created
#      server-side. Do not auto-retry create — check https://app.ofox.ai
#      first, then retry manually only if nothing was created.
#   6  --out-dir could not be created or entered (bad path, permissions).
#      This is a local filesystem problem, not an API problem — if it
#      happened during 'generate', the job may already exist server-side
#      (or still be running). Do NOT re-run 'generate'; fix --out-dir and
#      re-run: ofox-video.sh poll JOB_ID --out-dir <a writable directory>
#
# No-resubmit rule: once a create call gets a response (any HTTP status),
# this script never issues a second create call for the same invocation. If
# polling is slow, times out, or a poll request itself errors, the fix is to
# retry the POLL, never the CREATE. See the 'poll' subcommand.

set -u

DEFAULT_API_BASE="https://api.ofox.ai/v1"
# Overridable on purpose (pointing a run at a staging deployment is a real
# need), but never silently: validate_api_base() below refuses a plaintext
# non-loopback host and announces the override on stderr, because this
# variable decides which host receives OFOX_API_KEY.
API_BASE="${OFOX_API_BASE_URL:-$DEFAULT_API_BASE}"
GET_KEY_URL="https://app.ofox.ai"
DEFAULT_MODEL="bytedance/seedance-2.5"
DEFAULT_MAX_WAIT=540
DEFAULT_POLL_INTERVAL=6

# Concurrency for waiting on several jobs at once (batch, and `poll` with more
# than one job id). Submission stays sequential; only the waiting overlaps.
#
# The number is set by requests per minute, not by how many jobs feel
# reasonable. Each polling job issues at most one GET per poll interval, so at
# the default 6s that is 10 requests/minute per job. The account this was
# measured on allows 100 RPM, which makes 10 concurrent polls exactly the
# limit — so 10 is the ceiling the flag will accept and never the default.
#
# The default of 4 is 40 RPM, 40% of that budget. The other 60% is not spare:
# a batch's creates go out first, a 429 or 5xx retries at the same cadence,
# and an agent commonly has another Ofox call (a model list, an image job)
# in flight in the same session. Four also covers the common case in one wave
# — three or four takes of one prompt — so the wall clock is that of a single
# clip.
MAX_CONCURRENCY=10
DEFAULT_CONCURRENCY="${OFOX_POLL_CONCURRENCY:-4}"
# Measured on the repo owner's account, 2026-09-05. Used only to warn: this
# script never blocks a request because of it.
ACCOUNT_RPM=100
# Warn above 60% of the budget. Being at 100% is how a session earns 429s,
# which cost a poll cycle per job — time, not money.
RPM_SOFT_LIMIT=60
# How often the supervisor says something while several jobs are running. A
# ten-minute silence is indistinguishable from a hang.
POLL_HEARTBEAT=30
# Ceiling for the per-job backoff after consecutive 429s.
POLL_BACKOFF_MAX=60

# Cap for the readable part of an output filename, counted in Unicode
# codepoints (not bytes). 40 CJK characters is 120 UTF-8 bytes, which leaves
# the whole name — slug, '-', 8 hex of job id, extension — far below the
# 255-byte limit every filesystem this runs on enforces. Latin text needs the
# headroom more than CJK does: 24 was enough for a Chinese scene name but cut
# "convenience-store-breakup" mid-word.
SLUG_MAX_CHARS=40

# Network timeouts. Only the model-list fetches had any, which left every
# call that actually costs money able to hang forever on a stalled
# connection — and made --max-wait a promise the poll loop could not keep,
# since elapsed only advances once curl returns.
#
# CREATE_MAX_TIME is generous: a create normally answers in seconds, and
# timing one out lands in the ambiguous "no response, cannot tell whether it
# was billed" path (exit 5). That path exists and is handled correctly;
# hanging indefinitely helps no one and is not safer.
#
# Downloads deliberately get no overall limit — a large file is legitimately
# slow — and are guarded against stalls instead: abort if throughput stays
# under DOWNLOAD_MIN_BYTES/s for DOWNLOAD_STALL_SECONDS.
CONNECT_TIMEOUT=15
CREATE_MAX_TIME=120
POLL_MAX_TIME=60
DOWNLOAD_MIN_BYTES=512
DOWNLOAD_STALL_SECONDS=60

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODELS_SNAPSHOT="$SCRIPT_DIR/models-snapshot.json"
PRICING_SNAPSHOT="$SCRIPT_DIR/pricing-snapshot.json"
MODELS_CACHE_TTL="${OFOX_MODELS_TTL:-86400}" # 24h

# Fallback only. Per-model limits come from GET /v1/models; these unions of
# every video model's advertised values are used when that list is
# unavailable, so a valid request is never blocked by a missing model list.
# A union that has gone stale rejects a request the API would have accepted,
# which is worse than the round trip it saves: 768p and 2k (minimax/hailuo-3)
# were missing here until 2026-09-14, so hailuo's only two resolutions were
# refused offline. Re-check this against the catalog when refreshing the
# bundled snapshot.
VALID_RESOLUTIONS="480p 720p 768p 1080p 2k 4k"
VALID_ASPECT_RATIOS="21:9 16:9 4:3 1:1 3:4 9:16 adaptive"

# Set by load_models(): the file holding the model list, and where it came
# from ("live" | "cache" | "stale-cache" | "snapshot").
MODELS_FILE=""
MODELS_SOURCE=""

# Upstream providers. Ofox routes a multi-upstream model by weight and says
# outright that "which provider serves any single request is not predictable".
# For Seedance that alternates between BytePlus (outside mainland China) and
# Volcengine Ark (mainland), which moderate differently — so the same prompt
# can pass one run and be rejected the next with nothing to point at.
#
# Measured 2026-08-30 via the public catalog endpoint: all four
# bytedance/seedance-* are served by byteplus + volcengine; all four alibaba/*
# by aliyun alone. We pin Seedance to byteplus and leave everything else alone:
# with a single upstream, weighted routing is already deterministic, so pinning
# would change nothing while adding a hardcoded fact that can rot.
#
# Re-measured 2026-09-14, and the fact rotted exactly as predicted. Every
# alibaba/* model now reports TWO upstreams (alicloud + aliyun), and the two
# minimax/hailuo-3* models added since report minimax + novita. So the
# "single upstream, nothing to pin" rationale above no longer holds for
# alibaba/* — those requests route by weight today and are not pinned.
# Deliberately left that way here: whether the two alibaba upstreams differ
# behaviourally has not been measured, and pinning on an unmeasured guess is
# what this comment already warns against. Tracked with the hailuo-3 pinning
# question (Fizzy #841).
#
# Pricing was identical across upstreams on 2026-08-30 (verified tier by
# tier), and that is ALSO no longer universally true: alibaba/wan-3.0 prices
# alicloud at 0.11/s and aliyun at 0.0857/s for 720p, a 28% spread. Every
# other model still matches across its upstreams. rate_for() prefers the
# pinned provider's card for this reason; when nothing is pinned it takes the
# first card, which for wan-3.0 happens to be the dearer one — the safe
# direction per "never under-quote", but by array order, not by design. Do not
# "simplify" the pinned-card preference away.
#
# This list is the global set of slugs the script will accept at all; whether
# a given slug serves a given model is checked separately against the catalog
# below. alicloud and novita were missing here until 2026-09-14, so `providers
# MODEL` printed upstreams that `--provider` then refused.
VALID_PROVIDERS="openai anthropic gemini azure_foundry foundry aws_bedrock bedrock google_vertex vertex alicloud aliyun volcengine byteplus deepseek moonshot zhipu minimax novita grok jina tencent"
DEFAULT_SEEDANCE_PROVIDER="byteplus"

# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

list_contains() {
  # $1 = needle, $2 = space-separated haystack
  local needle="$1" hay="$2" item
  for item in $hay; do
    [ "$item" = "$needle" ] && return 0
  done
  return 1
}

# ---------------------------------------------------------------------------
# where OFOX_API_KEY is allowed to go
#
# Two hosts in this script are not chosen by its own code, and the key rides
# along with both:
#
#   1. OFOX_API_BASE_URL points the whole client — Authorization header
#      included — wherever it says. That is a capability worth keeping (a
#      staging deployment is the obvious legitimate use), so it is not
#      removed; it is narrowed to https (loopback excepted, for a local test
#      server) and made impossible to set without being told, on stderr,
#      which host is about to receive the key.
#   2. The create response carries its own `polling_url`, and the poll loop
#      sends `Authorization: Bearer $OFOX_API_KEY` to it. That is the one
#      path here that needs no compromised local environment at all: a
#      tampered or misconfigured API response is enough to hand the key to a
#      third party. So every polling URL is checked against API_BASE's origin
#      before the first request goes to it. The field is still honoured —
#      it is a normal shape for a job API — it just cannot move hosts.
#
# Duplicated in ofox-image-core/references/ofox-image.sh on purpose: each
# skill has to work when installed on its own, so a file shared across skill
# directories is not an option (CONTRIBUTING rule 7). Fix both.
# ---------------------------------------------------------------------------

url_origin() {
  # $1 = a URL. Prints "scheme://host:port" lowercased, with the scheme's
  # default port made explicit so https://api.ofox.ai and
  # https://api.ofox.ai:443 compare equal. Returns 1 for anything that is not
  # an http(s) URL.
  local url="$1" scheme rest authority host port
  case "$url" in
    [Hh][Tt][Tt][Pp]://*|[Hh][Tt][Tt][Pp][Ss]://*) : ;;
    *) return 1 ;;
  esac
  scheme="$(printf '%s' "${url%%://*}" | tr '[:upper:]' '[:lower:]')"
  rest="${url#*://}"
  authority="${rest%%/*}"
  authority="${authority%%\?*}"
  authority="${authority%%#*}"
  # Userinfo is never part of an Ofox URL, and keeping only what follows the
  # last '@' is what makes "https://api.ofox.ai@evil.example/v1/videos/x"
  # report evil.example — the host that would really receive the request —
  # instead of reading as ours to anyone (or any check) skimming the string.
  authority="${authority##*@}"
  case "$authority" in
    \[*\]*)
      host="${authority%%\]*}]"
      port="${authority#*\]}"
      port="${port#:}"
      ;;
    *:*)
      host="${authority%%:*}"
      port="${authority#*:}"
      ;;
    *)
      host="$authority"
      port=""
      ;;
  esac
  [ -n "$host" ] || return 1
  if [ -z "$port" ]; then
    case "$scheme" in
      http) port=80 ;;
      https) port=443 ;;
    esac
  fi
  case "$port" in ''|*[!0-9]*) return 1 ;; esac
  printf '%s://%s:%s' "$scheme" "$(printf '%s' "$host" | tr '[:upper:]' '[:lower:]')" "$port"
}

url_host() {
  # $1 = a URL. Prints just the host, for messages that have to name it.
  local origin="$1"
  origin="$(url_origin "$origin")" || return 1
  origin="${origin#*://}"
  printf '%s' "${origin%:*}"
}

is_loopback_host() {
  case "$1" in
    localhost|127.*|\[::1\]|::1) return 0 ;;
    *) return 1 ;;
  esac
}

validate_api_base() {
  # Runs once per invocation, before anything can use API_BASE. The default
  # is fine by construction, so this is entirely about the override.
  local override="${OFOX_API_BASE_URL:-}" origin host
  [ -n "$override" ] || return 0

  if ! origin="$(url_origin "$override")"; then
    echo "ERROR: OFOX_API_BASE_URL is set to '$override', which is not an http:// or https:// URL." >&2
    echo "Unset it to use $DEFAULT_API_BASE, or set it to a full base URL such as https://staging.example.com/v1." >&2
    return 2
  fi
  host="$(url_host "$override")"
  case "$origin" in
    https://*) : ;;
    *)
      if ! is_loopback_host "$host"; then
        echo "ERROR: OFOX_API_BASE_URL is set to '$override', which is not https://." >&2
        echo "OFOX_API_KEY travels in an Authorization header on every request this script makes, so a plaintext base URL would put your key on the wire in clear text." >&2
        echo "Use an https:// URL, or a loopback host (localhost, 127.0.0.1, [::1]) for a local test server." >&2
        return 2
      fi
      ;;
  esac
  echo "NOTE: OFOX_API_BASE_URL is set, so this run talks to host '$host' ($override) instead of $DEFAULT_API_BASE — including any request that carries your OFOX_API_KEY in an Authorization header. Unset OFOX_API_BASE_URL to go back to Ofox." >&2
  return 0
}

assert_same_origin_as_api_base() {
  # $1 = a URL the API handed back, $2 = what it is, for the message.
  # Succeeds only when that URL points at the same scheme://host:port this
  # client was configured for.
  local url="$1" what="$2" got want
  want="$(url_origin "$API_BASE")" || want=""
  got="$(url_origin "$url")" || got=""
  if [ -z "$got" ]; then
    echo "ERROR: the API returned a $what this script will not follow: '$url' is not an http:// or https:// URL." >&2
    return 1
  fi
  [ "$got" = "$want" ] && return 0
  echo "ERROR: the API returned a $what pointing at a different host: '$(url_host "$url")' (from '$url'), while this client is configured for '$(url_host "$API_BASE")' ($API_BASE)." >&2
  echo "Polling sends 'Authorization: Bearer \$OFOX_API_KEY', so a URL from the response body is never followed off the configured host — a tampered or misconfigured response must not be able to redirect your API key." >&2
  return 1
}

# ---------------------------------------------------------------------------
# model list: per-model limits instead of one hardcoded table
#
# GET /v1/models is a public, keyless, free endpoint that reports each model's
# real duration range, resolutions, aspect ratios and modes. Validating against
# it means a bad combination is caught locally with the model's own legal
# values, instead of costing a round trip to be told "invalid_request" — and
# it keeps working when Ofox adds a model or changes a limit.
#
# Order of preference: fresh cache -> live fetch -> stale cache -> bundled
# snapshot. If all of those fail we validate against the unions above and say
# so: a missing model list must never block a request that would have worked
# (CONTRIBUTING rule 6, fail open).
# ---------------------------------------------------------------------------

file_age_seconds() {
  # Portable mtime age. BSD stat (macOS) and GNU stat (Linux) disagree on
  # flags, so try both rather than assuming a platform.
  local f="$1" mtime now
  mtime="$(stat -f %m "$f" 2>/dev/null || stat -c %Y "$f" 2>/dev/null)" || return 1
  [ -n "$mtime" ] || return 1
  now="$(date +%s)"
  echo $((now - mtime))
}

load_models() {
  # Idempotent: the list is fetched at most once per invocation.
  [ -n "$MODELS_FILE" ] && return 0

  local cache_dir="${XDG_CACHE_HOME:-$HOME/.cache}/ofox"
  local cache_file="$cache_dir/models.json"
  local age

  if [ -f "$cache_file" ]; then
    age="$(file_age_seconds "$cache_file")" || age=""
    if [ -n "$age" ] && [ "$age" -lt "$MODELS_CACHE_TTL" ]; then
      MODELS_FILE="$cache_file"
      MODELS_SOURCE="cache"
      return 0
    fi
  fi

  # No Authorization header: this endpoint is public, and sending the key
  # where it isn't needed is a habit worth not having.
  local tmp
  mkdir -p "$cache_dir" 2>/dev/null
  tmp="$(mktemp "${TMPDIR:-/tmp}/ofox-models.XXXXXX")" || tmp=""
  if [ -n "$tmp" ] &&
    curl -fsS --max-time 10 "$API_BASE/models" -o "$tmp" 2>/dev/null &&
    jq -e '(.data | length) > 0' "$tmp" >/dev/null 2>&1; then
    if mv -f "$tmp" "$cache_file" 2>/dev/null; then
      MODELS_FILE="$cache_file"
    else
      MODELS_FILE="$tmp" # cache dir unwritable; use it for this run only
    fi
    MODELS_SOURCE="live"
    return 0
  fi
  [ -n "$tmp" ] && rm -f "$tmp"

  if [ -f "$cache_file" ]; then
    MODELS_FILE="$cache_file"
    MODELS_SOURCE="stale-cache"
    echo "NOTE: could not refresh the model list from $API_BASE/models; using the cached copy at $cache_file." >&2
    return 0
  fi

  if [ -f "$MODELS_SNAPSHOT" ]; then
    MODELS_FILE="$MODELS_SNAPSHOT"
    MODELS_SOURCE="snapshot"
    local snap_date
    snap_date="$(jq -r '._snapshot_date // "unknown date"' "$MODELS_SNAPSHOT" 2>/dev/null)"
    echo "NOTE: could not reach $API_BASE/models; validating against the bundled snapshot ($snap_date). A model added since then may be rejected here — set OFOX_SKIP_MODEL_VALIDATION=1 to skip per-model checks." >&2
    return 0
  fi

  MODELS_SOURCE="none"
  echo "NOTE: no model list available (fetch failed, no cache, no bundled snapshot). Falling back to generic parameter checks; the API will have the final say." >&2
  return 1
}

default_provider_for() {
  # $1 = model id. Prints the upstream to pin, or nothing to let Ofox route.
  # Only models served by MORE THAN ONE upstream belong here.
  case "$1" in
    bytedance/seedance-*) echo "$DEFAULT_SEEDANCE_PROVIDER" ;;
    *) echo "" ;;
  esac
}

catalog_cache_path() {
  # $1 = model id. One cache file per model; '/' isn't legal in a filename.
  local slug
  slug="$(printf '%s' "$1" | tr '/' '-')"
  echo "${XDG_CACHE_HOME:-$HOME/.cache}/ofox/catalog-${slug}.json"
}

load_catalog() {
  # $1 = model id. Fetches the public, keyless model catalog entry, which
  # carries provider_cards[] (each upstream and its price matrix). Prints the
  # cache file path on success. Never fetched for the default provider — only
  # for explicit --provider validation and the 'providers' subcommand.
  local model="$1" cache_file age
  cache_file="$(catalog_cache_path "$model")"

  if [ -f "$cache_file" ]; then
    age="$(file_age_seconds "$cache_file")" || age=""
    if [ -n "$age" ] && [ "$age" -lt "$MODELS_CACHE_TTL" ]; then
      printf '%s' "$cache_file"
      return 0
    fi
  fi

  local base tmp
  # The catalog lives under /v2 while API_BASE points at /v1.
  base="${API_BASE%/v1}"
  mkdir -p "$(dirname "$cache_file")" 2>/dev/null
  tmp="$(mktemp "${TMPDIR:-/tmp}/ofox-catalog.XXXXXX")" || return 1
  if curl -fsS --max-time 10 \
    "$base/v2/models/catalog/$model?include=provider_price" -o "$tmp" 2>/dev/null &&
    jq -e '(.provider_cards | length) > 0' "$tmp" >/dev/null 2>&1; then
    mv -f "$tmp" "$cache_file" 2>/dev/null || cache_file="$tmp"
    printf '%s' "$cache_file"
    return 0
  fi
  rm -f "$tmp"

  # A stale copy still answers "which upstreams serve this model" well enough.
  if [ -f "$cache_file" ]; then
    printf '%s' "$cache_file"
    return 0
  fi
  return 1
}

catalog_providers() {
  # $1 = model id. Prints that model's upstreams, space-separated, or nothing.
  local f
  f="$(load_catalog "$1")" || return 1
  jq -r '[.provider_cards[].provider_type] | join(" ")' "$f" 2>/dev/null
}

model_entry() {
  # $1 = model id (or one of its aliases). Prints that model's whole entry as
  # compact JSON, or nothing if the list doesn't have it.
  [ -n "$MODELS_FILE" ] || return 1
  jq -c --arg m "$1" \
    'first(.data[] | select(.id == $m or ((.aliases // []) | index($m)) != null)) // empty' \
    "$MODELS_FILE" 2>/dev/null
}

entry_list() {
  # $1 = entry JSON, $2 = jq path into it. Prints a space-separated list.
  printf '%s' "$1" | jq -r "($2 // []) | join(\" \")" 2>/dev/null
}

entry_num() {
  # $1 = entry JSON, $2 = jq path. Prints a number, or nothing if absent/null.
  printf '%s' "$1" | jq -r "($2 // empty) | tostring" 2>/dev/null
}

resolve_image_ref() {
  # $1 = the raw value passed to --frame-first-image/--frame-last-image.
  #
  # Passes http(s):// URLs and already-formed data: URIs through unchanged.
  # Base64-encodes a readable local file into a data:image/<ext>;base64,...
  # URI (portable `base64` + `tr` only, no new dependency). A bare string
  # that's neither a URL nor an existing local file is passed through as-is
  # so the API's own validation produces a clear error rather than this
  # script guessing. But a path that DOES exist as a file yet can't be read
  # (permissions) is a clear local problem — fail loudly and non-zero here
  # rather than silently sending the raw filesystem path as if it were a
  # usable image reference.
  local val="$1" ext ctype b64
  case "$val" in
    http://*|https://*|data:*)
      printf '%s' "$val"
      return 0
      ;;
  esac
  if [ -f "$val" ] && [ ! -r "$val" ]; then
    echo "ERROR: local image file '$val' exists but is not readable (check file permissions)." >&2
    return 1
  fi
  if [ -f "$val" ] && [ -r "$val" ]; then
    ext=$(printf '%s' "$val" | sed -E 's/.*\.//' | tr '[:upper:]' '[:lower:]')
    case "$ext" in
      jpg|jpeg) ctype="image/jpeg" ;;
      png) ctype="image/png" ;;
      webp) ctype="image/webp" ;;
      gif) ctype="image/gif" ;;
      bmp) ctype="image/bmp" ;;
      *) ctype="image/jpeg" ;;
    esac
    b64=$(base64 <"$val" 2>/dev/null | tr -d '\n')
    if [ -z "$b64" ]; then
      echo "ERROR: failed to base64-encode local image file '$val'." >&2
      return 1
    fi
    printf 'data:%s;base64,%s' "$ctype" "$b64"
    return 0
  fi
  printf '%s' "$val"
  return 0
}

usage() {
  cat >&2 <<'EOF'
ofox-video.sh — Ofox video generation API client (create, poll, download).

  ofox-video.sh check
  ofox-video.sh models
  ofox-video.sh providers [MODEL]
  ofox-video.sh generate --prompt "..." [OPTIONS]
  ofox-video.sh create   --prompt "..." [OPTIONS]   (submit only, returns a job id)
         add --dry-run to any of generate/batch/chain to price it without spending
         generate/create/batch/chain refuse to run without --approved. Quote the
         job with --dry-run, show the user the estimate, then re-run the same
         command with --approved. --dry-run itself never needs it.
  ofox-video.sh batch --prompt "..." --takes N [--contact-sheet|--no-contact-sheet] [--concurrency N] [OPTIONS]
  ofox-video.sh poll JOB_ID [JOB_ID...] [--out-dir DIR] [--name TEXT] [--max-wait SECONDS] [--poll-interval SECONDS] [--concurrency N]
  ofox-video.sh chain --shot "..." --shot "..." [--shots-file FILE] [--no-concat] [OPTIONS]
  ofox-video.sh contact-sheet VIDEO [VIDEO...] [--out-dir DIR]
  ofox-video.sh last-frame VIDEO [--out-dir DIR]
  ofox-video.sh frame-at VIDEO --at SECONDS [--out-dir DIR]
  ofox-video.sh mux-audio VIDEO AUDIO [--out-dir DIR]
         contact-sheet/last-frame/frame-at/mux-audio are local ffmpeg work:
         no API call, no key, no cost

Downloads are named <slug>-<short job id>.<ext>, where the slug comes from
--name or, without it, from the prompt. Each video gets a .json sidecar
holding the full job id, the prompt and the cost — the short id in the
filename cannot be expanded back on its own.

Independent clips are waited for in parallel, not one after another: give
'poll' every job id at once, or let 'batch' do it for its takes. --concurrency
caps how many are polled simultaneously (default 4, ceiling 10 — 10 polls at
the default 6s interval is already the whole measured 100 requests/minute
account limit). Submission stays sequential so a rejected create still stops a
batch before the remaining takes are paid for.

Seedance jobs are pinned to the byteplus upstream by default; override with
--provider volcengine, or --provider auto to let Ofox route by weight. Run
'providers' to see a model's upstreams. Pricing is identical across them.

Run with no arguments for this message. See the top of this file, or
skills/ofox-video-core/SKILL.md and references/api-params.md, for the full
option list and parameter reference.
EOF
}

# ---------------------------------------------------------------------------
# environment checks
# ---------------------------------------------------------------------------

check_curl_jq() {
  local missing=0
  if ! command -v curl >/dev/null 2>&1; then
    echo "ERROR: curl is not installed." >&2
    echo "  macOS:          usually preinstalled; if not, 'brew install curl'" >&2
    echo "  Debian/Ubuntu:  sudo apt-get install curl" >&2
    echo "  Other:          https://curl.se/download.html" >&2
    missing=1
  fi
  if ! command -v jq >/dev/null 2>&1; then
    echo "ERROR: jq is not installed." >&2
    echo "  macOS:          brew install jq" >&2
    echo "  Debian/Ubuntu:  sudo apt-get install jq" >&2
    echo "  Other:          https://jqlang.org/download/" >&2
    missing=1
  fi
  [ "$missing" -eq 0 ]
}

check_api_key() {
  if [ -z "${OFOX_API_KEY:-}" ]; then
    echo "ERROR: OFOX_API_KEY is not set in your shell environment." >&2
    echo "Get a key at ${GET_KEY_URL} (log in -> Settings -> API Keys -> Create New Key)," >&2
    echo "then export it in your shell:" >&2
    echo "  export OFOX_API_KEY=your_key_here" >&2
    echo "Already have it in a file? Source that file into this shell instead:" >&2
    echo "  set -a; . /path/to/.env; set +a" >&2
    return 1
  fi
  return 0
}

cmd_check() {
  # Exits 2, not 1. This subcommand exists to diagnose the environment, and 2
  # is what the exit-code table means by an environment error. Returning 1
  # would tell a caller following that table to "fix the flag and retry",
  # which is the wrong advice for a missing key.
  local ok=0
  check_curl_jq || ok=2
  if ! check_api_key; then
    ok=2
    # Not having a key is not a dead end: pricing works without one, and
    # that is exactly what someone deciding whether to sign up wants.
    echo "" >&2
    echo "You can still price a job before signing up — these need no key:" >&2
    echo "  $0 models" >&2
    echo "  $0 providers" >&2
    echo "  $0 generate --dry-run --prompt \"...\" --duration 15 --resolution 720p" >&2
  fi
  if [ "$ok" -eq 0 ]; then
    echo "OK: curl, jq, and OFOX_API_KEY are all present."
    echo "Note: the key is present but has NOT been verified against the API — this"
    echo "check makes no network call. A typo'd key passes here and fails on the"
    echo "first real request."
  fi
  return "$ok"
}

cmd_providers() {
  # Lists the upstreams serving a model, with each one's price tiers. Needs no
  # API key — the catalog endpoint is public — so it is safe before signing up.
  check_curl_jq || return 2
  local model="${1:-$DEFAULT_MODEL}"
  local f
  if ! f="$(load_catalog "$model")"; then
    echo "ERROR: could not fetch the provider list for '$model'." >&2
    echo "  Check the model id (run 'ofox-video.sh models'), or try again when the network is available." >&2
    return 3
  fi

  local providers
  providers="$(jq -r '[.provider_cards[].provider_type] | join(" ")' "$f")"
  echo "Upstream providers for $model: $providers"
  echo

  jq -r '
    ["PROVIDER", "RESOLUTION", "MODE", "$/s"],
    (.provider_cards[] | .provider_type as $p
      | (.pricing.video_pricing.tiers[]? | select(.resolution)
         | [$p, .resolution, (.input_type // "-"), .price]))
    | @tsv' "$f" | column -t -s "$(printf '\t')"

  echo
  case "$model" in
    bytedance/seedance-*)
      echo "This skill pins Seedance to '$DEFAULT_SEEDANCE_PROVIDER' by default. Without a pin, Ofox"
      echo "distributes requests by weight and which upstream serves any one request is"
      echo "not predictable — which matters because these two moderate differently:"
      echo "  byteplus    ByteDance's platform for markets outside mainland China"
      echo "  volcengine  Volcengine Ark, its mainland China platform, standard moderation"
      echo "Pricing is identical across both, so this is a region and moderation choice,"
      echo "never a cost one. Override with --provider, or --provider auto to unpin."
      ;;
    *)
      if [ "$(printf '%s' "$providers" | wc -w | tr -d ' ')" -le 1 ]; then
        echo "Only one upstream serves this model, so routing is already deterministic"
        echo "and this skill sends no provider field for it."
      fi
      ;;
  esac
  return 0
}

cmd_models() {
  # Lists the video models with their real limits and per-second base price.
  # Needs no API key — GET /v1/models is public — so it is safe to run before
  # a user has signed up, and it costs nothing.
  check_curl_jq || return 2
  load_models || true
  if [ -z "$MODELS_FILE" ]; then
    echo "ERROR: could not obtain a model list (no network, no cache, no bundled snapshot)." >&2
    return 3
  fi

  echo "Video models (source: $MODELS_SOURCE)"
  echo

  # Show the rate a caller would actually be charged: the model's own default
  # resolution, text-to-video. The headline pricing.output_video_per_second is
  # deliberately NOT shown — for seedance-2.5 it reports the 480p rate ($0.11)
  # while the model defaults to 720p ($0.24), and a reader multiplying the
  # first big number they see by their duration is off by 118%.
  local rows="" mid mdefault mrate
  while IFS=$'\t' read -r mid mdefault mrest; do
    [ -z "$mid" ] && continue
    mrate="$(rate_for "$mid" "$mdefault" "t2v" "" 2>/dev/null)" || mrate=""
    [ -z "$mrate" ] && mrate="?"
    rows="$rows$mid\t$mrate\t$mdefault\t$mrest\n"
  done <<EOF_MODELS
$(jq -r '
    .data[]
    | select((.supported_endpoints // []) | index("/v1/videos"))
    | [ .id + (if .is_deprecated then " (deprecated)" else "" end),
        (.video_attributes.default_resolution // "720p"),
        ((.video_attributes.resolutions // []) | join(",")) + "\t" +
        ((.video_attributes.min_duration_seconds | tostring) + "-" +
         (.video_attributes.max_duration_seconds | tostring) + "s") + "\t" +
        ((.video_attributes.modes // []) | join(",")) ]
    | @tsv' "$MODELS_FILE")
EOF_MODELS

  {
    printf 'MODEL\t$/s AT DEFAULT\tDEFAULT RES\tALL RESOLUTIONS\tDURATION\tMODES\n'
    printf '%b' "$rows"
  } | column -t -s "$(printf '\t')"

  echo
  echo "The rate shown is for each model's own default resolution, text-to-video —"
  echo "what you pay if you don't pass --resolution. Other resolutions cost more or"
  echo "less; run 'ofox-video.sh providers MODEL' for the full matrix, or check a"
  echo "price for a specific job with 'generate --dry-run' (no API key needed)."
  return 0
}

# ---------------------------------------------------------------------------
# error-code -> friendly message mapping
# (per contract: program against error.code, never parse error.message)
# ---------------------------------------------------------------------------

print_error_message() {
  local code="$1"
  case "$code" in
    invalid_request)
      echo "  invalid_request: a required field is missing or a parameter value is invalid. Re-check model, prompt, duration, resolution, aspect_ratio." >&2 ;;
    input_moderation_failed)
      echo "  input_moderation_failed: the INPUT image or video was rejected before generation, most often because it contains a real person's face." >&2
      echo "    bytedance/seedance-2.5 image-to-video rejects real-person reference images unless the caller declares the rights to them. Options:" >&2
      echo "    1. Use a non-photoreal reference (illustration, anime, product, landscape) — those pass." >&2
      echo "    2. ONLY if the user holds the rights to this person's likeness and has said so: --real-person true routes AUTHORIZED real-person references through Ofox's privacy-preserving preprocessing (measured lifting this refusal on 2.5, 2026-09-16). It is a declaration of authorization, NOT a retry flag — do not set it to clear this error." >&2
      echo "    Nothing was generated, so this call was not billed." >&2 ;;
    invalid_provider_type)
      echo "  invalid_provider_type: the provider slug sent is not one Ofox recognises. Run 'ofox-video.sh providers MODEL' for the valid ones, or pass --provider auto to let Ofox choose." >&2 ;;
    provider_type_unavailable)
      echo "  provider_type_unavailable: that provider is a real slug but does not serve this model. Run 'ofox-video.sh providers MODEL' to see which do, or pass --provider auto to let Ofox choose." >&2 ;;
    invalid_callback_url)
      echo "  invalid_callback_url: callback_url must be HTTPS and must not point to a private/internal network." >&2 ;;
    references_conflict)
      echo "  references_conflict: frame_images and input_references cannot both be set — use only one." >&2 ;;
    too_many_references)
      echo "  too_many_references: input_references allows at most 9 images, 3 audio clips (<=15s each), and 1 video." >&2 ;;
    cancel_not_supported)
      echo "  cancel_not_supported: the upstream provider cannot interrupt this job once it has started." >&2 ;;
    cancel_failed)
      echo "  cancel_failed: the job is already in a terminal state and cannot be cancelled." >&2 ;;
    unauthorized|invalid_api_key)
      echo "  $code: OFOX_API_KEY is missing or invalid. Get/verify a key at ${GET_KEY_URL} (Settings -> API Keys)." >&2 ;;
    upstream_auth_failed)
      echo "  upstream_auth_failed: Ofox's upstream provider rejected authentication — an Ofox-side routing issue, not your key. Try again shortly." >&2 ;;
    insufficient_credits)
      echo "  insufficient_credits: your Ofox balance is too low for this job. No charge was made. Add credits at ${GET_KEY_URL}." >&2 ;;
    not_found)
      echo "  not_found: this job id is invalid or not accessible with this API key." >&2 ;;
    model_not_found)
      echo "  model_not_found: the requested model is not available. Check the model name (e.g. bytedance/seedance-2.5)." >&2 ;;
    rate_limited)
      echo "  rate_limited: too many requests. Wait a few seconds and retry — this is not a job failure." >&2 ;;
    upstream_error|route_error)
      echo "  $code: the upstream video provider failed. If this happened on job creation, no job was made and it is safe to retry create; if it happened while polling an existing job, retry the poll — do not create a new job." >&2 ;;
    internal_error)
      echo "  internal_error: an Ofox platform-side error. If this happened on job creation, no job was made and it is safe to retry create; if it happened while polling, retry the poll — do not create a new job." >&2 ;;
    output_moderation_failed)
      echo "  output_moderation_failed: the job's OUTPUT failed a post-generation content check — this happens AFTER the video was generated, not at submission, and cannot be caught by client-side validation. This job is NOT billed (no usage field on the response)." >&2
      echo "    Two fixes. Both are new requests, not resubmissions of the failed one, so neither double-bills:" >&2
      echo "    1. Retry on the other upstream. Seedance is served by byteplus and volcengine, which moderate differently, so the same prompt can pass on one and not the other. Use --provider volcengine if you were on byteplus, or --provider byteplus if you were on volcengine." >&2
      echo "    2. Change the prompt or the reference image/audio." >&2 ;;
    bad_data_uri|download_failed|unreachable|not_image|too_large)
      echo "  $code: the real_person reference image failed validation (must be a small, publicly reachable, valid image). Check the image URL and retry." >&2 ;;
    "")
      echo "  (no error.code in the response body)" >&2 ;;
    *)
      echo "  $code: unrecognized error code — see references/api-params.md or https://ofox.ai/docs/api/videos for the current list." >&2 ;;
  esac
}

print_api_error() {
  # $1 = context ("create" or "poll"), $2 = http_code, $3 = response body
  local context="$1" http_code="$2" body="$3" code message
  code=$(printf '%s' "$body" | jq -r '.error.code // empty' 2>/dev/null)
  message=$(printf '%s' "$body" | jq -r '.error.message // empty' 2>/dev/null)
  echo "ERROR: Ofox API rejected the $context request (HTTP $http_code)." >&2
  print_error_message "$code"
  # error.message is not a stable contract to branch logic on (see the
  # error-code table), but it can carry a specific detail the generic
  # mapped explanation above doesn't (e.g. a minimum image width) — always
  # surface it, not only when error.code itself is unrecognized/absent.
  if [ -n "$message" ]; then
    echo "  Upstream message: $message" >&2
  fi
  if [ -z "$code" ]; then
    echo "  Raw response body:" >&2
    printf '%s\n' "$body" >&2
  fi
}

# ---------------------------------------------------------------------------
# the spend gate
# ---------------------------------------------------------------------------

# There is exactly one billable request in this file: the POST to
# $API_BASE/videos in cmd_generate. Every other curl here is a GET. So the set
# of subcommands that can put a charge on the account is exactly the set that
# reaches that POST — `generate`, `create` (the same call without the wait),
# `batch` (N of them) and `chain` (N of them) — and those four refuse to run
# without --approved.
#
# Nothing else is guarded, and each omission is a decision rather than an
# oversight:
#   check / models / providers   read-only, and `models`/`providers` are the
#                                public catalog: free, no key needed.
#   contact-sheet / last-frame / frame-at / mux-audio
#                                local ffmpeg over a file the caller already
#                                has. No network call at all.
#   poll                         only ever issues GETs against a job that
#                                already exists. Guarding it would be actively
#                                harmful: it is the recovery command this
#                                script prints whenever a run is refused,
#                                times out or is interrupted, so blocking it
#                                would strand a job that has already been paid
#                                for.
# references/test/approval.test.sh derives both halves of that split from the
# usage text at run time rather than from a list retyped here, so a new
# subcommand that reaches the POST without a guard turns the suite red.
#
# --dry-run returns before this guard in all four, on purpose. Quoting a price
# is the step that produces the number the user approves; a gate that blocked
# the quote would close the only route through itself.
#
# What this flag is: a place where spending has to be typed out, which makes it
# visible in a transcript and refusable by a reviewer.
#
# What it is NOT — and the docs must not claim otherwise: evidence that an
# approval happened. Nothing in a shell script can observe the conversation
# between an agent and its user, and an agent can pass --approved without ever
# showing anyone a price, exactly as it could previously just run the command.
# This moves "spend without quoting" from the default behaviour to a
# deliberate, auditable act. It does not detect it.
require_approved() {
  # require_approved SUBCOMMAND APPROVED_FLAG
  local sub="$1" approved="${2:-}"
  [ -n "$approved" ] && return 0
  echo "" >&2
  echo "ERROR: '$sub' spends real money and was run without --approved." >&2
  echo "Nothing was submitted and nothing was billed." >&2
  echo "  1. Quote it first, for free: re-run this exact command with --dry-run" >&2
  echo "       $0 $sub --dry-run ...   (submits nothing, needs no API key)" >&2
  echo "  2. Show the user the 'Estimated cost:' line it prints, together with" >&2
  echo "     the model, the full prompt and the parameters being quoted. The" >&2
  echo "     table that belongs in front of them is in this skill's" >&2
  echo "     references/approval-gate.md." >&2
  echo "  3. Once they have said yes to THAT table, run the original command" >&2
  echo "     again with --approved added." >&2
  echo "--approved records a stance; it cannot prove anyone was asked. It is" >&2
  echo "here so that spending without quoting has to be typed out instead of" >&2
  echo "being what happens by default." >&2
  return 1
}

# ---------------------------------------------------------------------------
# generate: validate params, build payload, POST, poll, download
# ---------------------------------------------------------------------------

cmd_generate() {
  if ! check_curl_jq; then return 2; fi

  local model="$DEFAULT_MODEL"
  local provider=""
  local provider_explicit=""
  local print_payload=""
  local dry_run=""
  local approved=""
  local submit_only="${OFOX_SUBMIT_ONLY:-}"
  local prompt=""
  local duration=""
  local resolution=""
  local aspect_ratio=""
  local size=""
  local generate_audio=""
  local seed=""
  local frame_first=""
  local frame_last=""
  local real_person=""
  local callback_url=""
  local extra_json=""
  # Whether --extra-json was written on the command line at all. bash cannot
  # tell "flag omitted" from "flag given an empty value" by looking at the
  # value, and the difference is the whole of the 2026-09-17 defect: a
  # `--extra-json "$(jq …)"` whose jq died on ARG_MAX hands over an empty
  # string, the `[ -n "$extra_json" ]` guard skips every check AND the merge,
  # and the job is submitted and billed with none of the references in it.
  local extra_json_seen=""
  local name_hint=""
  local out_dir="$PWD"
  local max_wait="$DEFAULT_MAX_WAIT"
  local poll_interval="$DEFAULT_POLL_INTERVAL"
  local key val

  while [ $# -gt 0 ]; do
    key="$1"
    case "$key" in
      --print-payload)
        print_payload=1
        shift
        continue
        ;;
      --dry-run)
        dry_run=1
        shift
        continue
        ;;
      --approved)
        approved=1
        shift
        continue
        ;;
    esac
    case "$key" in
      --model|--prompt|--duration|--resolution|--aspect-ratio|--size|--generate-audio|--seed|--provider|--frame-first-image|--frame-last-image|--real-person|--callback-url|--extra-json|--name|--out-dir|--max-wait|--poll-interval)
        if [ $# -lt 2 ]; then
          echo "ERROR: $key requires a value." >&2
          return 1
        fi
        val="$2"
        shift 2
        ;;
      *)
        echo "ERROR: unknown option '$key' for generate." >&2
        return 1
        ;;
    esac
    case "$key" in
      --model) model="$val" ;;
      --prompt) prompt="$val" ;;
      --duration) duration="$val" ;;
      --resolution) resolution="$val" ;;
      --aspect-ratio) aspect_ratio="$val" ;;
      --size) size="$val" ;;
      --generate-audio) generate_audio="$val" ;;
      --seed) seed="$val" ;;
      --provider) provider="$val"; provider_explicit=1 ;;
      --frame-first-image) frame_first="$val" ;;
      --frame-last-image) frame_last="$val" ;;
      --real-person) real_person="$val" ;;
      --callback-url) callback_url="$val" ;;
      --extra-json) extra_json="$val"; extra_json_seen=1 ;;
      --name) name_hint="$val" ;;
      --out-dir) out_dir="$val" ;;
      --max-wait) max_wait="$val" ;;
      --poll-interval) poll_interval="$val" ;;
    esac
  done

  # --- validation (no network calls made before this point) ---

  if [ -z "$prompt" ]; then
    echo "ERROR: --prompt is required." >&2
    return 1
  fi

  if [ -n "$duration" ]; then
    case "$duration" in
      ''|*[!0-9]*)
        echo "ERROR: --duration must be a positive integer number of seconds (got '$duration')." >&2
        return 1
        ;;
    esac
  fi

  # Per-model limits from the live model list, with the generic unions as the
  # fallback. Everything here happens before any create call.
  local entry="" ok_resolutions="$VALID_RESOLUTIONS" ok_aspects="$VALID_ASPECT_RATIOS"
  local min_dur="" max_dur="" ok_modes=""
  # ok_aspects falls back to the union of every model's values, so it cannot
  # answer "does THIS model support X". model_aspects is set only from a real
  # catalog entry and stays empty otherwise — the image-to-video block below
  # needs that distinction to fail open instead of inventing a value.
  local model_aspects=""
  # The catalog's canonical id for whatever the caller typed. Every model has
  # documented aliases ('seedance-2.5', 'seedance-2.5-20260807' for
  # bytedance/seedance-2.5) and the API takes them, so a rule keyed on a model
  # id has to compare against the resolved id, not the typed string. Stays as
  # typed when no catalog entry was available.
  local model_canonical="$model"

  if [ "${OFOX_SKIP_MODEL_VALIDATION:-}" != "1" ] && load_models; then
    entry="$(model_entry "$model")"

    if [ -z "$entry" ]; then
      # An id the list doesn't have. When the list is current, that's a real
      # error worth catching locally. When we're reading a bundled snapshot,
      # the model may simply be newer than the file — warn and let the API
      # decide rather than blocking a request that would have worked.
      if [ "$MODELS_SOURCE" = "snapshot" ] || [ "$MODELS_SOURCE" = "stale-cache" ]; then
        echo "NOTE: '$model' is not in the $MODELS_SOURCE model list, which may just be out of date. Skipping per-model checks; the API will validate it." >&2
      else
        echo "ERROR: --model '$model' is not in the Ofox model list. Run 'ofox-video.sh models' to see what is available." >&2
        return 1
      fi
    elif [ -z "$(entry_num "$entry" '.video_attributes')" ] &&
      ! printf '%s' "$entry" | jq -e '(.supported_endpoints // []) | index("/v1/videos")' >/dev/null 2>&1; then
      echo "ERROR: --model '$model' exists but does not support video generation (/v1/videos). Run 'ofox-video.sh models' to see the video models." >&2
      return 1
    else
      local v_res v_asp v_min v_max v_modes v_id
      v_id="$(printf '%s' "$entry" | jq -r '.id // empty' 2>/dev/null)"
      [ -n "$v_id" ] && model_canonical="$v_id"
      v_res="$(entry_list "$entry" '.video_attributes.resolutions')"
      v_asp="$(entry_list "$entry" '.video_attributes.aspect_ratios')"
      v_min="$(entry_num "$entry" '.video_attributes.min_duration_seconds')"
      v_max="$(entry_num "$entry" '.video_attributes.max_duration_seconds')"
      v_modes="$(entry_list "$entry" '.video_attributes.modes')"
      [ -n "$v_res" ] && ok_resolutions="$v_res"
      [ -n "$v_asp" ] && ok_aspects="$v_asp"
      [ -n "$v_asp" ] && model_aspects="$v_asp"
      [ -n "$v_min" ] && min_dur="$v_min"
      [ -n "$v_max" ] && max_dur="$v_max"
      [ -n "$v_modes" ] && ok_modes="$v_modes"

      if printf '%s' "$entry" | jq -e '.is_deprecated == true' >/dev/null 2>&1; then
        echo "NOTE: '$model' is marked deprecated by Ofox. It still runs for now; consider moving to a current model." >&2
      fi
    fi
  fi

  if [ -n "$duration" ] && [ -n "$min_dur" ] && [ -n "$max_dur" ]; then
    if [ "$duration" -lt "$min_dur" ] || [ "$duration" -gt "$max_dur" ]; then
      echo "ERROR: --duration must be between $min_dur and $max_dur for $model (got $duration)." >&2
      return 1
    fi
  fi

  if [ -n "$resolution" ] && ! list_contains "$resolution" "$ok_resolutions"; then
    echo "ERROR: --resolution '$resolution' is not supported by $model. Valid values: $ok_resolutions" >&2
    return 1
  fi

  if [ -n "$aspect_ratio" ] && ! list_contains "$aspect_ratio" "$ok_aspects"; then
    echo "ERROR: --aspect-ratio '$aspect_ratio' is not supported by $model. Valid values: $ok_aspects" >&2
    return 1
  fi

  if [ -n "$ok_modes" ] && { [ -n "$frame_first" ] || [ -n "$frame_last" ]; } &&
    ! list_contains "i2v" "$ok_modes"; then
    echo "ERROR: $model does not support image-to-video (frame images). It supports: $ok_modes" >&2
    return 1
  fi

  # --- upstream provider ---------------------------------------------------
  # Precedence: --provider > OFOX_VIDEO_PROVIDER > per-model default.
  # "auto" at any level means send no provider field and let Ofox route.
  if [ -z "$provider_explicit" ]; then
    provider="${OFOX_VIDEO_PROVIDER:-}"
    [ -z "$provider" ] && provider="$(default_provider_for "$model")"
  fi

  if [ "$provider" = "auto" ]; then
    provider=""
  elif [ -n "$provider" ]; then
    if ! list_contains "$provider" "$VALID_PROVIDERS"; then
      echo "ERROR: --provider '$provider' is not a known Ofox provider slug." >&2
      echo "  Valid slugs: $VALID_PROVIDERS" >&2
      echo "  Run 'ofox-video.sh providers $model' to see which ones serve this model, or use --provider auto to let Ofox choose." >&2
      return 1
    fi
    # Check the slug actually serves this model, but only from catalog data we
    # can get; never block a request because the catalog was unreachable.
    local model_providers=""
    if [ -n "$provider_explicit" ] || [ -n "${OFOX_VIDEO_PROVIDER:-}" ]; then
      model_providers="$(catalog_providers "$model" 2>/dev/null)" || model_providers=""
    else
      # Default path: only cross-check against a cache already on disk, so the
      # common case costs no network call at all.
      local cached
      cached="$(catalog_cache_path "$model")"
      if [ -f "$cached" ]; then
        model_providers="$(jq -r '[.provider_cards[].provider_type] | join(" ")' "$cached" 2>/dev/null)"
      fi
    fi
    if [ -n "$model_providers" ] && ! list_contains "$provider" "$model_providers"; then
      if [ -n "$provider_explicit" ]; then
        echo "ERROR: provider '$provider' does not serve $model." >&2
        echo "  This model is served by: $model_providers" >&2
        echo "  Use one of those, or --provider auto to let Ofox choose." >&2
        return 1
      fi
      # A default that the catalog says won't work: warn and stand down rather
      # than fail a request the user never asked to pin.
      echo "NOTE: the default provider '$provider' does not serve $model (it is served by: $model_providers). Letting Ofox route this one instead." >&2
      provider=""
    fi
  fi

  if [ -n "$size" ]; then
    case "$size" in
      [0-9]*x[0-9]*) ;;
      *)
        echo "ERROR: --size must be in WIDTHxHEIGHT form, e.g. 1280x720 (got '$size')." >&2
        return 1
        ;;
    esac
  fi

  if [ -n "$generate_audio" ] && [ "$generate_audio" != "true" ] && [ "$generate_audio" != "false" ]; then
    echo "ERROR: --generate-audio must be 'true' or 'false' (got '$generate_audio')." >&2
    return 1
  fi

  if [ -n "$real_person" ] && [ "$real_person" != "true" ] && [ "$real_person" != "false" ]; then
    echo "ERROR: --real-person must be 'true' or 'false' (got '$real_person')." >&2
    return 1
  fi

  if [ -n "$seed" ]; then
    case "$seed" in
      ''|*[!0-9]*)
        echo "ERROR: --seed must be a non-negative integer (got '$seed')." >&2
        return 1
        ;;
    esac
  fi

  if [ -n "$callback_url" ]; then
    case "$callback_url" in
      https://*) ;;
      *)
        echo "ERROR: --callback-url must start with https:// (Ofox rejects non-HTTPS callback URLs)." >&2
        return 1
        ;;
    esac
  fi

  # An explicitly empty --extra-json is an error, and omitting the flag is
  # byte-for-byte what it always was. The asymmetry is the point: every
  # existing caller that does not pass the flag is unaffected, while the one
  # shape that used to be silently dropped now stops the run before anything
  # is billed.
  if [ -n "$extra_json_seen" ] && [ -z "$extra_json" ]; then
    echo "ERROR: --extra-json was given an empty value." >&2
    echo "This usually means a command substitution produced nothing — most often '\$(jq -n …)' with a large data: URI, which dies on ARG_MAX, writes one line to stderr and yields an empty string." >&2
    echo "Until 1.30.0 that empty string was treated as 'flag not passed': no JSON check, nothing merged, and the job submitted and billed with none of your extra fields in it. Build the JSON into a variable, check it with 'jq -e .', then pass it — or drop the flag if you meant to send nothing." >&2
    return 1
  fi

  if [ -n "$extra_json" ]; then
    # `jq empty`, not `jq -e .`: -e keys its exit status on the OUTPUT value,
    # so a perfectly valid `null` or `false` was reported as "not valid
    # JSON". Both are still refused — by the object check below, which says
    # what is actually wrong with them.
    if ! printf '%s' "$extra_json" | jq empty >/dev/null 2>&1; then
      echo "ERROR: --extra-json is not valid JSON." >&2
      return 1
    fi
    # It is merged with jq's `*`, which is only defined between objects. A
    # valid-but-not-object value made the merge fail, the command
    # substitution yield an empty payload, and the request go out empty.
    if ! printf '%s' "$extra_json" | jq -e 'type == "object"' >/dev/null 2>&1; then
      echo "ERROR: --extra-json must be a JSON object (it is merged into the request body), got $(printf '%s' "$extra_json" | jq -r 'type')." >&2
      return 1
    fi
    if { [ -n "$frame_first" ] || [ -n "$frame_last" ]; } && printf '%s' "$extra_json" | jq -e 'has("input_references")' >/dev/null 2>&1; then
      echo "ERROR: cannot combine --frame-first-image/--frame-last-image with input_references in --extra-json (references_conflict) — use one or the other." >&2
      return 1
    fi
    # --extra-json is merged LAST, so any key it carries wins over the flags.
    # For a field with a flag, that means it lands in the request having
    # skipped the per-model validation, the aspect-ratio rules and the price
    # estimate the flag goes through — i.e. the body says 30 seconds at 1080p
    # while the quote the user approved said 4 seconds at 480p. Same rule the
    # sibling ofox-image.sh already applies to --extra-form: if a flag owns
    # the field, use the flag. Everything without a flag still passes
    # through, which is what the escape hatch is for.
    local clash
    clash=$(printf '%s' "$extra_json" | jq -r '
      ["model","prompt","duration","resolution","aspect_ratio","size",
       "generate_audio","seed","real_person","callback_url","frame_images"] as $guarded
      | [ (keys_unsorted[] | select(. as $k | $guarded | index($k)))
        , (select(.provider? | type == "object" and has("type")) | "provider.type")
        , (select(has("provider") and (.provider | type != "object")) | "provider")
        ] | join(", ")')
    if [ -n "$clash" ]; then
      echo "ERROR: --extra-json sets $clash, which this script validates and prices from its own flag(s). Use the flag instead: --model, --prompt, --duration, --resolution, --aspect-ratio, --size, --generate-audio, --seed, --real-person, --callback-url, --frame-first-image/--frame-last-image, --provider." >&2
      echo "A key merged through --extra-json wins over the flags and is merged AFTER the cost estimate is computed, so this would submit a job that does not match the price anyone approved." >&2
      echo "Fields with no flag are unaffected — input_references and provider.options still pass through here." >&2
      return 1
    fi
  fi

  case "$max_wait" in
    ''|*[!0-9]*)
      echo "ERROR: --max-wait must be a positive integer number of seconds (got '$max_wait')." >&2
      return 1
      ;;
  esac
  case "$poll_interval" in
    ''|*[!0-9]*)
      echo "ERROR: --poll-interval must be a positive integer number of seconds (got '$poll_interval')." >&2
      return 1
      ;;
  esac

  # A dry run sends no authenticated request, so it must not demand a key:
  # quoting a price is exactly what someone does *before* signing up, and the
  # repo's rule is to guide a keyless user rather than dead-end them.
  if [ -n "$dry_run" ]; then
    DRY_RUN_ACTIVE=1
  else
    if ! check_api_key; then return 2; fi
    # A run with no --approved is going to be refused below, after the estimate
    # has printed. DRY_RUN_ACTIVE means "this run is quoting, not spending",
    # which is exactly true here — without it the estimate would end "Actual
    # billing is reported below" on a run that reports no billing at all.
    [ -z "$approved" ] && DRY_RUN_ACTIVE=1
  fi

  # --out-dir is resolved here, under dry run too. A path that can't be
  # created is a free thing to catch — discovering it after a job is paid for
  # (exit 6) is the outcome a dry run exists to prevent.
  local dry_out_input="$out_dir"
  mkdir -p "$out_dir" 2>/dev/null
  if [ -z "$(cd "$out_dir" 2>/dev/null && pwd)" ]; then
    echo "ERROR: --out-dir '$dry_out_input' could not be created or entered (bad path or missing permissions)." >&2
    return 6
  fi

  # --- image-to-video and aspect_ratio -------------------------------------
  # 'adaptive' means two different things depending on the model, and
  # collapsing them would be a defect in either direction:
  #
  #   bytedance/seedance-2.5 + a frame image REQUIRES aspect_ratio=adaptive.
  #     Verified against the real API (see the seedance-2.5-image-to-video
  #     research): every other value fails once frame_images is attached, so
  #     it is forced even over a ratio the caller passed explicitly. Matched
  #     on the catalog's canonical id, so the documented aliases ('seedance-2.5')
  #     get the same treatment as the full id.
  #   Any other model that lists 'adaptive' merely SUPPORTS it. There it is
  #     the right default when the caller named no ratio — without it the
  #     attached frame's shape may not be honoured, and you only find that
  #     out after paying for the clip — but an explicit ratio is a choice
  #     this model never demanded, so overriding it would be overreach.
  #
  # "Does this model support adaptive" comes from the same catalog entry the
  # validation above already read (video_attributes.aspect_ratios), never
  # from a second hardcoded model list. When no entry was available
  # model_aspects is empty and nothing is added: fail open rather than invent
  # a value the model may reject.
  #
  # Every branch says what it did. This block never changes — nor declines to
  # change — an aspect ratio silently.
  if [ -n "$frame_first" ] || [ -n "$frame_last" ]; then
    if [ "$model_canonical" = "bytedance/seedance-2.5" ]; then
      if [ -n "$aspect_ratio" ] && [ "$aspect_ratio" != "adaptive" ]; then
        echo "NOTE: forcing aspect_ratio=adaptive for bytedance/seedance-2.5 image-to-video (required by the API); ignoring requested aspect ratio '$aspect_ratio'." >&2
      else
        echo "NOTE: forcing aspect_ratio=adaptive for bytedance/seedance-2.5 image-to-video (required by the API)." >&2
      fi
      aspect_ratio="adaptive"
    elif [ "$aspect_ratio" = "adaptive" ]; then
      echo "NOTE: $model image-to-video: sending aspect_ratio=adaptive as requested; the clip follows the attached frame's shape." >&2
    elif [ -n "$aspect_ratio" ]; then
      if list_contains "adaptive" "$model_aspects"; then
        echo "NOTE: $model image-to-video: keeping the aspect ratio you asked for ('$aspect_ratio'). Unlike bytedance/seedance-2.5, this model does not require 'adaptive', so your value stands — pass --aspect-ratio adaptive if you want the clip to follow the attached frame's shape instead." >&2
      else
        echo "NOTE: $model image-to-video: keeping the aspect ratio you asked for ('$aspect_ratio'); this model does not offer 'adaptive', so the attached frame's shape cannot be inherited automatically." >&2
      fi
    elif list_contains "adaptive" "$model_aspects"; then
      aspect_ratio="adaptive"
      echo "NOTE: $model image-to-video: no --aspect-ratio was passed, defaulting to aspect_ratio=adaptive (this model's catalog entry lists it) so the clip follows the attached frame's shape. Pass --aspect-ratio to pick a fixed ratio instead." >&2
    elif [ -n "$model_aspects" ]; then
      echo "NOTE: $model image-to-video: sending no aspect_ratio — this model does not offer 'adaptive' (it accepts: $model_aspects), so the attached frame's shape may not be preserved. Pass --aspect-ratio to choose one yourself." >&2
    else
      echo "NOTE: $model image-to-video: sending no aspect_ratio — no catalog entry for this model was available (offline, unknown id, or per-model checks skipped), so 'adaptive' support could not be confirmed and inventing a value could get the request rejected. Pass --aspect-ratio to set one explicitly." >&2
    fi
  fi

  # --- build the request payload ---

  # Roll a seed when the caller didn't pick one, exactly as batch already
  # does for its takes. Without this the server picks a seed and reports it
  # nowhere — the poll response carries no seed field — so a clip could not
  # even be described afterwards, let alone aimed at again at a higher
  # resolution. Choosing it here costs nothing (it is random either way) and
  # makes every job recordable. Recordable, not reproducible: an identical
  # request on a fixed seed has been measured coming back different.
  if [ -z "$seed" ]; then
    seed=$(( (RANDOM << 15 | RANDOM) & 0x7FFFFFFF ))
  fi

  local payload='{}'
  payload=$(printf '%s' "$payload" | jq --arg v "$model" '.model=$v')
  payload=$(printf '%s' "$payload" | jq --arg v "$prompt" '.prompt=$v')
  [ -n "$duration" ] && payload=$(printf '%s' "$payload" | jq --argjson v "$duration" '.duration=$v')
  [ -n "$resolution" ] && payload=$(printf '%s' "$payload" | jq --arg v "$resolution" '.resolution=$v')
  [ -n "$aspect_ratio" ] && payload=$(printf '%s' "$payload" | jq --arg v "$aspect_ratio" '.aspect_ratio=$v')
  [ -n "$size" ] && payload=$(printf '%s' "$payload" | jq --arg v "$size" '.size=$v')
  [ -n "$generate_audio" ] && payload=$(printf '%s' "$payload" | jq --argjson v "$generate_audio" '.generate_audio=$v')
  [ -n "$seed" ] && payload=$(printf '%s' "$payload" | jq --argjson v "$seed" '.seed=$v')
  [ -n "$real_person" ] && payload=$(printf '%s' "$payload" | jq --argjson v "$real_person" '.real_person=$v')
  [ -n "$callback_url" ] && payload=$(printf '%s' "$payload" | jq --arg v "$callback_url" '.callback_url=$v')

  # A local image's base64 data URI can be well over 1MB (frame_first_ref/
  # frame_last_ref below), and `--extra-json` could in principle carry one
  # too (e.g. an embedded base64 image inside input_references). Passing a
  # string that large as a `jq --arg`/`--argjson` command-line value hits
  # the OS's ARG_MAX (execve argv+environ limit, 1,048,576 bytes on this
  # machine) and fails with "jq: Argument list too long" *before any
  # network call is made* — reproduced for real with a real 885KB PNG whose
  # base64 encoding (1,179,996 bytes) already exceeded ARG_MAX on its own.
  # Fix: never put a potentially-large value in a jq command-line argument.
  # Write it to a temp file instead and read it with `--rawfile`/
  # `--slurpfile` (file content, not an exec argument — not subject to
  # ARG_MAX). Same short-lived create/use/remove-immediately pattern as
  # tmp_body below, so a temp file never survives past the single jq call
  # that needs it, on every path (success or an early `return 1`).
  if [ -n "$frame_first" ] || [ -n "$frame_last" ]; then
    local frames='[]' frame_first_ref frame_last_ref tmp_ref
    if [ -n "$frame_first" ]; then
      frame_first_ref=$(resolve_image_ref "$frame_first") || return 1
      tmp_ref=$(mktemp)
      printf '%s' "$frame_first_ref" >"$tmp_ref"
      frames=$(printf '%s' "$frames" | jq --rawfile u "$tmp_ref" '. + [{"type":"image_url","image_url":{"url":$u},"frame_type":"first_frame"}]')
      rm -f "$tmp_ref"
    fi
    if [ -n "$frame_last" ]; then
      frame_last_ref=$(resolve_image_ref "$frame_last") || return 1
      tmp_ref=$(mktemp)
      printf '%s' "$frame_last_ref" >"$tmp_ref"
      frames=$(printf '%s' "$frames" | jq --rawfile u "$tmp_ref" '. + [{"type":"image_url","image_url":{"url":$u},"frame_type":"last_frame"}]')
      rm -f "$tmp_ref"
    fi
    # frames itself now embeds whatever large base64 data URI was resolved
    # above, so merging it into payload must also avoid --argjson on the
    # command line — same reasoning, same fix.
    tmp_ref=$(mktemp)
    printf '%s' "$frames" >"$tmp_ref"
    payload=$(printf '%s' "$payload" | jq --slurpfile f "$tmp_ref" '.frame_images=$f[0]')
    rm -f "$tmp_ref"
  fi

  if [ -n "$provider" ]; then
    payload=$(printf '%s' "$payload" | jq --arg v "$provider" '.provider = {type: $v}')
  fi

  if [ -n "$extra_json" ]; then
    local tmp_extra merged
    tmp_extra=$(mktemp)
    printf '%s' "$extra_json" >"$tmp_extra"
    merged=$(printf '%s' "$payload" | jq --slurpfile extra "$tmp_extra" '. * $extra[0]')
    rm -f "$tmp_extra"
    # A failed merge leaves the command substitution empty, which without this
    # would post an empty body to a billable endpoint. The object check above
    # should make it unreachable; an unreachable check that costs nothing and
    # guards a paid request stays.
    if [ -z "$merged" ]; then
      echo "ERROR: merging --extra-json into the request body failed, so nothing was submitted and nothing was billed." >&2
      return 1
    fi
    payload="$merged"
  fi

  if [ -n "$print_payload" ]; then
    # The API key travels in an Authorization header, never in this body, so
    # printing it leaks nothing. Useful for seeing what actually got sent.
    echo "PAYLOAD $(printf '%s' "$payload" | jq -c .)" >&2
  fi

  # --- create the job (exactly one create call per invocation) ---

  # Say what this will cost before spending anything. i2v bills at t2v rates —
  # only a video input moves it to the v2v tier.
  #
  # The API's reference element type is "video_url" (alongside "image_url" and
  # "audio_url"), NOT "video". An earlier version of this check guessed "video"
  # and so quoted the t2v rate for a v2v job: a real run estimated $0.44 and
  # billed $0.56. Both spellings are accepted now — mispricing a job is worse
  # than tolerating a type string the API wouldn't have taken anyway.
  local est_mode="t2v"
  if printf '%s' "$extra_json" |
    jq -e '(.input_references // []) | map(select(.type == "video_url" or .type == "video")) | length > 0' \
      >/dev/null 2>&1; then
    est_mode="v2v"
  fi
  print_estimate "$model" "${resolution:-}" "$est_mode" "$provider" "$duration" 1

  local provider_label="auto (Ofox weighted)"
  [ -n "$provider" ] && provider_label="$provider"

  if [ -n "$dry_run" ]; then
    # Everything above already ran: arguments parsed, parameters validated
    # against the model, provider resolved, payload built, price quoted.
    # Nothing below runs, so nothing is submitted and nothing is billed. This
    # is what turns "quote before spending" into an instruction an agent can
    # actually follow.
    echo "DRY RUN — nothing was submitted and nothing was billed." >&2
    echo "Re-run without --dry-run to generate." >&2
    echo "STATUS dry_run"
    echo "MODEL $model"
    echo "PROVIDER $provider_label"
    [ -n "$duration" ] && echo "DURATION $duration"
    [ -n "$resolution" ] && echo "RESOLUTION $resolution"
    return 0
  fi

  # Last free instant. Everything above is validation, resolution and the
  # quote; the next statement is the POST that bills. The guard sits here
  # rather than at the top of the function on purpose: refusing after the
  # estimate has printed means the refusal carries the number the user needs
  # to be shown, and it leaves every parameter error still reported as a
  # parameter error.
  require_approved "${SUBCOMMAND:-generate}" "$approved" || return 1

  echo "Submitting job to Ofox (model=$model, provider=$provider_label)..." >&2
  # payload can itself now be well over 1MB (a resolved frame image is
  # inlined into it above) — pass it to curl via `--data-binary @file`, not
  # `-d "$payload"`. The latter is an exec argument like jq --arg/--argjson
  # above and would hit the same ARG_MAX wall just one step later.
  local tmp_body http_code curl_rc body tmp_payload
  tmp_payload=$(mktemp)
  printf '%s' "$payload" >"$tmp_payload"
  tmp_body=$(mktemp)
  http_code=$(curl -sS -o "$tmp_body" -w '%{http_code}' \
    --connect-timeout "$CONNECT_TIMEOUT" --max-time "$CREATE_MAX_TIME" \
    -X POST "$API_BASE/videos" \
    -H "Authorization: Bearer $OFOX_API_KEY" \
    -H "Content-Type: application/json" \
    --data-binary @"$tmp_payload")
  curl_rc=$?
  rm -f "$tmp_payload"
  body=$(cat "$tmp_body")
  rm -f "$tmp_body"

  if [ "$curl_rc" -ne 0 ]; then
    echo "ERROR: could not reach the Ofox API to create the job (curl exit $curl_rc)." >&2
    echo "We cannot tell whether a job was created server-side — no HTTP response was received." >&2
    echo "Do NOT blindly retry. Find out first — list your recent jobs and look for a new one:" >&2
    echo "  curl -s -H \"Authorization: Bearer \$OFOX_API_KEY\" \"${API_BASE}/videos?limit=5\" | jq ." >&2
    echo "(or open ${GET_KEY_URL}). If the newest entry predates this attempt, nothing was created" >&2
    echo "and retrying is safe. If a new job is there, poll it by id — never create it again." >&2
    return 5
  fi

  if [ "$http_code" != "202" ]; then
    print_api_error "create" "$http_code" "$body"
    return 3
  fi

  local job_id polling_url
  job_id=$(printf '%s' "$body" | jq -r '.id // empty')
  polling_url=$(printf '%s' "$body" | jq -r '.polling_url // empty')

  if [ -z "$job_id" ]; then
    echo "ERROR: Ofox returned 202 but the response has no job id — unexpected response shape." >&2
    echo "Raw body:" >&2
    printf '%s\n' "$body" >&2
    return 3
  fi
  # The response's own polling_url is used when it is on the host this client
  # is configured for, and the canonical URL is the fallback when the field is
  # absent — both are normal. What is not normal is a polling_url on another
  # host: the poll loop authenticates, so following one would send the key
  # somewhere the caller never named. That is refused, and refusing it must
  # not strand the job, which by this line exists and is billable.
  if [ -z "$polling_url" ]; then
    polling_url="$API_BASE/videos/$job_id"
  elif ! assert_same_origin_as_api_base "$polling_url" "polling_url"; then
    local bad_abs_out
    bad_abs_out="$(cd "$out_dir" 2>/dev/null && pwd)" || bad_abs_out="$out_dir"
    # The request half of the record, so the recovery poll below can still
    # write a complete sidecar.
    save_request_handoff "$payload" "$bad_abs_out" "$job_id"
    echo "" >&2
    echo "The job WAS created and is billable: $job_id. Nothing has been lost — it was not polled, that is all." >&2
    echo "Collect it over the configured host instead (poll builds the URL itself, it never reads one from a response):" >&2
    echo "  $0 poll $job_id --out-dir $bad_abs_out" >&2
    echo "JOB_ID $job_id"
    echo "SEED $seed"
    echo "OUT_DIR $bad_abs_out"
    return 3
  fi

  echo "Job created: $job_id" >&2
  echo "Polling: $polling_url" >&2
  echo "If this times out before the job finishes, do NOT re-run 'generate' for the same request." >&2
  echo "Instead run: $0 poll $job_id" >&2

  if [ -n "$submit_only" ]; then
    # Submit-and-return. The whole point is that this finishes in seconds, so
    # a caller with a short tool timeout can never end up in the one genuinely
    # bad state: job created and billable, id never printed. Wait separately
    # with `poll`, as many short calls as it takes.
    # Absolute, because the whole point of create is that the *next* call
    # happens separately — possibly from a different working directory. A
    # relative path here would hand the caller a poll command that silently
    # downloads somewhere else, or fails.
    local abs_out
    abs_out="$(cd "$out_dir" 2>/dev/null && pwd)" || abs_out="$out_dir"

    # Hand the follow-up poll the half of the record the API will not give it:
    # the response echoes neither resolution, aspect ratio nor seed, so
    # without this the sidecar written by `poll` is missing exactly the
    # fields needed to re-render the shot. A dotfile keyed by job id, so
    # concurrent creates cannot collide and a user browsing out-dir does not
    # see scratch state next to their videos.
    save_request_handoff "$payload" "$abs_out" "$job_id"

    echo "STATUS submitted"
    echo "JOB_ID $job_id"
    echo "SEED $seed"
    echo "POLLING_URL $polling_url"
    echo "OUT_DIR $abs_out"
    # Suppressed by batch, which is about to wait for every take itself and
    # says the same thing once for all of them instead of N times.
    if [ -z "${OFOX_SUBMIT_QUIET:-}" ]; then
      echo "" >&2
      echo "Submitted, not waiting. Download it with:" >&2
      # Carry --name into the suggested command: the follow-up poll is a
      # separate process that would otherwise fall back to naming the file from
      # the prompt, quietly losing the name the caller chose here.
      if [ -n "$name_hint" ]; then
        echo "  $0 poll $job_id --out-dir $abs_out --name \"$name_hint\"" >&2
      else
        echo "  $0 poll $job_id --out-dir $abs_out" >&2
      fi
      echo "The job is billable from now on whether or not you poll for it." >&2
    fi
    return 0
  fi

  echo "SEED $seed"
  poll_and_download "$job_id" "$polling_url" "$out_dir" "$max_wait" "$poll_interval" \
    "$name_hint" "$payload"
  return $?
}

# ---------------------------------------------------------------------------
# batch: N takes of one prompt, real per-take billing, optional contact sheet
#
# Generating several takes and keeping one is how this actually gets used, and
# it is the thing nobody prices honestly. So: estimate before spending, report
# what each take really cost from its own usage.video_cost, and total it.
#
# Every take is its own job, created one at a time through the same
# cmd_generate path a single generate uses (in its submit-only mode). That
# keeps the no-resubmit rule intact for free — nothing here can re-POST a
# request that already exists — and it means a take benefits from every
# validation and error mapping the single-shot path already has.
#
# The two halves are deliberately different:
#
#   submit  SEQUENTIAL. A create answers in seconds, so serialising it costs
#           almost no wall clock, and it is what makes the money guard exact:
#           if take 2's create is rejected, takes 3..N are never sent.
#   wait    CONCURRENT, up to --concurrency at a time. This is the ten-minute
#           half. One 15s 720p job measured over 600s of wall clock on
#           2026-09-05, so three takes serially is half an hour for work the
#           API does in ten minutes. The account allows 100 RPM and a polling
#           job spends 10 of them, so nothing about the rate limit required
#           the old serial wait.
#
# A take that fails to SUBMIT stops the run: whatever broke take 2's create
# will almost certainly break takes 3..N, and continuing would spend real
# money to collect identical failures. Takes already submitted are still
# waited for and downloaded — they are billable whether or not we collect
# them, and abandoning a paid job is not a saving.
#
# A take that fails AFTER submission (a generation-time or moderation failure)
# is a different animal: the money is already committed and the other takes
# are already running, so it is reported and the rest complete normally.
# ---------------------------------------------------------------------------

MAX_TAKES=10

cmd_batch() {
  local takes="" seed_given="" prompt_seen="" batch_provider="" batch_dry="" batch_approved=""
  local passthrough=() out_dir="$PWD" duration="" resolution="" model="$DEFAULT_MODEL"
  local sheet="auto"
  local concurrency="$DEFAULT_CONCURRENCY"
  local name_hint="" max_wait="$DEFAULT_MAX_WAIT" poll_interval="$DEFAULT_POLL_INTERVAL"
  local key val

  while [ $# -gt 0 ]; do
    key="$1"
    case "$key" in
      --takes)
        [ $# -lt 2 ] && { echo "ERROR: --takes requires a value." >&2; return 1; }
        takes="$2"; shift 2; continue
        ;;
      --concurrency)
        # Not forwarded to generate: it governs the wait this function runs
        # itself, and generate has no waiting left to do here.
        [ $# -lt 2 ] && { echo "ERROR: --concurrency requires a value." >&2; return 1; }
        concurrency="$2"; shift 2; continue
        ;;
      --contact-sheet)
        sheet="always"; shift; continue
        ;;
      --no-contact-sheet)
        sheet="never"; shift; continue
        ;;
      --print-payload)
        # Valueless flags have to be forwarded without consuming the next
        # argument, or they eat whatever follows them.
        passthrough+=("$key"); shift; continue
        ;;
      --dry-run)
        batch_dry=1; shift; continue
        ;;
      --approved)
        # Forwarded as well as recorded: every take goes through cmd_generate,
        # which has the same guard sitting next to the POST it makes.
        batch_approved=1; passthrough+=("$key"); shift; continue
        ;;
      *)
        if [ $# -lt 2 ]; then
          echo "ERROR: $key requires a value." >&2
          return 1
        fi
        val="$2"
        case "$key" in
          --provider) batch_provider="$val" ;;
          --seed) seed_given="$val" ;;
          --prompt) prompt_seen="1" ;;
          --out-dir) out_dir="$val" ;;
          --duration) duration="$val" ;;
          --resolution) resolution="$val" ;;
          --model) model="$val" ;;
          --name) name_hint="$val" ;;
          --max-wait) max_wait="$val" ;;
          --poll-interval) poll_interval="$val" ;;
        esac
        passthrough+=("$key" "$val")
        shift 2
        ;;
    esac
  done

  # --- batch-specific validation (no network calls yet) ---

  if [ -z "$takes" ]; then
    echo "ERROR: --takes is required for batch (how many takes to generate). Use 'generate' for a single one." >&2
    return 1
  fi
  case "$takes" in
    ''|*[!0-9]*)
      echo "ERROR: --takes must be a positive integer (got '$takes')." >&2
      return 1
      ;;
  esac
  if [ "$takes" -lt 1 ]; then
    echo "ERROR: --takes must be at least 1 (got $takes)." >&2
    return 1
  fi
  if [ "$takes" -gt "$MAX_TAKES" ]; then
    echo "ERROR: --takes is capped at $MAX_TAKES here (got $takes) — this spends real money per take. Run it again if you genuinely want more." >&2
    return 1
  fi
  if [ -z "$prompt_seen" ]; then
    echo "ERROR: --prompt is required." >&2
    return 1
  fi
  validate_concurrency "$concurrency" || return 1
  if [ "$concurrency" -gt "$takes" ]; then
    concurrency="$takes"
  fi

  if [ -n "$seed_given" ] && [ "$takes" -gt 1 ]; then
    echo "NOTE: --seed $seed_given is fixed, so all $takes takes ask for the same generation and you are billed for each. They may still come back different — a fixed seed does not make this API reproducible (measured 2026-09-15) — but the variation is then the server's, not one you chose. Drop --seed to let the takes vary on purpose." >&2
  fi

  # --- estimate before spending ---

  [ -n "$batch_dry" ] && DRY_RUN_ACTIVE=1
  # Same reason as cmd_generate's copy: an unapproved batch is refused below,
  # so its estimate must not promise a bill "reported below".
  [ -z "$batch_approved" ] && DRY_RUN_ACTIVE=1
  print_estimate "$model" "${resolution:-}" "t2v" "${batch_provider:-}" "$duration" "$takes"

  # Validate one take through the real path so a bad parameter is caught here
  # rather than after the first one is paid for. This used to run only under
  # --dry-run; it runs on both paths now, because it has to come BEFORE the
  # spend gate below. A batch with a bad --duration and no --approved would
  # otherwise report the missing approval, and "add --approved and try again"
  # is the last thing to teach someone whose parameters are wrong.
  #
  # Capture the inner call's stderr instead of letting it through: it prints
  # its own single-take estimate, and a caller told "there is exactly one
  # Estimated cost line, relay it" would otherwise see two and quite
  # reasonably relay the last one — the per-take figure this skill spends
  # two documents telling people not to quote. Errors still surface.
  local inner_err
  if ! inner_err="$(cmd_generate ${passthrough[@]+"${passthrough[@]}"} --dry-run 2>&1 >/dev/null)"; then
    printf '%s\n' "$inner_err" >&2
    return 1
  fi

  if [ -n "$batch_dry" ]; then
    echo "DRY RUN — $takes takes would be created one at a time, then waited for concurrently, $concurrency at once. Nothing was billed." >&2
    echo "The figure above is the whole batch. $takes takes means $takes bills, and running them concurrently means they all arrive at once — quote the total before starting, never the per-take figure." >&2
    concurrency_rpm_note "$concurrency" "$poll_interval"
    echo "Re-run without --dry-run to generate." >&2
    echo "STATUS dry_run"
    echo "TAKES_REQUESTED $takes"
    echo "CONCURRENCY $concurrency"
    return 0
  fi

  # Checked here as well as inside each take's cmd_generate. Letting take 1
  # trip the inner guard would work, but it would report a money refusal as
  # "take 1 could not be submitted (exit 1)" — and a batch is N bills, so the
  # one place it can still be stopped is before the first submission.
  require_approved "${SUBCOMMAND:-batch}" "$batch_approved" || return 1

  # --- phase 1: create every take, one at a time ---
  #
  # Sequential on purpose. A create answers in seconds, so this costs almost
  # nothing in wall clock, and it is the only ordering in which "take 2 was
  # rejected, so takes 3..N were never sent" can be true.

  mkdir -p "$out_dir" 2>/dev/null
  local abs_out
  abs_out="$(cd "$out_dir" 2>/dev/null && pwd)" || abs_out="$out_dir"

  local i=1 rc=0 submit_rc=0 stopped=""
  local records=() ids=() seeds=()
  local out line

  # cmd_generate submits and returns instead of waiting, the same mode the
  # `create` subcommand uses. Saved and restored rather than set inline: a
  # variable assignment prefixed to a *function* call is not reliably scoped
  # to that call in bash.
  local prev_submit_only_set="" prev_submit_only=""
  if [ -n "${OFOX_SUBMIT_ONLY+x}" ]; then
    prev_submit_only_set=1
    prev_submit_only="$OFOX_SUBMIT_ONLY"
  fi
  export OFOX_SUBMIT_ONLY=1
  # One "poll this job id yourself" block per take would be N pieces of advice
  # for a wait this function is about to do. It says it once, below, for all of
  # them.
  export OFOX_SUBMIT_QUIET=1

  while [ "$i" -le "$takes" ]; do
    echo "" >&2
    echo "--- creating take $i/$takes ---" >&2
    # Give each take an explicit seed when the caller didn't pick one. Without
    # this, takes differ only by a seed the API chose and never told us, so
    # "take 3 was the good one" cannot even be written down afterwards. With
    # it the take is at least identifiable and re-submittable — NOT
    # reproducible: an identical request on a fixed seed was measured
    # returning a visibly different clip (2026-09-15, see SKILL.md's
    # "Re-attempting a shot"). The seed is a record, not a guarantee.
    local take_args=(${passthrough[@]+"${passthrough[@]}"}) take_seed=""
    if [ -z "$seed_given" ]; then
      take_seed=$(( (RANDOM << 15 | RANDOM) & 0x7FFFFFFF ))
      take_args+=(--seed "$take_seed")
    else
      take_seed="$seed_given"
    fi
    out="$(cmd_generate "${take_args[@]}")"
    rc=$?
    if [ "$rc" -ne 0 ]; then
      submit_rc="$rc"
      echo "" >&2
      echo "Stopping the batch: take $i could not be submitted (exit $rc), so takes $i..$takes were NOT submitted." >&2
      echo "Whatever failed here would almost certainly fail for the rest, and each attempt costs money." >&2
      if [ "$i" -gt 1 ]; then
        echo "Takes 1..$((i - 1)) are already submitted and billable — they are waited for below, not abandoned." >&2
      fi
      stopped="1"
      break
    fi
    local take_id="" take_url="" take_seed_echoed=""
    while IFS= read -r line; do
      case "$line" in
        "JOB_ID "*) take_id="${line#JOB_ID }" ;;
        "POLLING_URL "*) take_url="${line#POLLING_URL }" ;;
        "SEED "*) take_seed_echoed="${line#SEED }" ;;
        "OUT_DIR "*) abs_out="${line#OUT_DIR }" ;;
      esac
    done <<EOF_TAKE
$out
EOF_TAKE
    if [ -z "$take_id" ]; then
      # Submit-only always prints a job id on success, so this cannot happen
      # without something being wrong enough that spending more would be
      # reckless.
      submit_rc=3
      echo "" >&2
      echo "Stopping the batch: take $i reported success but printed no job id, so takes $i..$takes were NOT submitted." >&2
      stopped="1"
      break
    fi
    [ -n "$take_seed_echoed" ] && take_seed="$take_seed_echoed"
    [ -n "$take_url" ] || take_url="$API_BASE/videos/$take_id"
    ids+=("$take_id")
    seeds+=("$take_seed")
    records+=("$(printf '%s\t%s' "$take_id" "$take_url")")
    i=$((i + 1))
  done

  unset OFOX_SUBMIT_QUIET
  if [ -n "$prev_submit_only_set" ]; then
    export OFOX_SUBMIT_ONLY="$prev_submit_only"
  else
    unset OFOX_SUBMIT_ONLY
  fi

  local submitted=${#ids[@]}
  local not_submitted=$(( takes - submitted ))
  if [ "$submitted" -eq 0 ]; then
    echo "ERROR: no takes were submitted." >&2
    return "${submit_rc:-3}"
  fi

  echo "" >&2
  echo "$submitted take(s) submitted and billable from now on, whether or not this command stays open." >&2
  echo "If it is interrupted, resume the downloads with:" >&2
  echo "  $0 poll ${ids[*]} --out-dir $abs_out" >&2

  # --- phase 2: wait for them concurrently ---

  poll_many "$concurrency" "$abs_out" "$max_wait" "$poll_interval" "$name_hint" "take" \
    ${records[@]+"${records[@]}"}

  # Read the results back BY INDEX. Takes finish in whatever order the API
  # feels like, and the seed printed next to take 3 has to be take 3's or the
  # whole "re-render that one" handle is worthless.
  # take_* arrays are indexed by take number (one entry per submitted take,
  # empty where there is nothing); paths/costs are the compacted lists the
  # contact sheet and the total need.
  local paths=() costs=() take_state=() take_rcs=() take_path=() take_cost=()
  local idx=0 completed=0 failed=0 running=0
  while [ "$idx" -lt "$submitted" ]; do
    local t_path="" t_cost="" t_rc="${POLL_MANY_RC[$idx]:-3}"
    while IFS= read -r line; do
      case "$line" in
        "VIDEO_PATH "*) t_path="${line#VIDEO_PATH }" ;;
        "VIDEO_COST "*) t_cost="${line#VIDEO_COST }" ;;
      esac
    done <<EOF_RESULT
${POLL_MANY_OUT[$idx]}
EOF_RESULT
    take_rcs+=("$t_rc")
    take_path+=("$t_path")
    take_cost+=("$t_cost")
    if [ "$t_rc" = "0" ] && [ -n "$t_path" ]; then
      paths+=("$t_path")
      costs+=("${t_cost:-0}")
      take_state+=("completed")
      completed=$((completed + 1))
    elif [ "$t_rc" = "4" ]; then
      # Still running upstream and still billable — the job id below is the
      # only way back to it.
      take_state+=("running")
      running=$((running + 1))
    else
      take_state+=("failed")
      failed=$((failed + 1))
    fi
    idx=$((idx + 1))
  done

  local done_count="$completed"
  if [ "$done_count" -eq 0 ]; then
    echo "ERROR: no takes completed." >&2
    local jid
    for jid in "${ids[@]}"; do
      echo "  submitted job: $jid" >&2
    done
    return 3
  fi

  # --- contact sheet (optional, fail open) ---

  local sheet_path=""
  if [ "$sheet" != "never" ]; then
    sheet_path="$(make_contact_sheet "$out_dir" "${paths[@]}")" || sheet_path=""
  fi

  # --- report: real billing, never the estimate ---

  local total
  total="$(printf '%s\n' ${costs[@]+"${costs[@]}"} | awk '{ s += $1 } END { printf "%.10f", s }')"
  local per
  per="$(awk -v t="$total" -v n="$done_count" 'BEGIN { printf "%.10f", (n ? t/n : 0) }')"

  # batch_completed means exactly that: every requested take is on disk. A
  # partial run says so in the status line rather than leaving an agent to
  # notice the counts disagree.
  if [ "$done_count" -eq "$takes" ]; then
    echo "STATUS batch_completed"
  else
    echo "STATUS batch_partial"
  fi
  echo "TAKES_REQUESTED $takes"
  echo "TAKES_SUBMITTED $submitted"
  echo "TAKES_COMPLETED $done_count"
  [ "$failed" -gt 0 ] && echo "TAKES_FAILED $failed"
  [ "$running" -gt 0 ] && echo "TAKES_RUNNING $running"
  [ "$not_submitted" -gt 0 ] && echo "TAKES_NOT_SUBMITTED $not_submitted"
  # Numbered by take, not by position in the completed list, so a gap is
  # visible and take 3's seed is still take 3's.
  idx=0
  while [ "$idx" -lt "$submitted" ]; do
    case "${take_state[$idx]}" in
      completed)
        echo "TAKE $((idx + 1)) ${ids[$idx]:-unknown} seed=${seeds[$idx]:-unknown} ${take_cost[$idx]:-unknown} ${take_path[$idx]}"
        ;;
      running)
        echo "TAKE $((idx + 1)) ${ids[$idx]:-unknown} seed=${seeds[$idx]:-unknown} RUNNING exit=${take_rcs[$idx]}"
        ;;
      *)
        echo "TAKE $((idx + 1)) ${ids[$idx]:-unknown} seed=${seeds[$idx]:-unknown} FAILED exit=${take_rcs[$idx]}"
        ;;
    esac
    idx=$((idx + 1))
  done
  [ -n "$sheet_path" ] && echo "CONTACT_SHEET $sheet_path"
  echo "BATCH_COST_TOTAL $total"
  echo "BATCH_COST_PER_TAKE $per"
  echo "" >&2
  local total_h
  total_h="$(awk -v t="$total" 'BEGIN { printf "%.2f", t }')"
  echo "" >&2
  echo "Each take carries its seed. To re-render one properly, reuse its seed with the" >&2
  echo "same prompt on the model you actually want:" >&2
  echo "  $0 generate --prompt \"<same prompt>\" --seed <that take's seed> --model bytedance/seedance-2.5 --resolution 1080p" >&2
  echo "" >&2
  echo "That is \$$total_h for $done_count take(s). If only one of them is usable, \$$total_h IS your" >&2
  echo "cost for that one clip — not the per-take figure. That total is the number worth" >&2
  echo "comparing across models and settings." >&2
  if [ "$running" -gt 0 ]; then
    echo "" >&2
    echo "$running take(s) are still running upstream and are billed regardless. Collect them with:" >&2
    idx=0
    while [ "$idx" -lt "$submitted" ]; do
      [ "${take_state[$idx]}" = "running" ] && echo "  $0 poll ${ids[$idx]} --out-dir $abs_out" >&2
      idx=$((idx + 1))
    done
  fi
  if [ "$failed" -gt 0 ]; then
    echo "" >&2
    echo "$failed take(s) failed after being submitted. A job that ends 'failed' carries no usage" >&2
    echo "and is not billed; the block above each failure has its reason." >&2
  fi

  # Nonzero whenever the run is not what was asked for: a stopped submission,
  # a failed take, or one still running. The counts above say which.
  if [ -n "$stopped" ] || [ "$failed" -gt 0 ]; then
    return 3
  fi
  [ "$running" -gt 0 ] && return 4
  return 0
}

rate_for() {
  # $1 = model, $2 = resolution (may be empty), $3 = mode (t2v|v2v),
  # $4 = pinned provider (may be empty).
  #
  # Prints a per-second rate, or nothing when we cannot establish one. Never
  # guesses: an estimate we can't back up is worse than no estimate, because
  # the user acts on it before spending.
  #
  # Source is the catalog's per-resolution tier matrix. The models endpoint's
  # single output_video_per_second is NOT usable here — for seedance-2.5 it
  # reports the 480p rate while the model defaults to 720p, i.e. half the
  # real number.
  local model="$1" res="${2:-}" mode="${3:-t2v}" want_provider="${4:-}"
  local f

  if [ -z "$res" ]; then
    # Fall back to whatever the API itself would default to.
    if load_models 2>/dev/null; then
      local entry
      entry="$(model_entry "$model")"
      [ -n "$entry" ] && res="$(entry_num "$entry" '.video_attributes.default_resolution')"
    fi
    [ -z "$res" ] && return 1
  fi

  f="$(load_catalog "$model" 2>/dev/null)" || f=""
  if [ -z "$f" ] || [ ! -f "$f" ]; then
    f="$PRICING_SNAPSHOT"
    [ -f "$f" ] || return 1
  fi

  # Prefer the pinned provider's own card. Prices matched across providers on
  # 2026-08-30, but that was only ever an observation, and on 2026-09-14 it
  # stopped being true: alibaba/wan-3.0 charges 0.11/s on alicloud and
  # 0.0857/s on aliyun at 720p. So this preference is load-bearing now, not a
  # nicety. With nothing pinned, first() takes the first card in catalog
  # order, which for wan-3.0 is the dearer one — the right direction per
  # "never under-quote", but not a guarantee any future model will keep.
  local price
  price="$(jq -r --arg m "$model" --arg r "$res" --arg t "$mode" --arg p "$want_provider" '
    (.provider_cards // (.models[]? | select(.id == $m) | .provider_cards) // [])
    | (if ($p != "" and any(.[]; .provider_type == $p))
       then map(select(.provider_type == $p)) else . end)
    | first(.[].pricing.video_pricing.tiers[]?
        | select(.resolution == $r and ((.input_type // "t2v") == $t))
        | .price)
    // empty' "$f" 2>/dev/null)"

  [ -n "$price" ] || return 1
  printf '%s' "$price"
}

estimate_note() {
  # $1 = model, $2 = resolution, $3 = mode, $4 = provider, $5 = duration,
  # $6 = takes. Prints a human-readable estimate, or nothing.
  local rate
  rate="$(rate_for "$1" "$2" "$3" "$4")" || return 1
  [ -n "$rate" ] || return 1
  awk -v d="$5" -v n="$6" -v r="$rate" 'BEGIN {
    if (n > 1) printf "~$%.2f for %d takes (%ds x $%s/s x %d)", d*n*r, n, d, r, n;
    else printf "~$%.2f (%ds x $%s/s)", d*r, d, r
  }'
}

# Set to 1 by any subcommand running under --dry-run, so shared helpers can
# tell the difference between "about to spend" and "just quoting".
DRY_RUN_ACTIVE=""

print_estimate() {
  # $1 = model, $2 = resolution, $3 = mode, $4 = provider, $5 = duration,
  # $6 = count.
  #
  # ALWAYS prints exactly one "Estimated cost:" line. Silence is the one
  # outcome a calling agent cannot relay to a user — it can repeat a number,
  # and it can repeat "unavailable", but it cannot notice the absence of a
  # line it was never told to expect.
  local note
  if [ -z "${5:-}" ]; then
    echo "Estimated cost: unavailable — no --duration given, so there is nothing to multiply the per-second rate by. Pass --duration to get a quote up front." >&2
    return 0
  fi
  note="$(estimate_note "$@" 2>/dev/null)" || note=""
  if [ -n "$note" ]; then
    if [ -n "$DRY_RUN_ACTIVE" ]; then
      echo "Estimated cost: $note. This is an estimate — the actual figure comes from the job's own usage once it runs." >&2
    else
      echo "Estimated cost: $note. Actual billing is reported below, from the job's own usage." >&2
    fi
  else
    if [ -n "$DRY_RUN_ACTIVE" ]; then
      echo "Estimated cost: unavailable for this model/resolution combination (no verified rate on hand — run 'ofox-video.sh providers $1')." >&2
    else
      echo "Estimated cost: unavailable for this model/resolution combination (no verified rate on hand — run 'ofox-video.sh providers $1'). Actual billing is reported below." >&2
    fi
  fi
}


make_contact_sheet() {
  # $1 = out dir, $2.. = video paths. Prints the sheet path on stdout when it
  # makes one. Fail open, loudly: a missing ffmpeg costs you the sheet, never
  # the videos you already paid for.
  local out_dir="$1"
  shift
  local videos=("$@")

  if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "NOTE: skipping the contact sheet — ffmpeg is not installed. The videos above are unaffected." >&2
    echo "  macOS: brew install ffmpeg   Debian/Ubuntu: sudo apt-get install ffmpeg" >&2
    return 1
  fi

  local tmpdir rows=() v row i=0
  tmpdir="$(mktemp -d)" || return 1

  for v in "${videos[@]}"; do
    row="$tmpdir/row_$i.png"
    # Three frames per take (roughly first / middle / last) tiled into a strip.
    # -frames:v 1 keeps it to a single output image.
    if ffmpeg -nostdin -loglevel error -i "$v"       -vf "select='eq(n\,0)+gte(t\,0.45*duration)*lt(prev_t\,0.45*duration)+gte(t\,0.9*duration)*lt(prev_t\,0.9*duration)',scale=320:-2,tile=3x1"       -frames:v 1 -y "$row" 2>/dev/null && [ -s "$row" ]; then
      rows+=("$row")
    else
      # Fall back to plain time-sampling if the select filter finds nothing.
      if ffmpeg -nostdin -loglevel error -i "$v"         -vf "fps=1,scale=320:-2,tile=3x1" -frames:v 1 -y "$row" 2>/dev/null && [ -s "$row" ]; then
        rows+=("$row")
      fi
    fi
    i=$((i + 1))
  done

  if [ "${#rows[@]}" -eq 0 ]; then
    echo "NOTE: could not extract frames for the contact sheet; the videos themselves are fine." >&2
    rm -rf "$tmpdir"
    return 1
  fi

  # Report an absolute path, never the relative one the caller happened to
  # pass — a path the reader has to resolve against an unstated working
  # directory is not an answer (see .trellis/spec/skills/index.md).
  local sheet stamp abs_dir
  stamp="$(date +%Y%m%d%H%M%S)"
  abs_dir="$(cd "$out_dir" 2>/dev/null && pwd)" || abs_dir="$out_dir"
  sheet="${abs_dir%/}/contact-sheet-${stamp}.png"
  if [ "${#rows[@]}" -eq 1 ]; then
    cp "${rows[0]}" "$sheet" || return 1
  else
    local args=() n=${#rows[@]}
    for row in "${rows[@]}"; do args+=(-i "$row"); done
    if ! ffmpeg -nostdin -loglevel error "${args[@]}"       -filter_complex "vstack=inputs=$n" -y "$sheet" 2>/dev/null; then
      echo "NOTE: extracted the frames but could not stack them into one sheet; the videos are fine." >&2
      rm -rf "$tmpdir"
      return 1
    fi
  fi

  rm -rf "$tmpdir"
  [ -s "$sheet" ] || return 1
  printf '%s' "$sheet"
  return 0
}

extract_last_frame() {
  # $1 = video, $2 = destination png. Grabs a frame slightly BEFORE the end
  # rather than the literal final one: trailing frames are often a fade or a
  # black frame, which would make the next shot open on nothing.
  local video="$1" dest="$2" dur seek

  dur="$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 \
    "$video" 2>/dev/null)" || dur=""

  if [ -n "$dur" ]; then
    seek="$(awk -v d="$dur" 'BEGIN { t = d - 0.1; if (t < 0) t = 0; printf "%.3f", t }')"
    if ffmpeg -nostdin -loglevel error -ss "$seek" -i "$video" \
      -frames:v 1 -y "$dest" 2>/dev/null && [ -s "$dest" ]; then
      return 0
    fi
  fi

  # Fall back to the true last frame if seeking didn't land one.
  if ffmpeg -nostdin -loglevel error -sseof -0.5 -i "$video" \
    -update 1 -frames:v 1 -y "$dest" 2>/dev/null && [ -s "$dest" ]; then
    return 0
  fi
  return 1
}

cmd_last_frame() {
  # Pull the closing frame out of a clip. No API call, no key, no cost —
  # useful on its own for feeding a frame into a later generate.
  local video="" out_dir=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --out-dir)
        [ $# -lt 2 ] && { echo "ERROR: --out-dir requires a value." >&2; return 1; }
        out_dir="$2"; shift 2
        ;;
      -*)
        echo "ERROR: unknown option '$1' for last-frame." >&2
        return 1
        ;;
      *)
        video="$1"; shift
        ;;
    esac
  done

  if [ -z "$video" ]; then
    echo "ERROR: give a video file. Usage: ofox-video.sh last-frame VIDEO [--out-dir DIR]" >&2
    return 1
  fi
  if [ ! -r "$video" ]; then
    echo "ERROR: cannot read '$video'." >&2
    return 1
  fi
  if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "ERROR: ffmpeg is required to extract a frame." >&2
    echo "  macOS: brew install ffmpeg   Debian/Ubuntu: sudo apt-get install ffmpeg" >&2
    return 2
  fi

  [ -z "$out_dir" ] && out_dir="$(dirname "$video")"
  mkdir -p "$out_dir" 2>/dev/null
  local abs_dir base dest
  abs_dir="$(cd "$out_dir" 2>/dev/null && pwd)" || abs_dir="$out_dir"
  base="$(basename "$video")"
  dest="${abs_dir%/}/${base%.*}-lastframe.png"

  if ! extract_last_frame "$video" "$dest"; then
    echo "ERROR: could not extract a frame from '$video'." >&2
    return 3
  fi
  echo "LAST_FRAME $dest"
  return 0
}

probe_duration() {
  # Seconds as a decimal, or empty if ffprobe is absent or the file has no
  # readable duration. Callers must cope with empty rather than assume.
  ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 \
    "$1" 2>/dev/null | head -1
}

cmd_frame_at() {
  # Pull the frame at a given second out of a clip. Same zero-cost local shape
  # as last-frame, but this one sits ON the spending path: what it writes gets
  # fed straight into a paid image-to-video job. So --at is required rather
  # than defaulted (a guessed timestamp is a job billed for the wrong picture),
  # and a timestamp past the end is an error rather than an empty file.
  local video="" out_dir="" at=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --at)
        [ $# -lt 2 ] && { echo "ERROR: --at requires a value in seconds." >&2; return 1; }
        at="$2"; shift 2
        ;;
      --out-dir)
        [ $# -lt 2 ] && { echo "ERROR: --out-dir requires a value." >&2; return 1; }
        out_dir="$2"; shift 2
        ;;
      -*)
        echo "ERROR: unknown option '$1' for frame-at." >&2
        return 1
        ;;
      *)
        video="$1"; shift
        ;;
    esac
  done

  if [ -z "$video" ]; then
    echo "ERROR: give a video file. Usage: ofox-video.sh frame-at VIDEO --at SECONDS [--out-dir DIR]" >&2
    return 1
  fi
  if [ ! -r "$video" ]; then
    echo "ERROR: cannot read '$video'." >&2
    return 1
  fi
  if [ -z "$at" ]; then
    echo "ERROR: --at SECONDS is required — say which second to grab." >&2
    echo "  For the closing frame use 'last-frame' instead; it steps back off the final frame, which is often a fade." >&2
    return 1
  fi
  case "$at" in
    *[!0-9.]* | "" | *.*.* | .)
      echo "ERROR: --at must be a non-negative number of seconds, got '$at'." >&2
      return 1
      ;;
  esac
  if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "ERROR: ffmpeg is required to extract a frame." >&2
    echo "  macOS: brew install ffmpeg   Debian/Ubuntu: sudo apt-get install ffmpeg" >&2
    return 2
  fi

  # Refuse a timestamp past the end up front, and say how long the clip is.
  # Left to ffmpeg this is a silent no-op that writes nothing, and the caller
  # finds out by submitting a paid job with a missing frame.
  local dur
  dur="$(probe_duration "$video")"
  if [ -n "$dur" ] && awk -v a="$at" -v d="$dur" 'BEGIN { exit !(a >= d) }'; then
    echo "ERROR: --at $at is past the end of '$video' (duration ${dur}s)." >&2
    echo "  For the closing frame use 'last-frame'." >&2
    return 1
  fi

  [ -z "$out_dir" ] && out_dir="$(dirname "$video")"
  mkdir -p "$out_dir" 2>/dev/null
  local abs_dir base stamp dest
  abs_dir="$(cd "$out_dir" 2>/dev/null && pwd)" || abs_dir="$out_dir"
  base="$(basename "$video")"
  stamp="$(printf '%s' "$at" | tr '.' 'p')"
  dest="${abs_dir%/}/${base%.*}-frame-${stamp}s.png"

  if ! ffmpeg -nostdin -loglevel error -ss "$at" -i "$video" \
    -update 1 -frames:v 1 -y "$dest" 2>/dev/null || [ ! -s "$dest" ]; then
    rm -f "$dest" 2>/dev/null
    echo "ERROR: could not extract a frame at ${at}s from '$video'." >&2
    return 3
  fi
  echo "FRAME_AT $dest"
  return 0
}

cmd_mux_audio() {
  # Put your own audio track on a clip. No API call, no key, no cost — the
  # terminal step for anything scored to music the caller already has, because
  # an audio reference sent to the API does not come back as the clip's audio
  # (measured; see references/api-params.md).
  #
  # Replaces the clip's own track rather than mixing with it: generated clips
  # arrive with a model-made soundtrack, and layering two is never what the
  # caller meant.
  local video="" audio="" out_dir=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --out-dir)
        [ $# -lt 2 ] && { echo "ERROR: --out-dir requires a value." >&2; return 1; }
        out_dir="$2"; shift 2
        ;;
      -*)
        echo "ERROR: unknown option '$1' for mux-audio." >&2
        return 1
        ;;
      *)
        if [ -z "$video" ]; then video="$1"; else audio="$1"; fi
        shift
        ;;
    esac
  done

  if [ -z "$video" ] || [ -z "$audio" ]; then
    echo "ERROR: give a video and an audio file. Usage: ofox-video.sh mux-audio VIDEO AUDIO [--out-dir DIR]" >&2
    return 1
  fi
  local f
  for f in "$video" "$audio"; do
    if [ ! -r "$f" ]; then
      echo "ERROR: cannot read '$f'." >&2
      return 1
    fi
  done
  if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "ERROR: ffmpeg is required to mux audio." >&2
    echo "  macOS: brew install ffmpeg   Debian/Ubuntu: sudo apt-get install ffmpeg" >&2
    return 2
  fi

  [ -z "$out_dir" ] && out_dir="$(dirname "$video")"
  mkdir -p "$out_dir" 2>/dev/null
  local abs_dir base dest
  abs_dir="$(cd "$out_dir" 2>/dev/null && pwd)" || abs_dir="$out_dir"
  base="$(basename "$video")"
  dest="${abs_dir%/}/${base%.*}-with-audio.mp4"

  # The result runs to the shorter of the two. That is a real loss of someone
  # else's material, so it is reported rather than swallowed — a note, not a
  # failure, because a slightly-off pair is still the file they asked for.
  local vdur adur
  vdur="$(probe_duration "$video")"
  adur="$(probe_duration "$audio")"
  if [ -n "$vdur" ] && [ -n "$adur" ]; then
    awk -v v="$vdur" -v a="$adur" 'BEGIN {
      d = v - a; if (d < 0) d = -d
      if (d <= 0.5) exit 0
      if (a > v)
        printf "NOTE: the audio is %.1fs and the picture is %.1fs — the result runs %.1fs and the audio is truncated by %.1fs.\n", a, v, v, d
      else
        printf "NOTE: the picture is %.1fs and the audio is %.1fs — the result runs %.1fs; the picture is truncated by %.1fs.\n", v, a, a, d
      exit 0
    }' >&2
  fi

  if ! ffmpeg -nostdin -loglevel error -i "$video" -i "$audio" \
    -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -shortest \
    -y "$dest" 2>/dev/null || [ ! -s "$dest" ]; then
    rm -f "$dest" 2>/dev/null
    echo "ERROR: could not mux '$audio' onto '$video'." >&2
    return 3
  fi
  echo "MUXED $dest"
  return 0
}

# ---------------------------------------------------------------------------
# chain: N shots, each opening on the previous shot's closing frame
#
# One job is one 4-30s clip, and a clip CAN hold several shots joined by hard
# cuts written as timestamps (verified 2026-09-03 — see "Several shots in one
# job" in references/prompt-structure.md). So this subcommand is not "the way
# to get multiple shots": it is continuity ACROSS jobs, for a sequence past the
# duration ceiling or when each shot needs its own approval, seed or
# resolution. Separate jobs share nothing, so the character, set and lighting
# drift between them; feeding shot N-1's last frame in as shot N's first frame
# is the lever this API gives you against that. The two compose — each job in a
# chain can itself carry several timestamped shots.
#
# Same house rules as batch: estimate before spending, one job at a time via
# cmd_generate (no-resubmit holds for free), stop on first failure, report real
# per-job cost.
# ---------------------------------------------------------------------------

MAX_SHOTS=10

shot_looks_like_prompt_fragment() {
  # True when a --shots-file line opens with an ALL-CAPS label ("STYLE:",
  # "AVOID:", "CONTINUES FROM:") — the shape of one line lifted out of a
  # multi-line templated prompt, which references/prompt-structure.md teaches
  # and every scenario skill writes. A shots file is one prompt per LINE, so
  # such a file silently becomes one separately billed job per label. This is
  # the cheapest reliable signal: no whole one-line shot prompt opens with a
  # bare uppercase label, while every template line does.
  #
  # POSIX classes rather than [A-Z]: a glob range is collation-ordered in some
  # locales and would match lowercase too. Digits are deliberately excluded, so
  # "SHOT 1: ..." — a plausible way to write a real one-line prompt — passes.
  local line="$1" label
  case "$line" in
    *:*) ;;
    *) return 1 ;;
  esac
  label="${line%%:*}"
  [ -z "$label" ] && return 1
  case "$label" in
    [[:upper:]]*) ;;
    *) return 1 ;;
  esac
  case "$label" in
    *[![:upper:][:space:]]*) return 1 ;;
  esac
  return 0
}

cmd_chain() {
  local shots=() shots_file="" out_dir="$PWD" duration="" resolution=""
  local model="$DEFAULT_MODEL" concat="auto" aspect="" chain_dry="" chain_approved=""
  local chain_name=""
  local passthrough=() key val

  while [ $# -gt 0 ]; do
    key="$1"
    case "$key" in
      --shot)
        [ $# -lt 2 ] && { echo "ERROR: --shot requires a value." >&2; return 1; }
        shots+=("$2"); shift 2; continue
        ;;
      --shots-file)
        [ $# -lt 2 ] && { echo "ERROR: --shots-file requires a value." >&2; return 1; }
        shots_file="$2"; shift 2; continue
        ;;
      --no-concat)
        concat="never"; shift; continue
        ;;
      --dry-run)
        chain_dry=1; shift; continue
        ;;
      --approved)
        # Forwarded as well as recorded, for the same reason batch forwards it.
        chain_approved=1; passthrough+=("$key"); shift; continue
        ;;
      --print-payload)
        passthrough+=("$key"); shift; continue
        ;;
      *)
        if [ $# -lt 2 ]; then
          echo "ERROR: $key requires a value." >&2
          return 1
        fi
        val="$2"
        case "$key" in
          --out-dir) out_dir="$val" ;;
          --duration) duration="$val" ;;
          --resolution) resolution="$val" ;;
          --model) model="$val" ;;
          --aspect-ratio) aspect="$val" ;;
          --name) chain_name="$val" ;;
        esac
        passthrough+=("$key" "$val")
        shift 2
        ;;
    esac
  done

  if [ -n "$shots_file" ]; then
    if [ ! -r "$shots_file" ]; then
      echo "ERROR: cannot read --shots-file '$shots_file'." >&2
      return 1
    fi
    local line lineno=0 file_shots=0 frag_count=0 frag_line="" frag_no=""
    while IFS= read -r line || [ -n "$line" ]; do
      lineno=$((lineno + 1))
      case "$line" in
        ''|'#'*) continue ;;
      esac
      shots+=("$line")
      file_shots=$((file_shots + 1))
      if shot_looks_like_prompt_fragment "$line"; then
        frag_count=$((frag_count + 1))
        if [ -z "$frag_no" ]; then
          frag_no="$lineno"
          frag_line="$line"
        fi
      fi
    done < "$shots_file"

    # Refuse before the estimate, for the same reason the ffmpeg check sits
    # ahead of shot 1: a fragment submitted as a prompt is a full-price job
    # bought for a quarter of a sentence, and the estimate it would print looks
    # entirely plausible. Stopping is the whole fix — re-joining the lines would
    # be guessing at someone's intent with their money.
    if [ "$frag_count" -gt 0 ]; then
      echo "ERROR: --shots-file '$shots_file' line $frag_no reads as part of a multi-line prompt, not as a shot of its own:" >&2
      echo "    $frag_line" >&2
      echo "  --shots-file is one prompt per line: every non-blank line becomes its own separately billed job, so a templated prompt written across several lines is submitted as several fragments ($frag_count of $file_shots lines here open with an ALL-CAPS label)." >&2
      echo "  Pass one --shot per prompt instead — a repeated --shot takes a multi-line value as a single prompt:" >&2
      echo "    ofox-video.sh chain --shot \"\$(cat shot1.txt)\" --shot \"\$(cat shot2.txt)\" --duration 8" >&2
      echo "  That is also the answer if the line really is a whole prompt that happens to open with a label ('CLOSE UP: ...'): --shot takes it as written, no file involved." >&2
      echo "  Nothing was submitted and nothing was billed." >&2
      return 1
    fi
  fi

  if [ "${#shots[@]}" -eq 0 ]; then
    echo "ERROR: give at least one --shot, or a --shots-file with one prompt per line." >&2
    return 1
  fi
  if [ "${#shots[@]}" -gt "$MAX_SHOTS" ]; then
    echo "ERROR: chain is capped at $MAX_SHOTS shots (got ${#shots[@]}) — each shot is a separately billed job." >&2
    return 1
  fi

  # Chaining is impossible without frame extraction, and finding that out
  # after paying for shot 1 would be the wrong time.
  if ! command -v ffmpeg >/dev/null 2>&1 && [ "${#shots[@]}" -gt 1 ]; then
    echo "ERROR: chain needs ffmpeg to carry each shot's closing frame into the next." >&2
    echo "  macOS: brew install ffmpeg   Debian/Ubuntu: sudo apt-get install ffmpeg" >&2
    echo "  Without it, generate each shot separately with 'generate' instead." >&2
    return 2
  fi

  local n=${#shots[@]}
  echo "Chaining $n shots. Each shot after the first opens on the previous shot's closing frame." >&2
  # What happens to shots 2+ is model-dependent: seedance-2.5 is forced to
  # 'adaptive' by the API, every other model only defaults to it when the
  # caller named no ratio and its catalog entry offers it. Each shot's own
  # generate call prints exactly which of those it did — this is the
  # sequence-level summary, so it must not claim more than the model gives.
  if [ "$n" -gt 1 ]; then
    if [ "$model" = "bytedance/seedance-2.5" ] && [ -n "$aspect" ]; then
      echo "NOTE: --aspect-ratio $aspect applies to shot 1 only. Shots 2+ are image-to-video, which $model requires to be 'adaptive' — they inherit their framing from the fed frame, so the sequence stays dimensionally consistent." >&2
    elif [ -n "$aspect" ]; then
      echo "NOTE: --aspect-ratio $aspect is passed to every shot, including the image-to-video ones (2+). A model that requires 'adaptive' there overrides it; a model that merely offers 'adaptive' keeps your value. Each shot prints which of those it did — omit --aspect-ratio to let shots 2+ inherit the fed frame's shape instead." >&2
    else
      echo "NOTE: shots 2+ are image-to-video and inherit their framing from the fed frame wherever the model offers 'adaptive' — each shot prints which it did, so the sequence stays dimensionally consistent." >&2
    fi
  fi

  [ -n "$chain_dry" ] && DRY_RUN_ACTIVE=1
  [ -z "$chain_approved" ] && DRY_RUN_ACTIVE=1
  print_estimate "$model" "${resolution:-}" "t2v" "" "$duration" "$n"

  # Shot 1 through the real path, stopping before the request. Like batch's
  # copy of this, it used to run only under --dry-run and now runs on both
  # paths, so that a bad parameter is reported as a bad parameter rather than
  # as a missing approval.
  local inner_err
  if ! inner_err="$(cmd_generate ${passthrough[@]+"${passthrough[@]}"} --prompt "${shots[0]}" --dry-run 2>&1 >/dev/null)"; then
    printf '%s\n' "$inner_err" >&2
    return 1
  fi

  if [ -n "$chain_dry" ]; then
    echo "DRY RUN — $n shots would be submitted in sequence. Nothing was billed." >&2
    echo "Re-run without --dry-run to generate." >&2
    echo "STATUS dry_run"
    echo "SHOTS_REQUESTED $n"
    return 0
  fi

  # Same reasoning as batch: a chain is N bills, and shot 1 tripping the inner
  # guard would be reported as "shot 1 failed (exit 1)" rather than as a money
  # refusal.
  require_approved "${SUBCOMMAND:-chain}" "$chain_approved" || return 1

  mkdir -p "$out_dir" 2>/dev/null
  local abs_out
  abs_out="$(cd "$out_dir" 2>/dev/null && pwd)" || abs_out="$out_dir"

  local i=1 rc=0 stopped="" prev_frame=""
  local paths=() costs=() ids=() out line
  while [ "$i" -le "$n" ]; do
    echo "" >&2
    echo "--- shot $i/$n ---" >&2

    local args=(${passthrough[@]+"${passthrough[@]}"} --prompt "${shots[$((i - 1))]}" --out-dir "$abs_out")
    # A chain's shots are meant to be watched — and concatenated — in order,
    # so when the caller named the chain, number the shots inside that name.
    # Without it every shot would share one slug and differ only by job id,
    # losing the ordering. This --name comes after passthrough's copy, and
    # generate's parser takes the last occurrence.
    [ -n "$chain_name" ] && args+=(--name "${chain_name}-shot${i}")
    [ -n "$prev_frame" ] && args+=(--frame-first-image "$prev_frame")

    out="$(cmd_generate "${args[@]}")"
    rc=$?
    if [ "$rc" -ne 0 ]; then
      echo "" >&2
      echo "Stopping the chain: shot $i failed (exit $rc), so shots $i..$n were NOT submitted." >&2
      echo "Shots already generated are kept and listed below." >&2
      stopped="1"
      break
    fi

    local shot_path=""
    while IFS= read -r line; do
      case "$line" in
        "VIDEO_PATH "*) shot_path="${line#VIDEO_PATH }"; paths+=("$shot_path") ;;
        "VIDEO_COST "*) costs+=("${line#VIDEO_COST }") ;;
        "JOB_ID "*) ids+=("${line#JOB_ID }") ;;
      esac
    done <<EOF_SHOT
$out
EOF_SHOT

    if [ "$i" -lt "$n" ]; then
      if [ -z "$shot_path" ]; then
        echo "Stopping the chain: shot $i reported no video path, so there is no frame to carry forward." >&2
        stopped="1"
        rc=3
        break
      fi
      prev_frame="${abs_out%/}/chain-frame-$i.png"
      if ! extract_last_frame "$shot_path" "$prev_frame"; then
        echo "Stopping the chain: could not extract a closing frame from shot $i." >&2
        echo "The shots generated so far are kept and listed below." >&2
        stopped="1"
        rc=3
        break
      fi
      echo "Carrying shot $i's closing frame into shot $((i + 1)): $prev_frame" >&2
    fi
    i=$((i + 1))
  done

  local done_count=${#paths[@]}
  if [ "$done_count" -eq 0 ]; then
    echo "ERROR: no shots completed." >&2
    return "${rc:-3}"
  fi

  local joined=""
  if [ "$concat" != "never" ] && [ "$done_count" -gt 1 ]; then
    joined="$(concat_clips "$abs_out" "${paths[@]}")" || joined=""
  fi

  local total per
  total="$(printf '%s\n' ${costs[@]+"${costs[@]}"} | awk '{ s += $1 } END { printf "%.10f", s }')"
  per="$(awk -v t="$total" -v n="$done_count" 'BEGIN { printf "%.10f", (n ? t/n : 0) }')"

  echo "STATUS chain_completed"
  echo "SHOTS_REQUESTED $n"
  echo "SHOTS_COMPLETED $done_count"
  local idx=0
  while [ "$idx" -lt "$done_count" ]; do
    echo "SHOT $((idx + 1)) ${ids[$idx]:-unknown} ${costs[$idx]:-unknown} ${paths[$idx]}"
    idx=$((idx + 1))
  done
  [ -n "$joined" ] && echo "JOINED $joined"
  echo "CHAIN_COST_TOTAL $total"
  echo "CHAIN_COST_PER_SHOT $per"

  [ -n "$stopped" ] && return 3
  return 0
}

concat_clips() {
  # $1 = out dir, $2.. = clips in order. Prints the joined file path.
  # Fail open: losing the join must never cost the clips already paid for.
  local out_dir="$1"
  shift
  local clips=("$@")

  if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "NOTE: skipping the join — ffmpeg is not installed. The shots above are unaffected." >&2
    return 1
  fi

  local listfile stamp joined clip
  listfile="$(mktemp)" || return 1
  for clip in "${clips[@]}"; do
    # The concat demuxer needs escaped single quotes in paths.
    printf "file '%s'\n" "$(printf '%s' "$clip" | sed "s/'/'\\\\''/g")" >> "$listfile"
  done

  stamp="$(date +%Y%m%d%H%M%S)"
  joined="${out_dir%/}/chain-joined-${stamp}.mp4"
  if ffmpeg -nostdin -loglevel error -f concat -safe 0 -i "$listfile" \
    -c copy -y "$joined" 2>/dev/null && [ -s "$joined" ]; then
    rm -f "$listfile"
    printf '%s' "$joined"
    return 0
  fi

  # Stream copy fails when the clips differ in codec/params; re-encode once.
  if ffmpeg -nostdin -loglevel error -f concat -safe 0 -i "$listfile" \
    -c:v libx264 -preset veryfast -pix_fmt yuv420p -y "$joined" 2>/dev/null &&
    [ -s "$joined" ]; then
    rm -f "$listfile"
    echo "NOTE: the shots needed re-encoding to join (their codecs differed)." >&2
    printf '%s' "$joined"
    return 0
  fi

  rm -f "$listfile" "$joined"
  echo "NOTE: could not join the shots into one file; they are all listed above and playable individually." >&2
  return 1
}

cmd_contact_sheet() {
  # Build a contact sheet from videos already on disk. No API call, no cost —
  # useful for re-tiling takes you already paid for, or for comparing clips
  # that came from separate runs.
  local out_dir="" videos=()
  while [ $# -gt 0 ]; do
    case "$1" in
      --out-dir)
        [ $# -lt 2 ] && { echo "ERROR: --out-dir requires a value." >&2; return 1; }
        out_dir="$2"; shift 2
        ;;
      -*)
        echo "ERROR: unknown option '$1' for contact-sheet." >&2
        return 1
        ;;
      *)
        videos+=("$1"); shift
        ;;
    esac
  done

  if [ "${#videos[@]}" -eq 0 ]; then
    echo "ERROR: give at least one video file. Usage: ofox-video.sh contact-sheet VIDEO [VIDEO...] [--out-dir DIR]" >&2
    return 1
  fi
  local v
  for v in "${videos[@]}"; do
    if [ ! -r "$v" ]; then
      echo "ERROR: cannot read '$v'." >&2
      return 1
    fi
  done
  if [ -z "$out_dir" ]; then
    out_dir="$(dirname "${videos[0]}")"
  fi
  mkdir -p "$out_dir" 2>/dev/null

  local sheet
  sheet="$(make_contact_sheet "$out_dir" "${videos[@]}")" || return 3
  echo "CONTACT_SHEET $sheet"
  return 0
}

# ---------------------------------------------------------------------------
# poll: resume polling / download for an existing job id (no create call)
# ---------------------------------------------------------------------------

# `poll` takes one job id or several. Several is what makes cross-clip
# fan-out usable: N independent `create` calls, then one command that waits on
# all of them at once. Sequentially, four 15-second clips is 40 minutes of
# waiting for 10 minutes of generation.
#
# One id behaves exactly as it always has — same call, same stdout, no
# subshell — because every existing caller and test depends on that shape.
cmd_poll() {
  if ! check_curl_jq; then return 2; fi

  local ids=()
  local out_dir="$PWD"
  local max_wait="$DEFAULT_MAX_WAIT"
  local poll_interval="$DEFAULT_POLL_INTERVAL"
  local name_hint=""
  local concurrency="$DEFAULT_CONCURRENCY"
  local key val

  while [ $# -gt 0 ]; do
    key="$1"
    case "$key" in
      --out-dir|--max-wait|--poll-interval|--name|--concurrency)
        if [ $# -lt 2 ]; then
          echo "ERROR: $key requires a value." >&2
          return 1
        fi
        val="$2"
        shift 2
        ;;
      --*)
        echo "ERROR: unknown option '$key' for poll." >&2
        return 1
        ;;
      *)
        # Anything that is not a flag is a job id. Ids may come before the
        # flags or after them; a bare word is never ambiguous here.
        ids+=("$key")
        shift
        continue
        ;;
    esac
    case "$key" in
      --out-dir) out_dir="$val" ;;
      --max-wait) max_wait="$val" ;;
      --poll-interval) poll_interval="$val" ;;
      --name) name_hint="$val" ;;
      --concurrency) concurrency="$val" ;;
    esac
  done

  if [ "${#ids[@]}" -eq 0 ]; then
    echo "ERROR: 'poll' requires a job id, e.g. $0 poll abc123 — or several: $0 poll abc123 def456" >&2
    return 1
  fi

  # A repeated id would be polled twice and downloaded twice onto the same
  # filename. That is a typo every time, not a request.
  local unique=() id
  for id in "${ids[@]}"; do
    if list_contains "$id" "${unique[*]+${unique[*]}}"; then
      echo "NOTE: job id $id was given more than once; polling it once." >&2
    else
      unique+=("$id")
    fi
  done
  ids=("${unique[@]}")

  if ! check_api_key; then return 2; fi

  # No request payload to pass: a poll knows only what the response reports,
  # so the sidecar it writes omits the resolution/aspect-ratio half.
  if [ "${#ids[@]}" -eq 1 ]; then
    poll_and_download "${ids[0]}" "$API_BASE/videos/${ids[0]}" "$out_dir" "$max_wait" \
      "$poll_interval" "$name_hint"
    return $?
  fi

  validate_concurrency "$concurrency" || return 1
  [ "$concurrency" -gt "${#ids[@]}" ] && concurrency="${#ids[@]}"

  mkdir -p "$out_dir" 2>/dev/null
  local abs_out
  abs_out="$(cd "$out_dir" 2>/dev/null && pwd)"
  if [ -z "$abs_out" ]; then
    echo "ERROR: --out-dir '$out_dir' could not be created or entered (bad path or missing permissions)." >&2
    echo "None of the jobs were affected — fix the path and poll them again." >&2
    return 6
  fi

  local records=()
  for id in "${ids[@]}"; do
    records+=("$(printf '%s\t%s' "$id" "$API_BASE/videos/$id")")
  done

  poll_many "$concurrency" "$abs_out" "$max_wait" "$poll_interval" "$name_hint" "job" \
    "${records[@]}"

  # Replay each job's own stdout, in the order the ids were given, under a
  # delimiter. Verbatim, so VIDEO_PATH / VIDEO_COST / SIDECAR_PATH still read
  # exactly as they do for a single poll — an agent relaying paths does not
  # have to learn a second output shape.
  local n="${#ids[@]}" idx=0 completed=0 failed=0 running=0
  local costs=() rc
  while [ "$idx" -lt "$n" ]; do
    rc="${POLL_MANY_RC[$idx]:-3}"
    echo "=== JOB $((idx + 1))/$n ${ids[$idx]} ==="
    [ -n "${POLL_MANY_OUT[$idx]}" ] && printf '%s\n' "${POLL_MANY_OUT[$idx]}"
    case "$rc" in
      0) completed=$((completed + 1)) ;;
      4) running=$((running + 1)) ;;
      *) failed=$((failed + 1)) ;;
    esac
    local line
    while IFS= read -r line; do
      case "$line" in
        "VIDEO_COST "*) costs+=("${line#VIDEO_COST }") ;;
      esac
    done <<EOF_JOB
${POLL_MANY_OUT[$idx]}
EOF_JOB
    idx=$((idx + 1))
  done

  local total
  total="$(printf '%s\n' ${costs[@]+"${costs[@]}"} | awk '{ s += $1 } END { printf "%.10f", s }')"

  if [ "$completed" -eq "$n" ]; then
    echo "STATUS poll_completed"
  else
    echo "STATUS poll_partial"
  fi
  echo "JOBS_REQUESTED $n"
  echo "JOBS_COMPLETED $completed"
  [ "$failed" -gt 0 ] && echo "JOBS_FAILED $failed"
  [ "$running" -gt 0 ] && echo "JOBS_RUNNING $running"
  echo "POLL_COST_TOTAL $total"

  if [ "$running" -gt 0 ]; then
    echo "" >&2
    echo "$running job(s) had not finished within --max-wait and are still billable. Re-poll them:" >&2
    idx=0
    while [ "$idx" -lt "$n" ]; do
      [ "${POLL_MANY_RC[$idx]:-3}" = "4" ] && echo "  $0 poll ${ids[$idx]} --out-dir $abs_out" >&2
      idx=$((idx + 1))
    done
  fi

  # Most severe actionable state wins: a failure needs a new prompt, a
  # timeout needs another poll, and those are different instructions.
  [ "$failed" -gt 0 ] && return 3
  [ "$running" -gt 0 ] && return 4
  return 0
}

# ---------------------------------------------------------------------------
# shared polling + download loop
# ---------------------------------------------------------------------------

poll_and_download() {
  local job_id="$1" polling_url="$2" out_dir="$3" max_wait="$4" poll_interval="$5"
  # Both optional; only the generate path has them to give. See
  # download_result() and write_sidecar().
  local name_hint="${6:-}" request_json="${7:-}"
  # Wall clock, not a tally of sleeps. Each poll request can now itself burn
  # up to POLL_MAX_TIME before returning, so counting only poll_interval per
  # iteration would let a run of slow or timing-out requests overshoot
  # --max-wait by minutes while believing it was well inside it.
  local poll_started elapsed=0 tmp_body http_code curl_rc body status
  # Consecutive 429s only. Concurrent polls share one account-wide rate
  # limit, so a 429 means the session is over budget, not that this job is
  # unlucky — retrying at the same cadence keeps it over budget. Any response
  # that gets through resets this to 0.
  local rate_limit_hits=0

  # Second line of defence for the same thing cmd_generate checks: every
  # request below carries the API key, and this function is reached with a URL
  # its caller chose. cmd_poll and cmd_batch build that URL from API_BASE, and
  # cmd_generate has already screened the one the response supplied — but the
  # check belongs next to the request that would leak, not only next to the
  # place the URL came from, because a future caller will not remember.
  if ! assert_same_origin_as_api_base "$polling_url" "polling URL"; then
    echo "Job $job_id was NOT polled and was not affected by this. Do NOT re-run 'generate' — collect it with:" >&2
    echo "  $0 poll $job_id --out-dir $out_dir" >&2
    return 3
  fi

  poll_started=$(date +%s)
  local out_dir_input="$out_dir"

  mkdir -p "$out_dir" 2>/dev/null

  # Resolve out_dir to an absolute, canonical path before it's used to build
  # any output path in download_result(). A caller-supplied relative
  # --out-dir (e.g. '.' or 'some/subdir') must never leak into a printed
  # VIDEO_PATH — the location of the downloaded file is this skill's actual
  # deliverable. Portable bash builtins only, no readlink -f/realpath
  # dependency (matches the curl+jq-only contract).
  out_dir=$(cd "$out_dir" 2>/dev/null && pwd)
  if [ -z "$out_dir" ]; then
    echo "ERROR: --out-dir '$out_dir_input' could not be created or entered (bad path or missing permissions)." >&2
    echo "Job $job_id was not affected by this — it may already exist or still be running server-side." >&2
    echo "Do NOT re-run 'generate' for the same request. Fix --out-dir to a writable directory and re-run:" >&2
    echo "  $0 poll $job_id --out-dir <a writable directory>" >&2
    return 6
  fi

  while [ "$elapsed" -lt "$max_wait" ]; do
    tmp_body=$(mktemp)
    http_code=$(curl -sS -o "$tmp_body" -w '%{http_code}' \
      --connect-timeout "$CONNECT_TIMEOUT" --max-time "$POLL_MAX_TIME" \
      -H "Authorization: Bearer $OFOX_API_KEY" \
      "$polling_url")
    curl_rc=$?
    body=$(cat "$tmp_body")
    rm -f "$tmp_body"

    if [ "$curl_rc" -ne 0 ]; then
      echo "WARN: poll request failed (curl exit $curl_rc). Retrying the POLL (not create) in ${poll_interval}s..." >&2
      sleep "$poll_interval"
      elapsed=$(( $(date +%s) - poll_started ))
      continue
    fi

    case "$http_code" in
      200)
        status=$(printf '%s' "$body" | jq -r '.status // empty')
        case "$status" in
          completed)
            # A poll invoked on its own has no payload of its own; pick up
            # the one create left behind, if this is the out-dir it left it
            # in. Nothing here is fatal — a missing handoff just means the
            # sidecar omits its request half.
            if [ -z "$request_json" ]; then
              request_json=$(load_request_handoff "$out_dir" "$job_id") || request_json=""
            fi
            # download_result clears the handoff itself, and only once a
            # sidecar has actually been written — see the note there.
            download_result "$job_id" "$body" "$out_dir" "$name_hint" "$request_json"
            return $?
            ;;
          failed|cancelled|expired)
            echo "ERROR: job $job_id ended with status '$status'." >&2
            print_error_message "$(printf '%s' "$body" | jq -r '.error.code // empty')"
            # Same rule as print_api_error(): a terminal failed/cancelled/
            # expired job can carry a useful error.message even when the
            # response itself was a normal HTTP 200 (this is exactly how
            # output_moderation_failed was first found — a 200 poll response
            # with a job-level failure, not an HTTP-level error) — never
            # swallow it.
            local job_message
            job_message=$(printf '%s' "$body" | jq -r '.error.message // empty' 2>/dev/null)
            if [ -n "$job_message" ]; then
              echo "  Upstream message: $job_message" >&2
            fi
            return 3
            ;;
          pending|queued|in_progress)
            rate_limit_hits=0
            sleep "$poll_interval"
            elapsed=$(( $(date +%s) - poll_started ))
            ;;
          *)
            echo "WARN: unrecognized status '$status' in poll response, continuing to poll..." >&2
            sleep "$poll_interval"
            elapsed=$(( $(date +%s) - poll_started ))
            ;;
        esac
        ;;
      429)
        # The first 429 waits exactly one poll interval, as it always has.
        # Each further 429 in a row doubles that, up to POLL_BACKOFF_MAX,
        # because with several polls sharing the limit the useful response to
        # being rate limited is to ask less often rather than to keep asking.
        # --max-wait is still wall clock, so a long backoff cannot overrun it.
        local backoff=$(( poll_interval * (1 << rate_limit_hits) ))
        [ "$backoff" -gt "$POLL_BACKOFF_MAX" ] && backoff="$POLL_BACKOFF_MAX"
        # Stop counting once the cap is reached: the shift above would keep
        # growing for no effect, and a long enough run of 429s would overflow it.
        [ "$backoff" -lt "$POLL_BACKOFF_MAX" ] && rate_limit_hits=$(( rate_limit_hits + 1 ))
        echo "WARN: rate limited while polling job $job_id. Backing off ${backoff}s (retrying the poll, not create)..." >&2
        sleep "$backoff"
        elapsed=$(( $(date +%s) - poll_started ))
        ;;
      5??)
        echo "WARN: upstream error (HTTP $http_code) while polling. Retrying the poll (not create) in ${poll_interval}s..." >&2
        sleep "$poll_interval"
        elapsed=$(( $(date +%s) - poll_started ))
        ;;
      *)
        print_api_error "poll" "$http_code" "$body"
        return 3
        ;;
    esac
  done

  echo "TIMEOUT: job $job_id has not reached a terminal state after ${max_wait}s." >&2
  echo "The job is very likely still running upstream. Re-run:" >&2
  echo "  $0 poll $job_id" >&2
  echo "Do NOT re-run 'generate' for the same request — that creates a duplicate, separately billed job." >&2
  return 4
}

# ---------------------------------------------------------------------------
# waiting on several jobs at once
#
# Why this exists: one 15-second 720p job took over 600 seconds of wall clock
# on 2026-09-05. Three of them serially is half an hour for work the API does
# in ten minutes. The rate limit is not the constraint — the account allows
# 100 RPM and a polling job spends 10 of them — so the only thing serial
# waiting buys is the wait itself.
#
# What is NOT parallelised here, on purpose: submission. A create is a
# seconds-long call, so submitting one at a time costs almost nothing in wall
# clock, and it is what keeps `batch`'s money guard exact — if take 2's create
# is rejected, takes 3..N are never sent. Firing N creates at once would spend
# N times before learning the first one was going to fail.
# ---------------------------------------------------------------------------

validate_concurrency() {
  # $1 = the value as given. Prints nothing; returns 1 with a message on stderr
  # when it is unusable.
  local v="$1"
  case "$v" in
    ''|*[!0-9]*)
      echo "ERROR: --concurrency must be a positive integer (got '$v')." >&2
      return 1
      ;;
  esac
  if [ "$v" -lt 1 ]; then
    echo "ERROR: --concurrency must be at least 1 (got $v)." >&2
    return 1
  fi
  if [ "$v" -gt "$MAX_CONCURRENCY" ]; then
    echo "ERROR: --concurrency is capped at $MAX_CONCURRENCY here (got $v). At the default 6s poll interval that is already ${ACCOUNT_RPM} requests/minute, which is the whole measured account limit." >&2
    return 1
  fi
  return 0
}

concurrency_rpm_note() {
  # $1 = concurrency, $2 = poll interval. Warns when the combination crowds
  # the account's rate limit. Never blocks: a 429 costs a poll cycle per job,
  # which is time, not money, and the existing per-job backoff handles it.
  local rpm
  rpm="$(awk -v c="$1" -v p="$2" 'BEGIN { if (p + 0 <= 0) p = 1; printf "%d", c * (60 / p) }')"
  [ -n "$rpm" ] || return 0
  if [ "$rpm" -gt "$RPM_SOFT_LIMIT" ]; then
    echo "NOTE: $1 concurrent polls at one request per ${2}s is about ${rpm} requests/minute, against a measured account limit of ${ACCOUNT_RPM}/min. Rate limiting costs a poll cycle per job, not money — but lower --concurrency or raise --poll-interval if you see rate-limit warnings." >&2
  fi
  return 0
}

# Results of the last poll_many run, indexed by the order the records were
# passed in — NOT by the order jobs finished. bash 3.2 has no namerefs, so
# these are globals; reading them by index is what keeps take 3 take 3 even
# when it lands first.
POLL_MANY_RC=()
POLL_MANY_OUT=()
POLL_MANY_ERR=()

poll_many() {
  # $1 = concurrency, $2 = out dir (absolute), $3 = max wait, $4 = poll
  # interval, $5 = --name hint (may be empty), $6 = label word for progress
  # output ("take" | "job"), then one record per job:
  #   "<job id><TAB><polling url>"
  #
  # Each job gets its own background subshell running the ordinary
  # poll_and_download — the same function a single `generate` or `poll` uses,
  # so every retry rule, error mapping, download check and sidecar write is
  # the one already tested. Its stdout and stderr go to files; its exit code
  # is written last, so the presence of the .rc file means the other two are
  # complete.
  #
  # Output discipline: nothing from a child is streamed. Interleaving four
  # polls' warnings live would produce something no one can read and, worse,
  # something no one can attribute. Instead each child's stderr is flushed as
  # one contiguous labelled block the moment that child finishes, and the
  # supervisor prints a heartbeat in between so a ten-minute wait is not
  # silent.
  local concurrency="$1" out_dir="$2" max_wait="$3" poll_interval="$4"
  local name_hint="$5" label="$6"
  shift 6
  local records=("$@")
  local n=${#records[@]}

  POLL_MANY_RC=()
  POLL_MANY_OUT=()
  POLL_MANY_ERR=()
  [ "$n" -eq 0 ] && return 0

  local work
  if ! work="$(mktemp -d)"; then
    # Every job passed in has already been created and is billable, so the
    # honest report is "still running, go and collect them" — not "failed",
    # which would tell the caller to spend again on a new prompt.
    echo "ERROR: could not create a scratch directory to collect the poll results." >&2
    local k=0
    while [ "$k" -lt "$n" ]; do
      POLL_MANY_RC+=(4)
      POLL_MANY_OUT+=("")
      POLL_MANY_ERR+=("No result collected: this script could not create a temporary directory. The job is unaffected and still billable.")
      k=$((k + 1))
    done
    return 6
  fi

  local ids=() urls=() state=() started_at=() pids=()
  local i=0
  while [ "$i" -lt "$n" ]; do
    ids+=("$(printf '%s' "${records[$i]}" | cut -f1)")
    urls+=("$(printf '%s' "${records[$i]}" | cut -f2)")
    state+=(0)          # 0 queued, 1 running, 2 harvested
    started_at+=(0)
    pids+=("")
    POLL_MANY_RC+=("")
    POLL_MANY_OUT+=("")
    POLL_MANY_ERR+=("")
    i=$((i + 1))
  done

  local active=0 next=0 harvested=0
  local now started heartbeat_at deadline
  started="$(date +%s)"
  heartbeat_at="$started"
  # A hard stop for the supervisor itself. Every child is bounded by
  # --max-wait plus its download, so this only fires if a child died without
  # writing its exit code — which would otherwise spin here forever.
  deadline=$(( started + max_wait + 300 ))

  if [ "$n" -gt 1 ]; then
    echo "" >&2
    echo "Waiting on $n jobs, up to $concurrency at a time (poll interval ${poll_interval}s, --max-wait ${max_wait}s each)." >&2
    concurrency_rpm_note "$concurrency" "$poll_interval"
  fi

  while [ "$harvested" -lt "$n" ]; do
    # --- fill the free slots ---
    while [ "$active" -lt "$concurrency" ] && [ "$next" -lt "$n" ]; do
      # Copy the slot's values out before forking. A background subshell sees
      # whatever the parent held at fork time, which is right but reads as if
      # it were racing $next; naming them here removes the question.
      local slot="$next" jid="${ids[$next]}" jurl="${urls[$next]}"
      echo "--- $label $((slot + 1))/$n: polling $jid ---" >&2
      (
        poll_and_download "$jid" "$jurl" "$out_dir" \
          "$max_wait" "$poll_interval" "$name_hint" \
          >"$work/$slot.out" 2>"$work/$slot.err"
        echo "$?" >"$work/$slot.rc"
      ) &
      pids[$slot]=$!
      state[$slot]=1
      started_at[$slot]="$(date +%s)"
      active=$((active + 1))
      next=$((next + 1))
    done

    # --- harvest anything that finished, in index order ---
    local progressed="" rc took
    i=0
    while [ "$i" -lt "$n" ]; do
      if [ "${state[$i]}" = "1" ] && [ -f "$work/$i.rc" ]; then
        rc="$(cat "$work/$i.rc" 2>/dev/null)"
        case "$rc" in ''|*[!0-9]*) rc=3 ;; esac
        took=$(( $(date +%s) - ${started_at[$i]} ))
        POLL_MANY_RC[$i]="$rc"
        POLL_MANY_OUT[$i]="$(cat "$work/$i.out" 2>/dev/null)"
        POLL_MANY_ERR[$i]="$(cat "$work/$i.err" 2>/dev/null)"
        state[$i]=2
        active=$((active - 1))
        harvested=$((harvested + 1))
        progressed=1
        echo "" >&2
        echo "--- $label $((i + 1))/$n finished after ${took}s (exit $rc) — ${ids[$i]} ---" >&2
        [ -n "${POLL_MANY_ERR[$i]}" ] && printf '%s\n' "${POLL_MANY_ERR[$i]}" >&2
      fi
      i=$((i + 1))
    done

    [ "$harvested" -ge "$n" ] && break

    now="$(date +%s)"
    if [ "$now" -ge "$deadline" ]; then
      echo "" >&2
      echo "WARN: giving up on the wait after $(( now - started ))s — longer than --max-wait plus a margin, so a background poll must have died without reporting." >&2
      i=0
      while [ "$i" -lt "$n" ]; do
        if [ "${state[$i]}" != "2" ]; then
          [ -n "${pids[$i]}" ] && kill "${pids[$i]}" 2>/dev/null
          POLL_MANY_RC[$i]=4
          POLL_MANY_OUT[$i]=""
          POLL_MANY_ERR[$i]="TIMEOUT: no result collected for ${ids[$i]}. The job may still be running and billable: $0 poll ${ids[$i]} --out-dir $out_dir"
          state[$i]=2
          harvested=$((harvested + 1))
        fi
        i=$((i + 1))
      done
      break
    fi

    if [ -z "$progressed" ] && [ $(( now - heartbeat_at )) -ge "$POLL_HEARTBEAT" ]; then
      local waiting="" pending=0
      i=0
      while [ "$i" -lt "$n" ]; do
        if [ "${state[$i]}" = "1" ]; then
          waiting="$waiting $label $((i + 1))"
          pending=$((pending + 1))
        fi
        i=$((i + 1))
      done
      local queued=$(( n - next ))
      if [ "$queued" -gt 0 ]; then
        echo "  still running:${waiting} ($queued more queued, $(( now - started ))s elapsed)" >&2
      else
        echo "  still running:${waiting} ($(( now - started ))s elapsed)" >&2
      fi
      heartbeat_at="$now"
    fi

    sleep 1
  done

  wait 2>/dev/null
  rm -rf "$work"
  return 0
}

# Build the readable part of an output filename.
#
# Priority: an explicit --name from the caller, then the job's own prompt.
# The prompt is present in every poll response, so a bare `poll JOB_ID` in a
# fresh shell — with no memory of what was generated — still produces a
# meaningful name instead of degrading to a raw job id. Prints nothing when
# there is no usable source, which is the caller's signal to fall back to the
# job id.
#
# Slicing happens in jq, not bash. jq slices by codepoint and is
# locale-independent, so a CJK prompt can never be cut mid-character the way
# `cut -b` would, and the result doesn't change under LC_ALL=C. jq is already
# a hard dependency of this script, so this costs no new requirement.
#
# Both sources are untrusted text that becomes part of a path: a --name comes
# from a calling skill, and a prompt comes from whoever wrote it. Path
# separators, characters illegal on Windows filesystems, and control
# characters are stripped, then any non-alphanumeric run is trimmed off both
# ends, so '../../etc/passwd' cannot survive as anything traversable, nothing
# turns into a hidden file or a leading-dash pseudo-flag, and a name never
# trails a stray comma or full stop where the slice happened to land. Han
# characters count as alphanumeric here, so CJK text survives while CJK
# punctuation is trimmed.
build_output_slug() {
  local name_hint="$1" prompt="$2" raw=""

  if [ -n "$name_hint" ]; then
    raw="$name_hint"
  else
    raw="$prompt"
  fi
  [ -z "$raw" ] && return 0

  # Order matters twice over. Whitespace is collapsed to a dash *before*
  # control characters are stripped, because tab and newline are both: strip
  # them first and "line one\nline two" glues into "line onelinetwo" instead
  # of separating into words. And the slice comes before the final trim,
  # because the slice itself can land on a separator and leave a trailing
  # dash.
  #
  # Control characters are matched with the POSIX class [[:cntrl:]], never
  # with a backslash-u codepoint range. jq's regex engine (Oniguruma) reads a
  # backslash-u escape inside a *pattern* as the literal letters u, 0, 0, ...,
  # which collapses such a range into the ASCII range 0-u: it silently deletes
  # most letters and digits while leaving the real control characters in
  # place, the exact opposite of the intent. Verified: "A dim convenience
  # store" came back as "  v ".
  jq -rn --arg s "$raw" --argjson max "$SLUG_MAX_CHARS" '
    $s
    | gsub("\\s+"; "-")
    | gsub("[[:cntrl:]]"; "")
    | gsub("[/\\\\:*?\"<>|]"; "")
    | gsub("-+"; "-")
    | . as $full
    | $full[0:$max] as $cut
    | (if ($full | length) > $max
       then (($cut | rindex("-")) // -1) as $ix
            | (if $ix > ($max / 2) then $cut[0:$ix] else $cut end)
       else $cut end)
    | sub("^[^[:alnum:]]+"; "")
    | sub("[^[:alnum:]]+$"; "")
  '
}

# Strip the request payload down to something safe to store.
#
# A resolved --frame-first-image lands in the payload as a base64 data URI
# that can exceed a megabyte on its own. Record that frames were used, never
# the bytes. Idempotent, so running it over an already-compacted payload is
# harmless.
compact_request_json() {
  printf '%s' "$1" | jq -c '
    (if (.frame_images | type) == "array"
     then {frame_images_count: (.frame_images | length)}
     else {} end) as $f
    | del(.frame_images) + $f' 2>/dev/null
}

# Path of the create -> poll handoff file for one job.
#
# `create` and `poll` are deliberately separate processes (that is what keeps
# a short tool timeout from stranding a billable job), which means the create
# payload cannot reach the poll by any in-memory route. The API is no help
# either: its response echoes neither resolution, aspect ratio nor seed. So
# create leaves the payload on disk and poll picks it up.
#
# Dotfile, keyed by job id: out-dir is a directory the user browses, and two
# concurrent creates must not overwrite each other's handoff.
request_handoff_path() {
  printf '%s/.ofox-request-%s.json' "${1%/}" "$2"
}

save_request_handoff() {
  local payload="$1" out_dir="$2" job_id="$3" compact path
  compact=$(compact_request_json "$payload") || return 1
  [ -z "$compact" ] && return 1
  path=$(request_handoff_path "$out_dir" "$job_id")
  printf '%s' "$compact" >"$path" 2>/dev/null || return 1
  return 0
}

# Prints the stored payload, or nothing. Absence is normal, not an error:
# polling a job created on another machine, into a different --out-dir, or by
# a plain `generate` leaves no handoff, and the sidecar simply omits its
# request half — exactly the behaviour before handoffs existed.
load_request_handoff() {
  local path
  path=$(request_handoff_path "$1" "$2")
  [ -r "$path" ] || return 1
  jq -e . "$path" >/dev/null 2>&1 || return 1
  cat "$path"
}

clear_request_handoff() {
  rm -f "$(request_handoff_path "$1" "$2")" 2>/dev/null
  return 0
}

# Write the metadata sidecar that sits next to a downloaded video.
#
# It carries what the filename cannot: the full job id (the short prefix in
# the name can't be expanded back, since the API has no list endpoint), the
# prompt, and the request as submitted — enough to re-render the same shot at
# a different resolution without reconstructing anything by hand.
#
# Note the split: the poll response reports model, prompt, seconds and cost,
# but *not* resolution or aspect ratio — those are echoed nowhere, so they
# only reach the sidecar through the create payload, which means only the
# generate path records them. A bare `poll JOB_ID` writes the response half
# and omits `request` rather than guessing.
#
# Returns nonzero without leaving a partial file if anything goes wrong; the
# caller treats that as a warning, never as a failed download.
write_sidecar() {
  local body="$1" video_path="$2" sidecar_path="$3" name_hint="$4" request_json="$5"
  local req="null" tmp rc

  if [ -n "$request_json" ]; then
    req=$(compact_request_json "$request_json") || req="null"
    [ -z "$req" ] && req="null"
  fi

  tmp=$(mktemp) || return 1
  printf '%s' "$body" | jq \
    --arg video "$(basename "$video_path")" \
    --arg name "$name_hint" \
    --argjson request "$req" '
    {
      job_id: .id,
      status: .status,
      model: .model,
      prompt: .prompt,
      video_seconds: (.usage.video_seconds // null),
      video_cost: (.usage.video_cost // null),
      created_at: .created_at,
      updated_at: .updated_at,
      video_file: $video
    }
    | (if $name != "" then .name = $name else . end)
    | (if $request != null then .request = $request else . end)
  ' >"$tmp" 2>/dev/null
  rc=$?

  # Only publish a sidecar that is actually parseable — a truncated or empty
  # one is worse than none, because it looks like a record and isn't.
  if [ "$rc" -ne 0 ] || ! jq -e . "$tmp" >/dev/null 2>&1; then
    rm -f "$tmp"
    return 1
  fi

  mv "$tmp" "$sidecar_path" 2>/dev/null || { rm -f "$tmp"; return 1; }
  return 0
}

download_result() {
  local job_id="$1" body="$2" out_dir="$3"
  # Optional. name_hint is the caller's --name; request_json is the create
  # payload as actually submitted, which only the generate path has. A bare
  # `poll JOB_ID` passes neither, and everything below degrades cleanly.
  local name_hint="${4:-}" request_json="${5:-}"
  local urls=() url

  # Prefer mirror_urls (CDN-signed, persistent) when present. In practice,
  # not every completed job includes mirror_urls (observed absent on a real
  # bytedance/seedance-2.5 text-to-video completion) — fall back to
  # unsigned_urls in that case rather than treating a completed job as an
  # error. unsigned_urls links are documented as temporary (may expire
  # within 24h), but once we've downloaded the file here, the file is saved
  # locally either way — the expiry window is irrelevant to the caller from
  # this point on, so no separate handling is needed downstream.
  while IFS= read -r url; do
    [ -n "$url" ] && urls+=("$url")
  done < <(printf '%s' "$body" | jq -r '
    if (.mirror_urls | type) == "array" then .mirror_urls[]?
    elif (.mirror_urls | type) == "string" then .mirror_urls
    else empty end')

  if [ ${#urls[@]} -eq 0 ]; then
    while IFS= read -r url; do
      [ -n "$url" ] && urls+=("$url")
    done < <(printf '%s' "$body" | jq -r '
      if (.unsigned_urls | type) == "array" then .unsigned_urls[]?
      elif (.unsigned_urls | type) == "string" then .unsigned_urls
      else empty end')
  fi

  if [ ${#urls[@]} -eq 0 ]; then
    echo "ERROR: job $job_id completed but the response has neither mirror_urls nor unsigned_urls — refusing to guess a download link." >&2
    echo "Raw response body:" >&2
    printf '%s\n' "$body" >&2
    return 3
  fi

  local cost seconds
  cost=$(printf '%s' "$body" | jq -r '.usage.video_cost // "unknown"')
  seconds=$(printf '%s' "$body" | jq -r '.usage.video_seconds // "unknown"')

  # The readable stem of every file this job produces. The job's own prompt
  # comes from the response, so this works identically whether the caller is
  # 'generate' (which knows what it asked for) or a bare 'poll JOB_ID' in a
  # fresh shell (which knows nothing). A short job-id suffix keeps two runs of
  # the same prompt from overwriting each other and keeps the file traceable
  # back to the job.
  local prompt slug base
  prompt=$(printf '%s' "$body" | jq -r '.prompt // empty')
  slug=$(build_output_slug "$name_hint" "$prompt")
  if [ -n "$slug" ]; then
    base="${slug}-${job_id:0:8}"
  else
    base="$job_id"
  fi

  # Note the ${arr[@]+"${arr[@]}"} form used on these arrays below: bash 3.2,
  # which is what /bin/bash still is on macOS, treats an empty array as unset,
  # so a plain "${arr[@]}" under `set -u` aborts the script. That mattered
  # here: if every sidecar write failed, expanding an empty sidecars killed
  # the run right after a paid download, printing VIDEO_PATH but never
  # VIDEO_COST — a successful, billed generation looking like a failure.
  local i=0 count=${#urls[@]} paths=() sidecars=() ext fname outpath sidecar

  for url in "${urls[@]}"; do
    i=$((i + 1))
    ext=$(printf '%s' "$url" | sed -E 's/[?#].*$//; s/^.*\.//')
    case "$ext" in
      mp4|mov|webm|m4v) ;;
      *) ext="mp4" ;;
    esac
    if [ "$count" -gt 1 ]; then
      fname="${base}_${i}.${ext}"
    else
      fname="${base}.${ext}"
    fi
    outpath="${out_dir%/}/${fname}"
    if ! curl -fsSL --connect-timeout "$CONNECT_TIMEOUT" \
         --speed-limit "$DOWNLOAD_MIN_BYTES" --speed-time "$DOWNLOAD_STALL_SECONDS" \
         "$url" -o "$outpath"; then
      echo "ERROR: failed to download from: $url" >&2
      return 3
    fi
    paths+=("$outpath")

    # Sidecar: the short id in the filename is not enough to poll or reconcile
    # this job later (the API has no list endpoint to expand a prefix
    # against), so the full id lives here along with everything needed to
    # re-render the same shot at a different resolution.
    sidecar="${outpath%.*}.json"
    if write_sidecar "$body" "$outpath" "$sidecar" "$name_hint" "$request_json"; then
      sidecars+=("$sidecar")
    else
      # A missing sidecar must never cost the user the video they just paid
      # for; the mp4 is on disk and every field below is still printed.
      echo "WARN: could not write metadata sidecar next to $outpath." >&2
    fi
  done

  echo "STATUS completed"
  echo "JOB_ID $job_id"
  for outpath in "${paths[@]}"; do
    echo "VIDEO_PATH $outpath"
  done
  for sidecar in ${sidecars[@]+"${sidecars[@]}"}; do
    echo "SIDECAR_PATH $sidecar"
  done

  # The handoff has served its purpose only once its contents are on disk in
  # a sidecar. Tying cleanup to this function merely returning would delete
  # it even when write_sidecar failed — that failure is a warning, not an
  # error, so the caller cannot tell the difference — and the record would be
  # gone for good, with no way to rebuild it.
  if [ "${#sidecars[@]}" -gt 0 ]; then
    clear_request_handoff "$out_dir" "$job_id"
  fi
  echo "VIDEO_SECONDS $seconds"
  echo "VIDEO_COST $cost"
  return 0
}

# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------

main() {
  local mode="${1:-}"
  # Recorded so require_approved can echo back the subcommand the caller
  # actually typed ('create' and 'batch' both run cmd_generate). Taken from
  # main's own dispatch word, never by scanning "$@" for it: a prompt is free
  # text, and `--prompt "run it with --approved"` must not read as a flag.
  SUBCOMMAND="$mode"
  # Every subcommand that builds a request from API_BASE validates the base
  # first, and says so when it has been overridden. The four local tools are
  # deliberately not in this list: they run ffmpeg over a file the caller
  # already has, so an environment variable that cannot affect them is no
  # reason to refuse them — and a notice about where the API key goes is
  # false on a command that sends none.
  case "$mode" in
    check|models|providers|generate|create|batch|chain|poll)
      validate_api_base || return 2
      ;;
  esac
  case "$mode" in
    check)
      cmd_check
      return $?
      ;;
    models)
      cmd_models
      return $?
      ;;
    providers)
      shift
      cmd_providers "$@"
      return $?
      ;;
    generate)
      shift
      cmd_generate "$@"
      return $?
      ;;
    create)
      # Same as generate, minus the waiting. See cmd_generate's submit_only.
      shift
      OFOX_SUBMIT_ONLY=1 cmd_generate "$@"
      return $?
      ;;
    batch)
      shift
      cmd_batch "$@"
      return $?
      ;;
    contact-sheet)
      shift
      cmd_contact_sheet "$@"
      return $?
      ;;
    chain)
      shift
      cmd_chain "$@"
      return $?
      ;;
    last-frame)
      shift
      cmd_last_frame "$@"
      return $?
      ;;
    frame-at)
      shift
      cmd_frame_at "$@"
      return $?
      ;;
    mux-audio)
      shift
      cmd_mux_audio "$@"
      return $?
      ;;
    poll)
      shift
      cmd_poll "$@"
      return $?
      ;;
    -h|--help|"")
      usage
      return 1
      ;;
    *)
      echo "ERROR: unknown command '$mode'." >&2
      usage
      return 1
      ;;
  esac
}

main "$@"
exit $?
