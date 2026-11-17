#!/usr/bin/env bash
# ofox-image.sh — Ofox image generation API client: validate, request, decode, save.
#
# Part of the ofox-image-core skill. Dependencies: bash, curl, jq. Nothing else.
#
# OFOX_API_KEY is read from the shell environment. This script never parses a
# dotenv file and never hardcodes the key; if the key lives in a file, the
# caller sources it into this script's environment first. The raw key is never
# printed by this script.
#
# The key only ever goes to one host: whatever API_BASE names. Every request
# here is built from API_BASE and no URL out of a response body is ever
# fetched, so the only way to move it is OFOX_API_BASE_URL — still supported
# (staging), but since 1.14.0 it must be https (loopback excepted) and the
# override is announced on stderr, naming the host that will receive the key.
# Covered by references/test/keyguard.test.sh.
#
# Unlike the Ofox video API, image generation is SYNCHRONOUS — there is no
# job id and no polling. One request either returns the image(s) in the
# response body, or fails. That also means there is no free "poll to check
# what happened" recovery path: every real call that reaches the API is a
# real spend attempt, and if the network drops before any HTTP response
# comes back, there is no job id to look up later to find out what happened
# (see exit 5 below).
#
# Usage:
#   ofox-image.sh check
#   ofox-image.sh models [--endpoint generations|edits]
#   ofox-image.sh generate --prompt "..." --quality VAL [--model NAME] [OPTIONS]
#   ofox-image.sh edit --image FILE --prompt "..." [--model NAME] [OPTIONS]
#
# generate OPTIONS:
#   --model NAME              optional, default "auto": the first available
#                               model in the cheapest-first priority chain
#                               (MODEL_CHAIN below), resolved against the live
#                               model list BEFORE the estimate is printed, so
#                               the model named in a quote is the model that
#                               would actually run. Pass an explicit id to pin
#                               one instead; run 'models' to list them.
#                               This used to be required with no default, on
#                               the grounds that the image models differ ~4x in
#                               price and defaulting would silently pick a
#                               price on the caller's behalf. --dry-run plus
#                               the approval gate answer that objection: the
#                               resolved model and its price now go in front of
#                               the user before every spend, default or not.
#                               Documented in depth here: openai/gpt-image-2,
#                               google/gemini-3.1-flash-image,
#                               qwen/qwen-image-3.0-pro. Every other image
#                               model Ofox serves also works; only their
#                               size/quality support is undocumented here.
#   --dry-run                 validate everything, resolve the model, build the
#                               payload and print a ROUGH cost estimate — then
#                               stop. No request is sent, nothing is billed,
#                               and no API key is needed. The estimate is
#                               rough by nature: an image is billed per output
#                               token, and the token count is only known once
#                               the response comes back. See references/
#                               token-anchors.json for what it is based on and
#                               when it refuses to guess at all.
#   --prompt TEXT        required.
#   --quality VAL        required (documented as required by the API).
#                          One of: auto low medium high standard hd — that is
#                          the union across models, and the only thing checked
#                          here. No model is known to accept all six, so a
#                          value the chosen model does not take comes back as
#                          an API rejection (exit 3), not a local error:
#                          measured 2026-09-04, openai/gpt-image-2 refuses
#                          `standard` (400, "Supported values are: 'low',
#                          'medium', 'high', and 'auto'"), which
#                          microsoft/mai-image-2.5-flash accepts. Nothing is
#                          billed for the refusal. Per-model table:
#                          references/api-params.md. No default is guessed
#                          here, pass exactly the value you intend.
#   --size VAL           optional. One of:
#                          auto 1024x1024 1536x1024 1024x1536 256x256
#                          512x512 1792x1024 1024x1792
#                        NOTE what that enum does NOT contain: 16:9 and 9:16.
#                          1792x1024 is 1.75 and 1024x1792 is 0.5714; the
#                          real ratios are 1.7778 and 0.5625. Neither can be
#                          requested, on any model, so every 16:9 or 9:16
#                          frame has to be cropped — see --target-aspect.
#   --target-aspect W:H  optional. The ratio the delivered file must actually
#                          be, e.g. 16:9. This script then picks the request
#                          size that survives the crop with the most pixels
#                          intact, measures the file it got back (never the
#                          size the response claims), and centre-crops to
#                          exactly W:H. Needs ffmpeg/ffprobe, checked before
#                          anything is spent.
#   --target-size WxH    optional. Exact output pixels, e.g. 1280x720. Same
#                          as --target-aspect for the ratio, plus a floor:
#                          the cheapest accepted size that clears it is
#                          requested, and the crop is scaled down to exactly
#                          WxH. Never scaled up — if the file comes back too
#                          small the run fails loudly instead of delivering
#                          an upscaled frame. Mutually exclusive with
#                          --target-aspect (this already fixes the ratio).
#                        With either flag the cropped frame takes the plain
#                          output name (so IMAGE_PATH is the file to attach)
#                          and the API's untouched bytes are kept alongside
#                          it as <name>-uncropped.<ext>, reported as
#                          IMAGE_PATH_UNCROPPED.
#   --n N                optional, integer 1-10 (server default 1).
#                          NOT supported by google/gemini-3.1-flash-image —
#                          passing --n at all with that model is a client-
#                          side validation error (rejected before any
#                          network call), matching the documented gotcha
#                          that Gemini rejects the n field outright.
#   --output-format VAL  optional. One of: png jpeg webp
#   --background VAL     optional. One of: transparent opaque auto
#   --extra-json JSON    optional. A JSON OBJECT merged into the request body:
#                          the escape hatch for fields with no flag of their
#                          own, e.g. extra_body.provider.type (gpt-image-2
#                          only). Rejected if it is empty (an explicit ""
#                          used to be indistinguishable from omitting the
#                          flag, which skipped every check below AND the
#                          merge, and billed the request anyway), if it is not
#                          an object (it is merged with jq's `*`, which only
#                          works between objects), if it sets a field that has
#                          a flag — model, prompt, quality, size, n,
#                          output_format, background, which are validated and
#                          priced from the flags while this merge happens
#                          after the estimate — or if it sets "input_images"
#                          (image-to-image is out of scope for this script —
#                          see below) or "stream": true (this script only
#                          parses a plain JSON response body, not a streamed
#                          one).
#   --out-dir DIR        optional, default: current directory.
#   --out-name NAME      optional base filename (no extension, no path
#                          separators). Default: ofox_image_<timestamp>_<pid>.
#
# edit OPTIONS (POST /v1/images/edits — take an image you already have and
# change it, rather than drawing a new one from the prompt alone):
#   --image PATH         the image to edit, as a local file. This is the
#                          primary input: it is measured working and needs no
#                          hosting anywhere. png/jpeg/webp only — the API
#                          enumerates exactly those three.
#   --image-url URL      alternative to --image: a public URL, or a
#                          data:image/...;base64,... URI. Confirmed accepted
#                          at validation 2026-09-15 (a data: URI got past file
#                          handling to model validation). The value is written
#                          to a temp file and read back with curl's
#                          -F "field=<file", never passed as a command-line
#                          argument — a base64 data URI of any real photo
#                          exceeds ARG_MAX and would die before the network.
#                        Exactly one of --image / --image-url is required.
#   --prompt TEXT        required BY THIS SCRIPT. Whether the API requires it
#                          is untested and deliberately so: the only way to
#                          find out is to send an edit without one, and on
#                          this endpoint a request that is not rejected is a
#                          request that renders and bills. An edit with no
#                          instruction has no meaning anyway.
#   --quality VAL        optional. Same union as generate. NOTE THE ASYMMETRY,
#                          it is the expensive one: /v1/images/generations
#                          rejects a bad --quality with a free HTTP 400, and
#                          /v1/images/edits DOES NOT — measured 2026-09-15,
#                          quality=ultra_not_a_value was silently ignored and
#                          six edits rendered and billed. So the client-side
#                          check below is not a convenience that saves a round
#                          trip, as it is on generate; here it is the only
#                          thing standing between a typo and a bill.
#   --size VAL           optional, same enum as generate, validated for typos
#                          only. Whether this endpoint honours it is UNTESTED
#                          (see --quality: finding out costs a real edit). All
#                          four measured runs passed no --size and got back a
#                          size in no enum, matching the INPUT's aspect ratio
#                          at a near-constant ~1.57 MP: 1672x941 from a
#                          854x480, a 320x180 and a 1792x1008 input, 1254x1254
#                          from a 256x256 one. 1672x941 is 1.777, i.e. the 16:9
#                          that generate's size enum cannot express at all. The
#                          1792x1008 run is the one showing this is a BUDGET
#                          and not an upsample floor: its input is larger than
#                          the output and the output did not grow.
#   --n N                optional, integer 1-10. Multiplies the spend; and
#                          because this endpoint validates so little, a value
#                          it does not like is more likely to render than to
#                          be refused.
#   --output-format VAL  optional. One of: png jpeg webp
#   --background VAL     optional. One of: transparent opaque auto
#   --target-aspect W:H  optional, same contract as generate: measure the
#   --target-size WxH      written file and centre-crop to the target, or fail
#                          loudly. Same reason as generate — an attached
#                          frame's ratio becomes the finished video's ratio.
#   --extra-form K=V     optional, repeatable. Escape hatch for a multipart
#                          field with no flag — and only for those. A KEY this
#                          script already sets from a flag (image, image_url,
#                          model, prompt, quality, size, n, output_format,
#                          background) is refused, because a second part with
#                          the same name skips that flag's validation and is
#                          added AFTER the estimate is computed: `--extra-form
#                          "n=10"` used to quote one image and request ten.
#                          Use the flag. This endpoint is multipart, so
#                          there is no --extra-json equivalent: a JSON body is
#                          rejected outright (measured — an application/json
#                          body with model set came back "You must provide a
#                          model parameter", i.e. the field was never seen).
#                          The VALUE may not start with '@' or '<': curl reads
#                          those as filesystem instructions ('@path' uploads
#                          that file, '<path' sends its contents as the field
#                          value), which made this flag a way to upload any
#                          file the user can read. Refused since 1.14.0; every
#                          ordinary key=value pair is unaffected, and the
#                          script's own -F "image=@PATH" comes from --image,
#                          not from here. Every OTHER field this script sets
#                          goes through curl's --form-string, which has no
#                          such prefixes — so a --prompt that opens with '@'
#                          is a prompt, not a file read.
#   --dry-run            validate everything, resolve the model, assemble and
#                          print the multipart field list, quote a cost — then
#                          stop. No request, no key needed, nothing billed.
#   --out-dir DIR        optional, default: current directory.
#   --out-name NAME      optional base filename (no extension, no separators).
#
# Out of scope for this script (see skills/ofox-image-core/SKILL.md):
#   - input_images / image-to-image on the GENERATIONS endpoint (a Qwen-only
#     field). Editing an existing image is what 'edit' above is for; this
#     refers to the separate, silently-ignored-if-misspelled field on
#     /v1/images/generations, which stays unexposed.
#   - Masked / inpainting edits. The endpoint may or may not accept a 'mask'
#     field; nothing here establishes that it does, and finding out costs a
#     billed edit per attempt.
#     WHAT 1.14.0 NARROWED, stated rather than left to be discovered: until
#     then the suggestion here was to attach one with
#     --extra-form "mask=@FILE". That spelling is now refused along with
#     every other '@'/'<' value, because the same spelling uploads any file
#     the user can read. A mask therefore cannot be attached through this
#     script today. Establishing masked edits needs its own flag, with its
#     own path validation, not a general file-upload hole left open for the
#     one field that might want it.
#
# Exit codes:
#   0  success — image(s) decoded and saved, usage token counts printed.
#   1  usage / parameter validation error (no network call made).
#   2  environment error (missing curl/jq/OFOX_API_KEY).
#   3  API rejected the request, or the response could not be parsed into a
#      usable image.
#   4  --out-dir could not be created or entered (bad path, permissions) —
#      a local filesystem problem, caught BEFORE any network call is made
#      (out-dir is resolved up front for exactly this reason: no reason to
#      spend money on a request whose output can't be written anywhere).
#   5  ambiguous network failure on the generate/edit call — no HTTP response
#      was received at all (curl exit nonzero, no HTTP status). Unlike the
#      video API, there is no job id and no poll endpoint to check afterwards —
#      the only way to find out whether this was billed is to check your
#      usage/billing history at https://app.ofox.ai. Do not blindly retry.
#
# Whether a REJECTED request (a real HTTP error response, e.g. 4xx) is
# billed is NOT confirmed for this endpoint as of writing — this script
# assumes (but has not verified with a real call) that it follows the same
# pattern as most billed generation APIs: a request that never produced an
# image is not charged. Treat that as an open question until a real error
# case has been observed and documented, not as a settled fact.

set -u

DEFAULT_API_BASE="https://api.ofox.ai/v1"
# Overridable on purpose (pointing a run at a staging deployment is a real
# need), but never silently: validate_api_base() below refuses a plaintext
# non-loopback host and announces the override on stderr, because this
# variable decides which host receives OFOX_API_KEY.
API_BASE="${OFOX_API_BASE_URL:-$DEFAULT_API_BASE}"
GET_KEY_URL="https://app.ofox.ai"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODELS_SNAPSHOT="$SCRIPT_DIR/models-snapshot.json"
TOKEN_ANCHORS="$SCRIPT_DIR/token-anchors.json"
MODELS_CACHE_TTL="${OFOX_MODELS_TTL:-86400}" # 24h

# Network timeouts for the one call that costs money. Only the model-list
# fetch had any, leaving generate able to hang forever on a stalled
# connection. Generous, because image generation is synchronous — the whole
# render happens inside this one request, so a short limit would kill valid
# slow jobs. Timing out lands in the ambiguous exit-5 path ("no response, no
# job id, check billing history"), which is already handled; hanging
# indefinitely is not the safer alternative.
CONNECT_TIMEOUT=15
GENERATE_MAX_TIME=300

# The models this skill's docs and pricing notes cover in depth. It is NOT a
# whitelist — --model is checked against the live model list (see load_models),
# so any image model Ofox offers works. This is only what gets named in help
# text when we have no list to name real models from.
# qwen/qwen-image-3.0-pro was qwen/qwen-image-3.0-pro until 2026-09-15; Ofox
# kept the old id as an alias, so both resolve, but this line is help text and
# should name the id the catalog does.
DOCUMENTED_MODELS="openai/gpt-image-2 google/gemini-3.1-flash-image qwen/qwen-image-3.0-pro"

# THE image model priority chain — the single definition in this repo. Every
# consumer (this skill's docs, and every scenario skill built on it) resolves
# a model by calling this script, never by keeping its own copy of the list:
# a second copy is a second thing to forget to update when prices move.
#
# Ranked by measured cost PER IMAGE, not by the catalog's per-output-token
# rate — the two rankings disagree here. At the one --quality/--size pair
# measured on both models (low / 1024x1024, 2026-09-02), openai/gpt-image-2
# costs more per output token than microsoft/mai-image-2.5-flash but spends
# only 196 output tokens on an image against mai-flash's 1024, which more than
# cancels the higher per-token rate out: ~0.6 cents/image against ~2.0
# cents/image, gpt-image-2 cheaper by about 3.4x. Do not re-derive this order
# from the rate card alone — the comparable figure is rate x that model's own
# measured token count, and google/gemini-3.1-flash-lite-image and
# microsoft/mai-image-2.5 below have no per-image measurement yet, only the
# per-token rate.
#
# The cents are rates x measured tokens, and the rates are Ofox's to change.
# They did on 2026-09-15: mai-flash's output_image went 0.000026 -> 0.0000195,
# moving its row from ~2.67 to ~2.0 cents and the gap from 4.5x to 3.4x with
# no token count moving and no code changing. The script itself always prices
# from the live list, so this comment block is the only thing that can go
# stale — re-check it whenever references/refresh-snapshot.sh is run.
#
#   openai/gpt-image-2                   ~0.6 cents/image     preferred
#   microsoft/mai-image-2.5-flash        ~2.0 cents/image     second
#   google/gemini-3.1-flash-lite-image   0.000030 USD/token   no per-image figure yet
#   microsoft/mai-image-2.5              0.000047 USD/token   same vendor, better quality
#
# EVERY cents/image figure above is only true for the pair it was measured at
# (low / 1024x1024 for both), and the spread within one model is larger than
# the gap between the two. Measured 2026-09-04: gpt-image-2 at high /
# 1792x1024 spends 5063 output tokens, ~15.4 cents/image — about 26x its own
# row above. No like-for-like comparison exists at any pair other than
# low / 1024x1024, so "cheapest model" is a narrower claim than this list
# looks. anchor_measurements() below reads every measured point a model has,
# and print_estimate() quotes the one matching the request's own pair (or the
# dearest, labelled an upper bound, when no point matches) — so the estimate
# is pair-aware even though this comment's per-image column is not. Read
# references/token-anchors.json's _what_the_count_does_depend_on before
# quoting a cents/image figure from the rows above by hand.
#
# History, kept so a reorder never reads as someone quietly sneaking a
# preference through: on 2026-09-02, with both cents-per-image figures above
# already measured, the repo owner looked at them and deliberately kept
# microsoft/mai-image-2.5-flash first (see references/token-anchors.json's
# chain-order history note for that reasoning, and its instruction that the
# next person who wanted to reorder the chain should raise it first rather
# than doing it quietly). On 2026-09-04 the repo owner did exactly that and
# asked for openai/gpt-image-2 first instead — this is that request, not an
# unreviewed reordering. See references/pricing.md for the full record.
#
# It is a PRIORITY, not a lock: --model <id> still pins any image model Ofox
# serves, including ones far more expensive than anything here. The chain only
# decides what happens when nobody picked.
#
# google/gemini-2.5-flash-image also sits at 0.000030 USD/token and is
# deliberately not in the chain — three entries at the same per-token price
# buys nothing over two. The openai/gpt-5* family's 0.000032 USD is a text
# model's incidental image output, not an image model, and is not a
# candidate at all.
MODEL_CHAIN="openai/gpt-image-2 microsoft/mai-image-2.5-flash google/gemini-3.1-flash-lite-image microsoft/mai-image-2.5"

# Set by resolve_model(): the id that will actually be used, plus — when the
# preferred model was skipped — what was skipped, why, and how the price
# compares. All four are reported to the caller, because "we fell back" is
# exactly the fact an approval table must not omit.
RESOLVED_MODEL=""
MODEL_FALLBACK_FROM=""
MODEL_FALLBACK_REASON=""
MODEL_PRICE_DELTA=""
MODEL_CHAIN_EXHAUSTED=""

# Set by load_models(): the file holding the model list, and where it came
# from ("live" | "cache" | "stale-cache" | "snapshot").
MODELS_FILE=""
MODELS_SOURCE=""
VALID_SIZES="auto 1024x1024 1536x1024 1024x1536 256x256 512x512 1792x1024 1024x1792"
VALID_QUALITIES="auto low medium high standard hd"
VALID_OUTPUT_FORMATS="png jpeg webp"
VALID_BACKGROUNDS="transparent opaque auto"
NO_N_MODEL="google/gemini-3.1-flash-image"

# The two endpoints this script speaks to, spelled exactly as /v1/models lists
# them in each entry's supported_endpoints array. They are values, not
# literals scattered through the code, because every capability question here
# ("can this model do that?") is answered by looking one of them up in the
# live catalog rather than by consulting a table in this file.
GENERATIONS_ENDPOINT="/v1/images/generations"
EDITS_ENDPOINT="/v1/images/edits"

# The file formats POST /v1/images/edits accepts as input, quoted from its own
# rejection message (2026-09-15, a text/plain upload): "Supported file formats
# are 'image/jpeg', 'image/png', and 'image/webp'." That is the API
# enumerating its own set, which is the only basis on which a list like this
# earns a place in this script — the same standard model_qualities() is held
# to. It is checked locally because the alternative is uploading a file that
# was never going to work.
EDIT_INPUT_FORMATS="png jpg jpeg webp"

# --quality is a PER-MODEL enum, and VALID_QUALITIES above is the union of
# every value any model takes. Validating only against the union is what let
# --quality standard sail through both validation and --dry-run and then die
# at submission with HTTP 400 the moment MODEL_CHAIN's head became
# openai/gpt-image-2 on 2026-09-04 — five copy-pasteable commands in two
# other skills shipped broken that way, and a dry run caught none of them.
#
# What is in the table below is FIRST-HAND ONLY, and there is exactly one
# row, because there is exactly one model whose accepted set has been
# enumerated by the API itself:
#
#   openai/gpt-image-2   auto low medium high
#     From the refusal's own message, verbatim, 2026-09-04, nothing billed:
#     Invalid value: 'standard'. Supported values are: 'low', 'medium',
#     'high', and 'auto'. So 'standard' and 'hd' are excluded by the API's
#     own enumeration, not by inference.
#
# Everything else falls through to the union on purpose. What exists for the
# other models is evidence that a value WORKS, not an enumeration of what a
# model takes: microsoft/mai-image-2.5-flash accepted 'standard' on nine real
# runs, google/gemini-3.1-flash-image accepted 'low' — neither tells us what
# else those models would have accepted. Narrowing a model on that basis
# would invent a whitelist, and a false rejection here is worse than the 400
# it would be trying to prevent: the 400 costs a round trip and nothing in
# money, while a false rejection blocks work outright with no way around it
# short of editing this script. So: an absence of evidence stays permissive,
# and a row only gets added when a model has enumerated its own set.
model_qualities() {
  # $1 = model id. Prints the values that model is KNOWN to accept, or
  # nothing when its accepted set has never been enumerated — in which case
  # the caller must fall back to VALID_QUALITIES rather than guess.
  case "$1" in
    openai/gpt-image-2) echo "auto low medium high" ;;
    *) ;;
  esac
}

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
# This script makes exactly three network calls — the public keyless model
# list, POST /images/generations and POST /images/edits — and every one of
# them is built from API_BASE. No URL from a response body is ever fetched,
# so the sibling ofox-video.sh's polling_url problem has no counterpart here.
# What both scripts do share is OFOX_API_BASE_URL: it points the client, and
# the Authorization header with it, at whatever host it names. That stays (a
# staging deployment is the obvious legitimate use) but is narrowed to https
# — loopback excepted, for a local test server — and is announced on stderr
# naming the host that is about to receive the key.
#
# Duplicated in ofox-video-core/references/ofox-video.sh on purpose: each
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
  # Keep only what follows the last '@': the userinfo of
  # "https://api.ofox.ai@evil.example/v1" is not the host, and the host is
  # what receives the request.
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

decode_b64_to_file() {
  # $1 = base64 string, $2 = destination path.
  # Portable base64 decode: GNU coreutils uses -d; older BSD/macOS base64
  # only understands -D. Try -d first (works on GNU and modern macOS),
  # fall back to -D (older macOS) if that fails.
  local b64="$1" outfile="$2"
  if printf '%s' "$b64" | base64 -d >"$outfile" 2>/dev/null && [ -s "$outfile" ]; then
    return 0
  fi
  if printf '%s' "$b64" | base64 -D >"$outfile" 2>/dev/null && [ -s "$outfile" ]; then
    return 0
  fi
  return 1
}

# ---------------------------------------------------------------------------
# target ratio / target size: request the size that crops best, then crop
#
# The size enum this API accepts CANNOT express 16:9 or 9:16. Not "does not
# reliably produce" — cannot be asked for at all:
#
#   1024x1024 512x512 256x256   1.0000   1:1 exact
#   1536x1024                   1.5000   3:2 exact
#   1024x1536                   0.6667   2:3 exact
#   1792x1024                   1.7500   nearest 16:9, which is 1.7778
#   1024x1792                   0.5714   nearest 9:16, which is 0.5625
#
# So every 16:9 or 9:16 frame this API produces has to be cropped. There is
# no flag, no model and no prompt wording that avoids it. That matters well
# beyond tidiness because of where these frames go: attaching one to a
# bytedance/seedance-2.5 job forces aspect_ratio: adaptive, so the frame's
# own ratio becomes the finished video's ratio. A 1.75 frame yields a 1.75
# video, and correcting it means paying for the video again.
#
# Two facts make the crop impossible to do by eye. The response's own size
# field is not evidence of what was written (microsoft/mai-image-2.5-flash:
# requested 1792x1024, response said 1354x774, file measured 1344x768 —
# three different numbers, three real runs), and openai/gpt-image-2
# honouring --size exactly (one run, 2026-09-04) still did not remove the
# crop, because 1792x1024 is not 16:9 either. So the measurement has to come
# from the written file, every time, on every model.
#
# That is what --target-aspect / --target-size are for: state the ratio (or
# the exact pixels) the frame actually has to be, and this script picks the
# request size, measures the file it got, and crops to the ratio exactly.
# Three agents in a row re-derived "measure the file, then crop" by hand
# before this existed.
#
# Crop dimensions are exact multiples of the reduced ratio, never a rounded
# division — that is what makes the result the ratio asked for rather than
# something 0.03% off it. Both hand-crops on record fall out of the same
# rule: 1344x768 -> 1344x756 for 16:9 (k=84), 1792x1024 -> 1792x1008 (k=112).
# ---------------------------------------------------------------------------

gcd_of() {
  # $1, $2 = positive integers. Echoes their greatest common divisor.
  local a="$1" b="$2" t
  while [ "$b" -ne 0 ]; do
    t=$((a % b))
    a="$b"
    b="$t"
  done
  echo "$a"
}

parse_ratio_pair() {
  # $1 = "W:H" or "WxH", $2 = the separator to require (":" or "x").
  # Echoes "W H" with both terms validated as positive integers. The ratio is
  # NOT reduced here — reduction is a separate step, because --target-size
  # needs the raw pixels as well as the ratio they imply.
  local spec="$1" sep="$2" w h
  case "$sep" in
    ':') w="${spec%%:*}"; h="${spec##*:}" ;;
    *)   w="${spec%%x*}"; h="${spec##*x}" ;;
  esac
  # Reject anything that isn't exactly two positive integer terms. "16:9:1"
  # and "16:" both fall out here, as does any non-digit.
  case "$spec" in
    *"$sep"*) : ;;
    *) return 1 ;;
  esac
  case "$w$sep$h" in
    "$spec") : ;;
    *) return 1 ;;
  esac
  case "$w" in ''|*[!0-9]*) return 1 ;; esac
  case "$h" in ''|*[!0-9]*) return 1 ;; esac
  [ "$w" -gt 0 ] && [ "$h" -gt 0 ] || return 1
  echo "$w $h"
}

reduce_ratio() {
  # $1 = W, $2 = H. Echoes "W H" divided by their gcd, so 1792 1008 -> 16 9.
  local w="$1" h="$2" g
  g="$(gcd_of "$w" "$h")"
  [ "$g" -gt 0 ] || return 1
  echo "$((w / g)) $((h / g))"
}

crop_dims_for() {
  # $1 = measured width, $2 = measured height, $3/$4 = REDUCED target ratio.
  # Echoes "cropW cropH": the largest centre-crop of the measured image whose
  # dimensions are exact integer multiples of the reduced ratio. Fails (1)
  # when the image is too small to hold even one multiple of it.
  local mw="$1" mh="$2" tw="$3" th="$4" kw kh k
  kw=$((mw / tw))
  kh=$((mh / th))
  k="$kw"
  [ "$kh" -lt "$k" ] && k="$kh"
  [ "$k" -ge 1 ] || return 1
  echo "$((tw * k)) $((th * k))"
}

select_size_for_target() {
  # $1/$2 = reduced target ratio. $3/$4 = a pixel floor, or "" for none.
  # Echoes the --size value to request.
  #
  # Two different rankings, because the two flags want different things:
  #
  #   with a pixel floor (--target-size): the crop is scaled to exactly those
  #   pixels afterwards, so anything above the floor is tokens paid for and
  #   thrown away. Cheapest candidate that clears the floor wins.
  #
  #   without one (--target-aspect): nothing is thrown away, so the best
  #   candidate is the one that survives the crop with the most pixels
  #   intact. 16:9 picks 1792x1024 (98.4% retained) over 1536x1024 (84.4%)
  #   and over 1024x1024 (56.3%); 1:1 picks 1024x1024, since 512x512 retains
  #   fewer pixels and 1536x1024 costs more for the same crop.
  local tw="$1" th="$2" fw="${3:-}" fh="${4:-}"
  local cand cw ch dims ccw cch req_area ret_area take
  local best="" best_req=0 best_ret=0
  for cand in $VALID_SIZES; do
    [ "$cand" = "auto" ] && continue
    cw="${cand%x*}"
    ch="${cand#*x}"
    dims="$(crop_dims_for "$cw" "$ch" "$tw" "$th")" || continue
    ccw="${dims% *}"
    cch="${dims#* }"
    if [ -n "$fw" ]; then
      { [ "$ccw" -ge "$fw" ] && [ "$cch" -ge "$fh" ]; } || continue
    fi
    req_area=$((cw * ch))
    ret_area=$((ccw * cch))
    take=""
    if [ -z "$best" ]; then
      take=1
    elif [ -n "$fw" ]; then
      if [ "$req_area" -lt "$best_req" ] ||
        { [ "$req_area" -eq "$best_req" ] && [ "$ret_area" -gt "$best_ret" ]; }; then
        take=1
      fi
    else
      if [ "$ret_area" -gt "$best_ret" ] ||
        { [ "$ret_area" -eq "$best_ret" ] && [ "$req_area" -lt "$best_req" ]; }; then
        take=1
      fi
    fi
    if [ -n "$take" ]; then
      best="$cand"
      best_req="$req_area"
      best_ret="$ret_area"
    fi
  done
  [ -n "$best" ] || return 1
  echo "$best"
}

measure_image_file() {
  # $1 = path to an image on disk. Echoes "WxH" read from the FILE, never
  # from anything the API said about it. ffprobe because that is what this
  # repo already depends on for media measurement (ofox-video-core uses
  # ffmpeg/ffprobe for its contact sheets and chain frames) — no new
  # dependency is introduced to answer "how big is this PNG".
  local f="$1" dims
  command -v ffprobe >/dev/null 2>&1 || return 1
  dims="$(ffprobe -v error -select_streams v:0 \
    -show_entries stream=width,height -of csv=p=0:s=x "$f" 2>/dev/null)" || return 1
  dims="${dims%%$'\n'*}"
  dims="${dims%x}"
  case "$dims" in
    *x*) : ;;
    *) return 1 ;;
  esac
  case "${dims%x*}" in ''|*[!0-9]*) return 1 ;; esac
  case "${dims#*x}" in ''|*[!0-9]*) return 1 ;; esac
  echo "$dims"
}

crop_image_to() {
  # $1 = source, $2 = destination, $3/$4 = crop WxH, $5/$6 = optional exact
  # output WxH to scale the crop down to. Centre crop: ffmpeg's crop filter
  # defaults x/y to (iw-ow)/2, (ih-oh)/2.
  local src="$1" dst="$2" cw="$3" ch="$4" ow="${5:-}" oh="${6:-}" vf
  vf="crop=${cw}:${ch}"
  if [ -n "$ow" ] && { [ "$ow" -ne "$cw" ] || [ "$oh" -ne "$ch" ]; }; then
    vf="${vf},scale=${ow}:${oh}"
  fi
  ffmpeg -nostdin -loglevel error -i "$src" -vf "$vf" -frames:v 1 -y "$dst" \
    >/dev/null 2>&1 || return 1
  [ -s "$dst" ] || return 1
  return 0
}

# ---------------------------------------------------------------------------
# model list
#
# GET /v1/models is public, keyless and free, and reports which models serve
# /v1/images/generations. Checking --model against it means this skill works
# with every image model Ofox offers instead of a hand-maintained list of
# three that silently rejected the other eleven.
#
# Unlike the video API, the models endpoint exposes no per-model size/quality
# capability data for image models (there is no image_attributes to match
# video_attributes), so --size/--quality/--output-format/--background stay
# hardcoded from the docs. Only the model id itself is validated dynamically.
#
# This mirrors the same logic in ofox-video-core's ofox-video.sh rather than
# sharing it: each skill must work when installed on its own, so a shared file
# across skill directories is not an option (CONTRIBUTING rule 7).
#
# Order of preference: fresh cache -> live fetch -> stale cache -> bundled
# snapshot -> no check at all. A missing model list never blocks a request
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
    echo "NOTE: could not reach $API_BASE/models; checking --model against the bundled snapshot ($snap_date). A model added since then may be rejected here — set OFOX_SKIP_MODEL_VALIDATION=1 to skip the check." >&2
    return 0
  fi

  MODELS_SOURCE="none"
  echo "NOTE: no model list available (fetch failed, no cache, no bundled snapshot). Skipping the --model check; the API will have the final say." >&2
  return 1
}

model_entry() {
  # $1 = model id (or one of its aliases). Prints that model's whole entry as
  # compact JSON, or nothing if the list doesn't have it.
  [ -n "$MODELS_FILE" ] || return 1
  jq -c --arg m "$1" \
    'first(.data[] | select(.id == $m or ((.aliases // []) | index($m)) != null)) // empty' \
    "$MODELS_FILE" 2>/dev/null
}

output_image_rate() {
  # $1 = model id. Prints its per-output-token image rate, or nothing.
  local entry
  entry="$(model_entry "$1")" || return 1
  [ -n "$entry" ] || return 1
  printf '%s' "$entry" | jq -er '.pricing.output_image // empty' 2>/dev/null
}

model_unavailable_reason() {
  # $1 = model id, $2 = the endpoint it has to serve (default: generations).
  # Prints why this model cannot be used, or nothing when it can. Only checks
  # that cost nothing: the model list is public and keyless.
  #
  # The endpoint is a PARAMETER, not a second hardcoded list, and that is the
  # whole answer to "which models accept an edit". Ofox already publishes it:
  # every entry's supported_endpoints array names /v1/images/edits or does
  # not. Confirmed predictive in both directions on 2026-09-15 — a model whose
  # array omits it (qwen/qwen-image-3.0-pro) is refused with
  # `endpoint_not_supported`, and seven whose array carries it all ran an edit.
  # So no static edit-support table exists here, deliberately: this repo has
  # five documented defects from keeping its own copy of an external API's
  # value table, and the newest was created by refreshing the data next to it.
  local entry endpoint="${2:-$GENERATIONS_ENDPOINT}"
  entry="$(model_entry "$1")"
  if [ -z "$entry" ]; then
    echo "not in the Ofox model list"
    return 0
  fi
  if ! printf '%s' "$entry" | jq -e --arg e "$endpoint" '(.supported_endpoints // []) | index($e)' >/dev/null 2>&1; then
    echo "does not serve $endpoint"
    return 0
  fi
  if printf '%s' "$entry" | jq -e '.is_deprecated == true' >/dev/null 2>&1; then
    echo "marked deprecated by Ofox"
    return 0
  fi
  return 0
}

resolve_model() {
  # Walks MODEL_CHAIN and sets RESOLVED_MODEL to the first usable entry,
  # recording the fallback in MODEL_FALLBACK_* when that is not the preferred
  # one. Always succeeds: an unresolvable chain still yields the preferred
  # model, because refusing to name one would leave the caller with nothing to
  # put in front of the user.
  #
  # This runs BEFORE any estimate is printed and before any request is built,
  # on purpose. A quote that says "the preferred model" and a run that uses
  # something else is a user approving a price they were never shown.
  # $1 = the endpoint the resolved model has to serve (default: generations).
  # The chain itself is not duplicated per endpoint: all four entries happen
  # to serve both today, and if one ever stops, this walk skips it for exactly
  # the reason the catalog gives. A second chain would be a second thing to
  # forget to update.
  local endpoint="${1:-$GENERATIONS_ENDPOINT}"
  local preferred reason candidate rate_pref rate_used
  preferred="${MODEL_CHAIN%% *}"
  RESOLVED_MODEL=""
  MODEL_FALLBACK_FROM=""
  MODEL_FALLBACK_REASON=""
  MODEL_PRICE_DELTA=""
  MODEL_CHAIN_EXHAUSTED=""

  if ! load_models; then
    RESOLVED_MODEL="$preferred"
    echo "NOTE: no model list available, so '$preferred' (the preferred model) could not be checked for availability. Using it unverified; the API will have the final say." >&2
    return 0
  fi

  for candidate in $MODEL_CHAIN; do
    reason="$(model_unavailable_reason "$candidate" "$endpoint")"
    if [ -z "$reason" ]; then
      RESOLVED_MODEL="$candidate"
      break
    fi
    [ "$candidate" = "$preferred" ] && MODEL_FALLBACK_REASON="$reason"
    echo "NOTE: skipping '$candidate' — $reason." >&2
  done

  if [ -z "$RESOLVED_MODEL" ]; then
    # Not a fallback: nothing was fallen back TO, so MODEL_FALLBACK_FROM stays
    # empty and the fallback lines stay silent. MODEL_CHAIN_EXHAUSTED is what
    # carries this case into the caller's output instead, because "the model
    # in your table is one we already know is broken" is the last thing that
    # should reach the user as stderr prose only.
    MODEL_CHAIN_EXHAUSTED="${MODEL_FALLBACK_REASON:-no usable model in the chain}"
    MODEL_FALLBACK_REASON=""
    RESOLVED_MODEL="$preferred"
    echo "ERROR: none of the models in the priority chain is usable right now ($MODEL_CHAIN)." >&2
    echo "Falling back to '$preferred' anyway so you get a definite answer rather than none; expect the API to reject it. Run 'ofox-image.sh models' and pass --model explicitly." >&2
    return 0
  fi

  [ "$RESOLVED_MODEL" = "$preferred" ] && return 0

  MODEL_FALLBACK_FROM="$preferred"
  rate_pref="$(output_image_rate "$preferred")" || rate_pref=""
  rate_used="$(output_image_rate "$RESOLVED_MODEL")" || rate_used=""
  if [ -n "$rate_pref" ] && [ -n "$rate_used" ]; then
    MODEL_PRICE_DELTA="$(awk -v a="$rate_used" -v b="$rate_pref" 'BEGIN {
      if (b + 0 == 0) { printf "%s vs %s per output token", a, b }
      else { printf "%.2fx the preferred rate (%s vs %s per output token)", a/b, a, b }
    }')"
  elif [ -n "$rate_used" ]; then
    MODEL_PRICE_DELTA="unknown — '$RESOLVED_MODEL' is $rate_used per output token, but there is no published rate for '$preferred' to compare it against"
  elif [ -n "$rate_pref" ]; then
    MODEL_PRICE_DELTA="unknown — no published output_image rate for '$RESOLVED_MODEL', the model actually chosen, so it cannot be compared with '$preferred' at $rate_pref per output token"
  else
    MODEL_PRICE_DELTA="unknown — neither '$preferred' nor '$RESOLVED_MODEL' has a published output_image rate on hand"
  fi
  return 0
}

# Compute what one image generation actually cost.
#
# The image endpoint returns no cost of its own (unlike the video API's
# usage.video_cost), and the platform exposes no billing endpoint to look it
# up afterwards — every /v1/usage, /v1/billing, /v1/credits, /v1/account
# variant answers 404. So the only honest figure is one computed here from
# the published rates and the response's own token counts.
#
# The formula, verified to eight decimal places against a real invoice line
# of $0.06723950 for a call reporting input_tokens=79, output_tokens=1120:
#
#   cost = input_tokens * pricing.input + output_tokens * pricing.output_image
#
# That is the finding worth keeping: an image response's output tokens bill
# entirely at the `output_image` rate ($60/M for Gemini), and the `output`
# rate ($3/M) does not enter into it. Reading the model page alone left those
# two readings 20x apart; the invoice settled it.
#
# Prints nothing and returns nonzero when the rates aren't available, so the
# caller says so rather than quoting a guess.
image_cost_for() {
  # $1 = model id, $2 = input tokens, $3 = output tokens
  local model="$1" in_tok="$2" out_tok="$3" entry
  case "$in_tok$out_tok" in
    *[!0-9]*|'') return 1 ;;
  esac
  entry="$(model_entry "$model")" || return 1
  [ -n "$entry" ] || return 1

  # The two endpoints that publish rates disagree on key names for the same
  # numbers: /v2/models/catalog calls them input/output, while /v1/models —
  # the list this script actually loads — calls them prompt/completion.
  # output_image is spelled the same in both. Accept either spelling rather
  # than depending on which source filled MODELS_FILE.
  printf '%s' "$entry" | jq -er --argjson i "$in_tok" --argjson o "$out_tok" '
    ((.pricing.input // .pricing.prompt) // empty | tonumber) as $ri
    | (.pricing.output_image // empty | tonumber) as $ro
    | ($i * $ri + $o * $ro)
    | . * 100000000 | round / 100000000
    | tostring' 2>/dev/null
}

# Compute what one EDIT actually cost. Separate from image_cost_for because
# an edit's bill has a component a generation's does not: the input image.
#
# Measured 2026-09-15, openai/gpt-image-2, an 854x480 PNG in, 1672x941 out:
#
#   "usage": {
#     "input_tokens": 608,
#     "input_tokens_details": { "image_tokens": 576, "text_tokens": 32 },
#     "output_tokens": 301,
#     "output_tokens_details": { "image_tokens": 301 },
#     "total_tokens": 909
#   }
#
# So the answer to "do edits report usage the way generations do" is: yes, and
# then some — input_tokens_details splits the prompt's text from the uploaded
# image, and the catalog carries a `pricing.image` rate ($0.000008 for
# gpt-image-2) distinct from `pricing.prompt` ($0.000005) that exists for
# exactly that. 576 of the 608 input tokens on that run were the picture.
#
# Which leaves two readings of the same numbers and no invoice to settle them:
#
#   flat  (generations' own formula, every input token at the prompt rate)
#           608*0.000005 + 301*0.00003            = 0.01207
#   split (text at the prompt rate, image at the image rate)
#           32*0.000005 + 576*0.000008 + 301*0.00003 = 0.013798
#
# 13% apart. This returns the DEARER of the two rather than picking a
# favourite, because the standing rule is never to under-quote: erring high
# costs a moment's surprise and erring low gets a bill approved that nobody
# agreed to. Neither reading has been held against a console billing line —
# note that image_cost_for's formula has only ever been invoice-checked on ONE
# model either, and on the other endpoint, so nothing about it transfers here
# by assumption.
edit_cost_for() {
  # $1 = model id, $2 = input tokens, $3 = output tokens,
  # $4 = input image tokens ("" when the response didn't split them),
  # $5 = input text tokens ("").
  local model="$1" in_tok="$2" out_tok="$3" img_tok="${4:-}" txt_tok="${5:-}" entry
  case "$in_tok$out_tok" in
    *[!0-9]* | '') return 1 ;;
  esac
  case "$img_tok" in *[!0-9]*) img_tok="" ;; esac
  case "$txt_tok" in *[!0-9]*) txt_tok="" ;; esac
  # Only trust the split when both halves are present and actually add up. A
  # partial or inconsistent split is a response shape we have not seen, and
  # guessing at it is how a 26x quote happened last time.
  if [ -z "$img_tok" ] || [ -z "$txt_tok" ] ||
    [ "$((img_tok + txt_tok))" -ne "$in_tok" ]; then
    img_tok=""
    txt_tok=""
  fi
  entry="$(model_entry "$model")" || return 1
  [ -n "$entry" ] || return 1

  printf '%s' "$entry" | jq -er \
    --argjson i "$in_tok" --argjson o "$out_tok" \
    --arg img "${img_tok:-}" --arg txt "${txt_tok:-}" '
    ((.pricing.input // .pricing.prompt) // empty | tonumber) as $ri
    | (.pricing.output_image // empty | tonumber) as $ro
    # pricing.image is the per-input-image-token rate. Several models publish
    # no such key; for them the image half simply bills at the text rate, so
    # the two readings collapse into one and the max below is a no-op.
    | ((.pricing.image // null) | if . == null then $ri else (. | tonumber) end) as $rimg
    | ($i * $ri + $o * $ro) as $flat
    | (if $img == "" then $flat
       else (($txt | tonumber) * $ri + ($img | tonumber) * $rimg + $o * $ro) end) as $split
    | (if $split > $flat then $split else $flat end)
    | . * 100000000 | round / 100000000
    | tostring' 2>/dev/null
}

# ---------------------------------------------------------------------------
# which model do we report, and price, once the response is back?
#
# Not the bookkeeping question it looks like. The response is supposed to echo
# the model in `.model`, and everything downstream — the printed MODEL line and
# the rate lookup behind IMAGE_COST — reads that echo.
#
# openai/gpt-image-2 does not send the field at all (measured 2026-09-02, two
# paid calls). The old code did `.model // "unknown"`, then looked the literal
# string "unknown" up in the rate table, found nothing, and printed
# "could not compute a cost — no published rates available for 'unknown'" —
# for a request this script had built itself, three hundred lines earlier, out
# of a model id it knew perfectly well. Both real calls came back with no cost
# figure for no reason. That is the bug this exists to close.
#
# The fix is a fallback, and the two ways the echo can disappoint us must NOT
# be collapsed into one:
#
#   - The field is ABSENT. Nothing was contradicted; the upstream just did not
#     bother to repeat itself. Use the requested id, and say the id came from
#     the request so nobody mistakes it for confirmation.
#   - The field is PRESENT and DIFFERENT. Something upstream routed, aliased or
#     downgraded the request. Report what it says, not what we asked for.
#     Overwriting it with the requested id would erase the only evidence that
#     it happened — and it is the model that ran, not the one that was asked
#     for, that the invoice will be computed from.
#
# MODEL_SOURCE is printed on every success, not only on the awkward paths. An
# agent relaying this can repeat a line; it cannot notice a line that was never
# there to begin with (same reasoning as print_estimate's always-one-line rule).
#
# Lives in its own function rather than inline in cmd_generate so that all
# three branches get a direct unit test, the way image_cost_for does:
# cmd_generate itself cannot be unit tested without a real, billable POST.
# ---------------------------------------------------------------------------

# Outputs of resolve_response_model. Globals rather than a printed value, for
# the same reason resolve_model uses RESOLVED_MODEL: the caller needs two
# answers (which id, and where it came from), and a `x=$(fn)` capture runs the
# function in a subshell, where the second one would be assigned and then
# thrown away.
RESPONSE_MODEL=""
RESPONSE_MODEL_SOURCE=""

resolve_response_model() {
  # $1 = the model id that was requested, $2 = the raw response body.
  # Sets RESPONSE_MODEL (the id to report and price) and RESPONSE_MODEL_SOURCE
  # ("response" or "request"). Warns on stderr when the echo is missing or
  # contradicts the request.
  local requested="$1" body="$2" echoed
  echoed=$(printf '%s' "$body" | jq -r '.model // empty' 2>/dev/null)

  if [ -z "$echoed" ]; then
    RESPONSE_MODEL="$requested"
    RESPONSE_MODEL_SOURCE="request"
    echo "NOTE: the response carried no 'model' field, so the MODEL line below" >&2
    echo "is the id that was requested ('$requested'), not one the API confirmed." >&2
    echo "The cost is priced at that model's published rates." >&2
    return 0
  fi

  RESPONSE_MODEL="$echoed"
  RESPONSE_MODEL_SOURCE="response"
  if [ "$echoed" != "$requested" ]; then
    echo "WARNING: upstream ran '$echoed', not the requested '$requested'." >&2
    echo "Reported and priced as '$echoed' — that is what will be billed." >&2
    echo "Anything measured from this run belongs to '$echoed'; do not record it" >&2
    echo "against '$requested' (see references/token-anchors.json)." >&2
  fi
  return 0
}

# ---------------------------------------------------------------------------
# pre-flight estimate
#
# The video side can quote a job exactly before submitting it: duration is an
# input and the rate is per second. Images cannot — they bill per output token
# and the token count only exists in the response. So the only honest
# pre-flight figure is one anchored to a real, previously measured call with
# the same model, labelled as rough, and withheld entirely when no such
# measurement exists (references/token-anchors.json).
#
# Applying one model's measured token count to another model would produce a
# number that looks exactly like the measured one and is not. That is the
# failure mode this refuses.
#
# THE SECOND failure mode, and the reason this block is pair-aware rather
# than one-number-per-model: an anchor is only valid for the --quality and
# --size it was measured at. Measured 2026-09-04, openai/gpt-image-2 spends
# 196 output tokens at low / 1024x1024 and 5063 at high / 1792x1024 — 26x,
# from two flags. The lookup this replaced read one count per model and never
# saw what was requested, so a real run at high / 1792x1024 was quoted at the
# low / 1024x1024 figure: approved at 0.6 cents, billed 15.4. See
# token-anchors.json's _what_the_count_does_depend_on.
#
# So the rule is: quote the measurement for the request's OWN pair when one
# exists, and otherwise quote the DEAREST measurement the model has, labelled
# as an upper bound with the pair it came from. Never interpolate between two
# measured points, and never let the quote come out below what the request
# could actually cost. An upper bound labelled as one is honest; an estimate
# that turns out to be 26x low is not, because by then someone has already
# said yes to it.
# ---------------------------------------------------------------------------

anchor_measurements() {
  # $1 = model id. Prints one measured point per line, TSV:
  #   <output_tokens>\t<quality>\t<size>\t<measured>
  # The anchor's own row first, then every entry in additional_measurements
  # (a second pair for a model that already has a row is added there rather
  # than overwriting the first, because both are true — each for its own
  # pair). Empty output means nothing has been measured for this model, which
  # is the "cannot be predicted" case rather than a reason to borrow.
  [ -f "$TOKEN_ANCHORS" ] || return 1
  jq -r --arg m "$1" '
    (.anchors[$m] // empty) as $a
    | ([$a] + ($a.additional_measurements // []))
    | map(select((.output_tokens | type) == "number"))
    | .[]
    | [ (.output_tokens | tostring),
        (.quality // "unrecorded"),
        (.size // "unrecorded"),
        (.measured // "an earlier run") ]
    | @tsv
  ' "$TOKEN_ANCHORS" 2>/dev/null
}

# Set to 1 by generate --dry-run, so the estimate can say "nothing is going to
# be billed here" rather than "the bill follows below". Same switch, same
# reason, as ofox-video.sh's DRY_RUN_ACTIVE.
DRY_RUN_ACTIVE=""

print_estimate() {
  # $1 = model id, $2 = image count (n), $3 = the --quality this request will
  # send, $4 = the --size it will send ("" when the flag was omitted, which
  # leaves the size to the API and is therefore just as unknown as "auto").
  #
  # ALWAYS prints exactly one "Estimated cost:" line. Silence is the one
  # outcome a calling agent cannot relay to a user — it can repeat a number,
  # and it can repeat "cannot be predicted", but it cannot notice the absence
  # of a line it was never told to expect. (Lifted from ofox-video.sh's
  # print_estimate, deliberately: the two scripts must behave the same way
  # here, because the same agent relays both into the same approval table.)
  local model="$1" count="${2:-1}" req_q="${3:-}" req_size="${4:-}"
  local rate measured per_image total tail
  local tokens="" pair_q="" pair_size=""
  local exact="" best="" best_tokens=-1 points=0
  local m_tokens m_q m_size m_date
  local measurements bound="" req_desc pair_desc
  # The rate comes from the model list, which validation usually loaded
  # already — but not when OFOX_SKIP_MODEL_VALIDATION=1. Load it here too
  # rather than quoting nothing for a run that skipped the check.
  load_models >/dev/null 2>&1 || true
  rate="$(output_image_rate "$model")" || rate=""
  measurements="$(anchor_measurements "$model")" || measurements=""

  # "auto", and an omitted flag, both resolve to something the server picks.
  # We cannot know which point was measured for a pair we cannot name, so
  # they take the upper-bound path rather than being matched optimistically
  # against whatever happens to be the model's first anchor row.
  local pair_known=1
  case "$req_q" in "" | auto) pair_known="" ;; esac
  case "$req_size" in "" | auto) pair_known="" ;; esac

  while IFS="$(printf '\t')" read -r m_tokens m_q m_size m_date; do
    [ -n "${m_tokens:-}" ] || continue
    case "$m_tokens" in '' | *[!0-9]*) continue ;; esac
    points=$((points + 1))
    if [ -n "$pair_known" ] && [ "$m_q" = "$req_q" ] && [ "$m_size" = "$req_size" ]; then
      exact="$m_tokens|$m_q|$m_size|$m_date"
    fi
    # Ranking on output tokens is CORRECT here, unlike on the edit path.
    # Audited 2026-09-17 when the edit selector was fixed: a generation's cost
    # is tokens * rate — ONE term, with a rate that is constant per model — so
    # "most output tokens" and "dearest" are the same ordering by
    # construction. An edit adds a second term for the uploaded image, which
    # dominates at large input sizes, and that is what made the same key wrong
    # over there. If a per-point rate is ever introduced here, this stops being
    # safe and must move to comparing computed cost, as print_edit_estimate
    # now does.
    if [ "$m_tokens" -gt "$best_tokens" ]; then
      best_tokens="$m_tokens"
      best="$m_tokens|$m_q|$m_size|$m_date"
    fi
  done <<EOF
$measurements
EOF

  local chosen=""
  if [ -n "$exact" ]; then
    chosen="$exact"
  elif [ -n "$best" ]; then
    chosen="$best"
    bound=1
  fi

  if [ -z "$chosen" ]; then
    echo "Estimated cost: cannot be predicted for '$model' — no real call's output-token count has been recorded for it (see references/token-anchors.json). An image bills per output token, and the token count only exists once the response comes back. Say so; do not substitute another model's figure." >&2
    return 0
  fi

  tokens="${chosen%%|*}"
  chosen="${chosen#*|}"
  pair_q="${chosen%%|*}"
  chosen="${chosen#*|}"
  pair_size="${chosen%%|*}"
  measured="${chosen#*|}"
  [ -n "$measured" ] || measured="an earlier run"

  if [ -z "$rate" ]; then
    echo "Estimated cost: cannot be predicted — no published output_image rate for '$model' (offline, or the model is missing from the list). Its measured output-token count is $tokens (at --quality $pair_q --size $pair_size); the rate to multiply it by is what's missing." >&2
    return 0
  fi

  per_image="$(awk -v t="$tokens" -v r="$rate" 'BEGIN { printf "%.4f", t * r }')"
  total="$(awk -v t="$tokens" -v r="$rate" -v n="$count" 'BEGIN { printf "%.4f", t * r * n }')"

  if [ -n "$DRY_RUN_ACTIVE" ]; then
    tail="Nothing is being billed by this run."
  else
    tail="The exact figure is the IMAGE_COST line below, computed from the response's own token counts."
  fi

  # The pair travels with the price, in the same line, so that a table built
  # from nothing but this one sentence still shows whether the number belongs
  # to what was asked for.
  pair_desc="--quality $pair_q --size $pair_size"
  req_desc="--quality ${req_q:-unset, left to the API} --size ${req_size:-unset, left to the API}"

  local label="ROUGH"
  [ -n "$bound" ] && label="ROUGH UPPER BOUND"

  if [ "$count" -gt 1 ] 2>/dev/null; then
    printf 'Estimated cost: %s ~$%s total = %s images x ~$%s each (%s output tokens x $%s/token, measured %s at %s). %s\n' \
      "$label" "$total" "$count" "$per_image" "$tokens" "$rate" "$measured" "$pair_desc" "$tail" >&2
  else
    printf 'Estimated cost: %s ~$%s (%s output tokens x $%s/token, measured %s at %s). %s\n' \
      "$label" "$per_image" "$tokens" "$rate" "$measured" "$pair_desc" "$tail" >&2
  fi

  if [ -n "$bound" ]; then
    # "the dearest of the 1 measured point" implies a comparison that did not
    # happen. With one point on file, "the only" is the true sentence and the
    # Weak ceiling note below is the consequence.
    local points_desc
    if [ "$points" -eq 1 ]; then
      points_desc="the only measured point"
    else
      points_desc="the dearest of the $points measured points"
    fi
    echo "  UPPER BOUND because nothing has been measured at this request's own pair ($req_desc). This is $points_desc for '$model', quoted as a ceiling so a table errs high on the token count instead of low — erring low is what got a 0.6-cent quote approved for a frame that billed 15.4 cents. Nothing is interpolated between measured points; see references/token-anchors.json. It bounds the output-token component only, the prompt's input tokens excluded, as every figure here does." >&2
    if [ "$points" -le 1 ]; then
      # Worth being exact about: with one measured point, "dearest" and "only"
      # are the same sentence, and a ceiling over a single sample is not a
      # ceiling over the model. gpt-image-2's own two points are 26x apart.
      echo "  Weak ceiling, and say so in the table: '$model' has been measured at exactly one pair, so this is the dearest by default rather than a bound anyone has tested. If its token count climbs with size or quality the way openai/gpt-image-2's does (196 to 5063, 26x), a real bill at $req_desc can come in above this. Measure that pair and add it to references/token-anchors.json rather than leaning on the label." >&2
    fi
  else
    echo "  Measured at the same --quality and --size this request sends, which is the only condition under which an image anchor means anything: on openai/gpt-image-2 the same model's measured points are 26x apart across two flags." >&2
  fi

  if [ "$count" -gt 1 ] 2>/dev/null; then
    echo "  Rough, twice over: the token count is one model's measured average, not a promise, and whether output tokens scale linearly with --n has never been measured. Treat the per-image figure as the reliable half." >&2
  else
    echo "  Rough because an image's token count is only known after the fact; this reuses a measured one for the same model. It also excludes the input-token component (the prompt), which on every observed call was a fraction of a cent." >&2
  fi
  return 0
}

edit_anchor_measurements() {
  # $1 = model id. One measured EDIT per line, TSV:
  #   <output_tokens>\t<input_tokens>\t<input_size>\t<quality>\t<measured>
  # Kept in a separate section of token-anchors.json from the generation
  # anchors, and read by a separate function, because an edit's token counts
  # are not a generation's: the same model on the same day reported 196 output
  # tokens for a 1024x1024 generation and 301 for an edit, and an edit also
  # bills 576 input tokens for the picture that a generation never has. Reusing
  # anchor_measurements() here would quote one endpoint's numbers for the
  # other's request — the borrowed-number failure that file exists to refuse.
  [ -f "$TOKEN_ANCHORS" ] || return 1
  jq -r --arg m "$1" '
    (.edit_anchors[$m] // empty) as $a
    | ([$a] + ($a.additional_measurements // []))
    | map(select((.output_tokens | type) == "number"))
    | .[]
    | [ (.output_tokens | tostring),
        ((.input_tokens // 0) | tostring),
        (.input_size // "unrecorded"),
        (.quality // "unrecorded"),
        (.measured // "an earlier run") ]
    | @tsv
  ' "$TOKEN_ANCHORS" 2>/dev/null
}

print_edit_estimate() {
  # $1 = model id, $2 = image count (n), $3 = the --quality this request will
  # send ("" when omitted, which lets the server default apply),
  # $4 = the input image's measured WxH, or "" when it could not be measured.
  #
  # Same contract as print_estimate: ALWAYS exactly one "Estimated cost:" line,
  # because an agent can relay a number or the words "cannot be predicted" but
  # cannot notice a line that was never printed.
  #
  # An edit's estimate is weaker than a generation's, and the wording says so
  # rather than hiding it. A generation anchor is valid for a (quality, size)
  # pair; an edit has a THIRD axis nobody has varied — the input image's own
  # dimensions, which is what the 576 input image tokens were charged for and
  # which scales with the picture the caller happens to pass. One measured
  # point on one model at one input size is not a bound on anything, and
  # labelling it one would repeat the mistake that got a 0.6-cent quote
  # approved for a 15.4-cent frame.
  local model="$1" count="${2:-1}" req_q="${3:-}" in_size="${4:-}"
  local rate rate_img per_image total tail
  local best="" best_tokens=-1 best_cost=-1 points=0 exact="" bound=""
  local m_out m_in m_insize m_q m_date m_cost measurements
  local a_out a_in a_insize a_q a_date

  load_models >/dev/null 2>&1 || true
  rate="$(output_image_rate "$model")" || rate=""
  measurements="$(edit_anchor_measurements "$model")" || measurements=""

  # Resolved BEFORE the loop on purpose: the dearest point has to be chosen on
  # the money, and the money needs the input-token rate as well as the output
  # one. This used to sit below the loop, which is why the loop could only
  # compare output tokens.
  rate_img="$(printf '%s' "$(model_entry "$model")" | jq -er '.pricing.image // empty' 2>/dev/null)" || rate_img=""
  [ -n "$rate_img" ] || rate_img="$(printf '%s' "$(model_entry "$model")" | jq -er '(.pricing.input // .pricing.prompt) // empty' 2>/dev/null)" || rate_img=""
  [ -n "$rate_img" ] || rate_img=0

  # Same shape as print_estimate: quote the point measured at this request's
  # own conditions when one exists, otherwise the DEAREST point, never an
  # interpolation between them. The condition that matters differs though.
  # For a generation it is (quality, size); for an edit the two measured
  # points have identical output size, quality and model and still differ 2.3x
  # in output tokens, while the INPUT image is what the bill tracks — so the
  # input's size is what a point is matched on here.
  #
  # "DEAREST" IS MEASURED IN MONEY, NOT IN OUTPUT TOKENS, and that is a fix
  # rather than a preference. Through 1.13.0 this loop kept the point with the
  # highest output_tokens. The four measured points run 129 / 229 / 301 / 129
  # output tokens ordered by input size, and 0.006054 / 0.009182 / 0.013894 /
  # 0.016438 in real cost — so the genuinely dearest point (1792x1008) has the
  # EQUAL-LOWEST output count and the old key skipped straight past it. Any
  # input without an exact match was handed 0.013894 as an "upper bound" over
  # a point known to bill 0.016438. On an edit the uploaded picture is most of
  # the bill at large sizes (1508 image tokens = 74% of that run), so output
  # tokens are the smaller half and ranking on them ranks on the wrong thing.
  # A bound that is not the largest known value is not a bound.
  #
  # With no published rate there is no money to compare, so the old
  # output-token ordering stays as the fallback — that path cannot print a
  # figure anyway and only names the point's token counts.
  while IFS="$(printf '\t')" read -r m_out m_in m_insize m_q m_date; do
    [ -n "${m_out:-}" ] || continue
    case "$m_out" in '' | *[!0-9]*) continue ;; esac
    points=$((points + 1))
    if [ -n "$in_size" ] && [ "$m_insize" = "$in_size" ]; then
      exact="$m_out|$m_in|$m_insize|$m_q|$m_date"
    fi
    if [ -n "$rate" ]; then
      m_cost="$(awk -v o="$m_out" -v i="$m_in" -v r="$rate" -v ri="$rate_img" \
        'BEGIN { printf "%.10f", o * r + i * ri }')"
      if awk -v a="$m_cost" -v b="$best_cost" 'BEGIN { exit !(a > b) }'; then
        best_cost="$m_cost"
        best="$m_out|$m_in|$m_insize|$m_q|$m_date"
      fi
    elif [ "$m_out" -gt "$best_tokens" ]; then
      best_tokens="$m_out"
      best="$m_out|$m_in|$m_insize|$m_q|$m_date"
    fi
  done <<EOF
$measurements
EOF

  if [ -n "$exact" ]; then
    best="$exact"
  elif [ -n "$best" ]; then
    bound=1
  fi

  if [ -z "$best" ]; then
    # No figures in this message, on purpose. It is the one place where the
    # right answer is "there is no number", and a number quoted here to
    # illustrate why — even another model's, even clearly labelled — is a
    # number an agent can lift into a cost table. The reasoning survives
    # without it; the reader who wants the evidence has the file named below.
    echo "Estimated cost: cannot be predicted for '$model' — no real EDIT's token counts have been recorded for it (see references/token-anchors.json, edit_anchors). Its generation anchors do not transfer: the one model measured on both spent visibly different output tokens on the two endpoints, and an edit additionally bills the uploaded image, which a generation has no equivalent of. Say so plainly; do not substitute a generation figure, another model's figure, or anything derived from one." >&2
    return 0
  fi

  a_out="${best%%|*}"; best="${best#*|}"
  a_in="${best%%|*}"; best="${best#*|}"
  a_insize="${best%%|*}"; best="${best#*|}"
  a_q="${best%%|*}"
  a_date="${best#*|}"
  [ -n "$a_date" ] || a_date="an earlier run"

  if [ -z "$rate" ]; then
    echo "Estimated cost: cannot be predicted — no published output_image rate for '$model' (offline, or the model is missing from the list). Its measured edit spent $a_out output tokens and $a_in input tokens (input image $a_insize, --quality $a_q); the rate to multiply them by is what's missing." >&2
    return 0
  fi
  # rate_img was resolved before the selection loop — see the note there.

  per_image="$(awk -v o="$a_out" -v i="$a_in" -v r="$rate" -v ri="$rate_img" \
    'BEGIN { printf "%.4f", o * r + i * ri }')"
  total="$(awk -v o="$a_out" -v i="$a_in" -v r="$rate" -v ri="$rate_img" -v n="$count" \
    'BEGIN { printf "%.4f", (o * r + i * ri) * n }')"

  if [ -n "$DRY_RUN_ACTIVE" ]; then
    tail="Nothing is being billed by this run."
  else
    tail="The exact figure is the EDIT_COST line below, computed from the response's own token counts."
  fi

  local label="ROUGH"
  [ -n "$bound" ] && label="ROUGH UPPER BOUND"

  if [ "$count" -gt 1 ] 2>/dev/null; then
    printf 'Estimated cost: %s ~$%s total = %s images x ~$%s each (%s output + %s input tokens, measured %s on an input image of %s at --quality %s). %s\n' \
      "$label" "$total" "$count" "$per_image" "$a_out" "$a_in" "$a_date" "$a_insize" "$a_q" "$tail" >&2
  else
    printf 'Estimated cost: %s ~$%s (%s output + %s input tokens, measured %s on an input image of %s at --quality %s). %s\n' \
      "$label" "$per_image" "$a_out" "$a_in" "$a_date" "$a_insize" "$a_q" "$tail" >&2
  fi

  # The input image is the axis that makes this weaker than a generation
  # estimate, so it gets named every time, and gets named louder when the
  # request's own input is a different size from the measured one.
  if [ -n "$bound" ]; then
    if [ -n "$in_size" ]; then
      echo "  UPPER BOUND because nothing has been measured on a $in_size input for '$model'; this is the dearest of $points measured point(s), quoted as a ceiling so the figure errs high rather than low. An edit bills the uploaded picture as input tokens, and the points on record move with it but NOT in proportion to it — 240 image tokens for a 320x180 input, 256 for 256x256, 576 for 854x480 and 1508 for 1792x1008; 854x480 has 6.3x the pixels of 256x256 for 2.25x the tokens, and 1792x1008 has 4.4x the pixels of 854x480 for 2.6x the tokens. That input term is most of the bill at large sizes (1508 tokens = 74% of the 1792x1008 run), which is why the dearest point is chosen on computed cost rather than on output tokens — those run 129/229/301/129 across the four points and do not track the input at all. Nothing is interpolated between them; see references/token-anchors.json's edit_anchors." >&2
    else
      echo "  UPPER BOUND because the input image could not be measured (ffprobe missing, or --image-url was used), so no measured point can be matched to it. This is the dearest of $points measured point(s). Nothing is interpolated; see references/token-anchors.json's edit_anchors." >&2
    fi
  else
    echo "  Measured on an input image of exactly this size, which is the condition that matters most on this endpoint: two of the points on record share a model, a quality and an identical 1672x941 output and still differ 2.3x in output tokens. What the bill tracks is the uploaded image, not the delivered one. The token count is still only exact after the fact." >&2
  fi
  if [ "$points" -le 1 ]; then
    echo "  Single sample: '$model' has been measured on exactly one edit, so this is not a ceiling anyone has tested — on the generations endpoint the same model's measured points sit 26x apart across two flags. Measure more pairs and add them to references/token-anchors.json rather than leaning on this line." >&2
  fi
  if [ -n "$req_q" ] && [ "$req_q" != "$a_q" ]; then
    echo "  Different --quality too: you are sending '$req_q', the measurement was at '$a_q'. On the generations endpoint that one flag moved the token count 26x." >&2
  fi
  if [ "$count" -gt 1 ] 2>/dev/null; then
    echo "  And --n $count multiplies it: whether output tokens scale linearly with --n has never been measured on either endpoint." >&2
  fi
  return 0
}

infer_extension() {
  # $1 = the --output-format value the caller requested (may be empty).
  # The documented response shape has no format/output_format field of its
  # own (only created/data/model/size/quality/usage) — so when the caller
  # didn't request a format, there is nothing in the response to infer it
  # from either. Default to png: it's what the documented example request
  # uses, it's lossless, and every model/provider fronted by this endpoint
  # is expected to support it.
  local output_format="$1"
  case "$output_format" in
    png) echo "png" ;;
    jpeg|jpg) echo "jpg" ;;
    webp) echo "webp" ;;
    *) echo "png" ;;
  esac
}

usage() {
  cat >&2 <<'EOF'
ofox-image.sh — Ofox image generation API client (synchronous: request,
decode, save; no job id, no polling).

  ofox-image.sh check
  ofox-image.sh models [--endpoint generations|edits]
  ofox-image.sh generate --prompt "..." --quality VAL [--model NAME] [OPTIONS]
  ofox-image.sh edit --image FILE --prompt "..." [--model NAME] [OPTIONS]

generate draws a new image from text. edit changes an image you already have
(POST /v1/images/edits, multipart) — pass the file with --image and say what
to change with --prompt. Not every model can edit: 'models --endpoint edits'
lists the ones that can, read live from the catalog.

--model is optional: omit it (or pass "auto") to use the first available
model in the cheapest-first priority chain, resolved before anything is
quoted. Add --dry-run to any generate or edit call to validate it and print a
rough cost estimate without sending a request — no API key needed.

Two things about edit that generate does not have. It bills the image you
upload as input tokens on top of the output (576 of 608 input tokens on the
one measured run), and it does NOT reject bad parameter values the way
generate does — an unknown --quality was silently accepted and rendered a
billable image. The client-side checks are the guard there, so --dry-run
first is worth more here, not less.

Producing a first frame for a video job? Pass --target-aspect 16:9 (or
--target-size 1280x720). The size enum this API accepts has no 16:9 or 9:16
entry, so such a frame always needs cropping, and an attached frame's ratio
becomes the finished video's ratio.

Run with no arguments for this message. See the top of this file, or
skills/ofox-image-core/SKILL.md and references/api-params.md, for the full
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

check_image_tools() {
  # Only needed when --target-aspect/--target-size is in play: those flags are
  # a promise that the delivered file is the ratio asked for, and the only way
  # to keep it is to measure the written file and crop it. Guarded the same
  # way curl and jq are, and for the same reason — checked BEFORE the one
  # billable call, so a missing tool costs nothing to discover. Fail loud
  # rather than fail open here: falling open would mean handing back a
  # wrong-ratio frame that then propagates into a paid video job.
  local missing=0
  if ! command -v ffprobe >/dev/null 2>&1; then
    echo "ERROR: ffprobe is not installed, and --target-aspect/--target-size cannot be honoured without it." >&2
    missing=1
  fi
  if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "ERROR: ffmpeg is not installed, and --target-aspect/--target-size cannot be honoured without it." >&2
    missing=1
  fi
  if [ "$missing" -ne 0 ]; then
    echo "  macOS:          brew install ffmpeg   (ffprobe ships with it)" >&2
    echo "  Debian/Ubuntu:  sudo apt-get install ffmpeg" >&2
    echo "  Other:          https://ffmpeg.org/download.html" >&2
    echo "Or drop --target-aspect/--target-size: everything else in this script, including" >&2
    echo "--dry-run pricing, works without ffmpeg. You then own the measure-and-crop step" >&2
    echo "by hand, and the size the API reports is not evidence of what it wrote." >&2
    return 1
  fi
  return 0
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
  local ok=0
  check_curl_jq || ok=1
  check_api_key || ok=1
  if [ "$ok" -eq 0 ]; then
    echo "OK: curl, jq, and OFOX_API_KEY are all present."
  fi
  return "$ok"
}

cmd_models() {
  # Lists the image models with their per-image output price. Needs no API key
  # — GET /v1/models is public — so it is safe to run before signing up.
  check_curl_jq || return 2

  # --endpoint decides which capability is being listed. This is how "which
  # models accept an edit" is answered in this skill: by asking the catalog,
  # live, every time. There is no edit-support table in this file to go stale.
  local endpoint="$GENERATIONS_ENDPOINT" what="image generation"
  while [ $# -gt 0 ]; do
    case "$1" in
      --endpoint)
        [ $# -ge 2 ] || { echo "ERROR: --endpoint requires a value (generations|edits)." >&2; return 1; }
        case "$2" in
          generations) endpoint="$GENERATIONS_ENDPOINT"; what="image generation" ;;
          edits) endpoint="$EDITS_ENDPOINT"; what="image editing" ;;
          *) echo "ERROR: --endpoint must be 'generations' or 'edits' (got '$2')." >&2; return 1 ;;
        esac
        shift 2
        ;;
      *) echo "ERROR: unknown option '$1' for models." >&2; return 1 ;;
    esac
  done

  load_models || true
  if [ -z "$MODELS_FILE" ]; then
    echo "ERROR: could not obtain a model list (no network, no cache, no bundled snapshot)." >&2
    return 3
  fi

  echo "Models serving $endpoint ($what) — source: $MODELS_SOURCE"
  echo
  jq -r --arg e "$endpoint" '
    ["MODEL", "$/OUTPUT IMAGE TOKEN"],
    (.data[]
      | select((.supported_endpoints // []) | index($e))
      | [ .id + (if .is_deprecated then " (deprecated)" else "" end),
          (.pricing.output_image // "-") ])
    | @tsv' "$MODELS_FILE" | column -t -s "$(printf '\t')"

  echo
  echo "Prices are per output image token, not per image. 'generate' and 'edit'"
  echo "turn that into an IMAGE_COST/EDIT_COST line for you; references/pricing.md"
  echo "has the formula and the invoice it was verified against."
  if [ "$endpoint" = "$EDITS_ENDPOINT" ]; then
    echo
    # "live" would be a lie on the snapshot/stale-cache rungs, and this block
    # is reachable from all of them. Name the source the header already
    # printed instead of asserting the best case.
    echo "This list IS the answer to 'which models accept an edit' — it is read"
    echo "from each model's supported_endpoints (source: $MODELS_SOURCE, see the"
    echo "header above), never from a table in this script. Confirmed both ways"
    echo "on 2026-09-15: a model missing from this list is refused with"
    echo "endpoint_not_supported, and models on it ran."
    echo "An edit also bills the image you upload, which a generation never does."
  else
    echo "This skill documents these in depth:"
    echo "  $DOCUMENTED_MODELS"
    echo "Others work but their size/quality support is not documented here."
  fi

  # Show the default that a caller who omits --model would actually get,
  # resolved right now against this same list — not just the head of the
  # chain, which may be the one that is unavailable.
  echo
  echo "Priority chain used when --model is omitted (cheapest first):"
  local rank=1 candidate reason
  for candidate in $MODEL_CHAIN; do
    reason="$(model_unavailable_reason "$candidate" "$endpoint")"
    if [ -n "$reason" ]; then
      printf '  %s. %s  [unavailable: %s]\n' "$rank" "$candidate" "$reason"
    else
      printf '  %s. %s\n' "$rank" "$candidate"
    fi
    rank=$((rank + 1))
  done
  resolve_model "$endpoint" 2>/dev/null
  echo "Resolves right now to: $RESOLVED_MODEL"
  if [ -n "$MODEL_FALLBACK_FROM" ]; then
    echo "  (fallback from $MODEL_FALLBACK_FROM — $MODEL_FALLBACK_REASON; $MODEL_PRICE_DELTA)"
  elif [ -n "$MODEL_CHAIN_EXHAUSTED" ]; then
    echo "  (nothing in the chain is usable — that is the preferred model, and it is $MODEL_CHAIN_EXHAUSTED. Pass --model explicitly.)"
  fi
  return 0
}

# ---------------------------------------------------------------------------
# error mapping
#
# This endpoint's error vocabulary has NOT been broadly explored. A real
# rejected call (2026-08-29, an invalid extra_body.provider.type) showed the
# actual error shape is {"error": {"message", "type", "code"}} — an
# OpenAI-SDK-style shape, DIFFERENT from the video API's {code, message}
# shape where "code" was a real semantic string. Here, error.code was
# literally the HTTP status as a NUMBER (400), not a semantic string — the
# real classifier is error.type (only "invalid_request_error" confirmed so
# far). Two message-only gotchas (Gemini + /v1/images/edits, Gemini + n) are
# doc-prose-only and are both caught client-side before any network call in
# this script anyway. Anything else below is deliberately treated as
# unconfirmed rather than guessed: the raw error.message is always printed
# either way, since it is often more specific than any fixed mapping this
# script could offer.
# ---------------------------------------------------------------------------

print_api_error() {
  # $1 = context ("generate" or "edit"), $2 = http_code, $3 = response body
  local context="$1" http_code="$2" body="$3" err_type code message param
  err_type=$(printf '%s' "$body" | jq -r '.error.type // empty' 2>/dev/null)
  code=$(printf '%s' "$body" | jq -r '.error.code // empty' 2>/dev/null)
  message=$(printf '%s' "$body" | jq -r '.error.message // empty' 2>/dev/null)
  param=$(printf '%s' "$body" | jq -r '.error.param // empty' 2>/dev/null)
  echo "ERROR: Ofox API rejected the $context request (HTTP $http_code)." >&2
  case "$err_type" in
    invalid_request_error)
      echo "  error.type: invalid_request_error — the request itself was rejected as malformed or unsupported. On /v1/images/edits this is also the type for a missing image ('at least one image or image_url is required'), an unsupported input format, and a missing/invalid API key. See the upstream message below for the specific reason." >&2
      ;;
    model_not_found)
      echo "  error.type: model_not_found — the model id does not exist. Observed with error.code 404. Run 'ofox-image.sh models' for the current list; a typo in a vendor prefix (bailian/ vs qwen/, say) lands here." >&2
      ;;
    endpoint_not_supported)
      echo "  error.type: endpoint_not_supported — the model exists but does not serve this endpoint. Observed with error.code 400, on a model whose catalog supported_endpoints array omits it. Run 'ofox-image.sh models --endpoint edits' to see which models accept an edit; this script normally catches this before the request, so seeing it means the model list was unavailable or the check was skipped." >&2
      ;;
    "")
      echo "  (no error.type in the response body)" >&2
      ;;
    *)
      echo "  error.type: $err_type — not yet confirmed/documented for this endpoint (observed so far: invalid_request_error, image_generation_user_error, model_not_found, endpoint_not_supported). See the raw upstream message below and https://ofox.ai/docs/api/openai/images for current guidance." >&2
      ;;
  esac
  if [ -n "$code" ]; then
    # Measured 2026-09-15 on /v1/images/edits: code is 404 for model_not_found
    # and 400 for endpoint_not_supported — the HTTP status again — but it is
    # literally null on the two validation rejections (missing image, bad
    # mimetype), which instead carry a `param` field the generations endpoint
    # has never sent. So code is neither a semantic string nor reliably
    # present. error.type is the classifier; nothing here branches on code.
    echo "  error.code: $code (the HTTP status again, not a semantic string — and on this endpoint it can be absent entirely. error.type above is the classifier.)" >&2
  fi
  if [ -n "$param" ]; then
    echo "  error.param: $param" >&2
  fi
  if [ -n "$message" ]; then
    echo "  Upstream message: $message" >&2
  elif [ -z "$err_type" ] && [ -z "$code" ]; then
    echo "  Raw response body:" >&2
    printf '%s\n' "$body" >&2
  fi
}

# ---------------------------------------------------------------------------
# generate: validate params, build payload, POST, decode, save
# ---------------------------------------------------------------------------

cmd_generate() {
  if ! check_curl_jq; then return 2; fi

  local model=""
  local prompt=""
  local quality=""
  local size=""
  local n=""
  local output_format=""
  local background=""
  local extra_json=""
  # Whether --extra-json was written on the command line at all. bash cannot
  # tell "flag omitted" from "flag given an empty value" by looking at the
  # value, and treating the two as one is a fail-open: an empty value from a
  # command substitution that died (jq over ARG_MAX is the measured case on
  # the sibling video script) skipped every check below AND the merge, and
  # the request went out and billed without the fields the caller meant.
  local extra_json_seen=""
  local out_dir="$PWD"
  local out_name=""
  local dry_run=""
  local target_aspect=""
  local target_size=""
  local key val

  while [ $# -gt 0 ]; do
    key="$1"
    case "$key" in
      --model|--prompt|--quality|--size|--n|--output-format|--background|--extra-json|--out-dir|--out-name|--target-aspect|--target-size)
        if [ $# -lt 2 ]; then
          echo "ERROR: $key requires a value." >&2
          return 1
        fi
        val="$2"
        shift 2
        ;;
      --dry-run)
        dry_run=1
        shift
        continue
        ;;
      *)
        echo "ERROR: unknown option '$key' for generate." >&2
        return 1
        ;;
    esac
    case "$key" in
      --model) model="$val" ;;
      --prompt) prompt="$val" ;;
      --quality) quality="$val" ;;
      --size) size="$val" ;;
      --n) n="$val" ;;
      --output-format) output_format="$val" ;;
      --background) background="$val" ;;
      --extra-json) extra_json="$val"; extra_json_seen=1 ;;
      --out-dir) out_dir="$val" ;;
      --out-name) out_name="$val" ;;
      --target-aspect) target_aspect="$val" ;;
      --target-size) target_size="$val" ;;
    esac
  done

  # --- validation: all of it runs before the one billable call, and the only
  #     network it does is the public, keyless GET /v1/models ---

  [ -n "$dry_run" ] && DRY_RUN_ACTIVE=1

  # Whether the id below was typed by the caller or produced by MODEL_CHAIN.
  # It changes what an error about that model has to say: a user who never
  # passed --model cannot connect "openai/gpt-image-2 rejects this" to
  # anything they wrote unless the message tells them where it came from.
  local model_from_chain=""
  if [ -z "$model" ] || [ "$model" = "auto" ]; then
    model_from_chain=1
    # Resolve the chain to one concrete id here, before the estimate is
    # printed and before the payload is built, so everything downstream —
    # including whatever the caller shows the user for approval — names the
    # model that would really run.
    resolve_model
    model="$RESOLVED_MODEL"
    if [ -n "$MODEL_FALLBACK_FROM" ]; then
      echo "NOTE: falling back to '$model' — the preferred '$MODEL_FALLBACK_FROM' is $MODEL_FALLBACK_REASON. Price: $MODEL_PRICE_DELTA." >&2
    elif [ -n "$MODEL_CHAIN_EXHAUSTED" ]; then
      echo "NOTE: no model in the priority chain is usable ('$model', the preferred one, is $MODEL_CHAIN_EXHAUSTED). It is being used anyway so there is a definite model to quote, but expect the API to reject it — say so before asking anyone to approve this." >&2
    fi
  fi

  if [ "${OFOX_SKIP_MODEL_VALIDATION:-}" != "1" ] && load_models; then
    local entry
    entry="$(model_entry "$model")"
    if [ -z "$entry" ]; then
      # An id the list doesn't have. Only treat that as an error when the list
      # is current — a snapshot may simply predate the model.
      if [ "$MODELS_SOURCE" = "snapshot" ] || [ "$MODELS_SOURCE" = "stale-cache" ]; then
        echo "NOTE: '$model' is not in the $MODELS_SOURCE model list, which may just be out of date. Sending it anyway; the API will validate it." >&2
      else
        echo "ERROR: --model '$model' is not in the Ofox model list. Run 'ofox-image.sh models' to see what is available." >&2
        return 1
      fi
    elif ! printf '%s' "$entry" | jq -e '(.supported_endpoints // []) | index("/v1/images/generations")' >/dev/null 2>&1; then
      echo "ERROR: --model '$model' exists but does not support image generation (/v1/images/generations). Run 'ofox-image.sh models' to see the image models." >&2
      return 1
    elif printf '%s' "$entry" | jq -e '.is_deprecated == true' >/dev/null 2>&1; then
      echo "NOTE: '$model' is marked deprecated by Ofox. It still runs for now; consider moving to a current model." >&2
    fi
  fi

  if [ -z "$prompt" ]; then
    echo "ERROR: --prompt is required." >&2
    return 1
  fi

  if [ -z "$quality" ]; then
    echo "ERROR: --quality is required (Ofox documents it as a required field). Valid values: $VALID_QUALITIES. No default is assumed here — not every value is confirmed to apply to every model." >&2
    return 1
  fi
  if ! list_contains "$quality" "$VALID_QUALITIES"; then
    echo "ERROR: --quality '$quality' is not a documented value. Valid values: $VALID_QUALITIES" >&2
    return 1
  fi
  # Then against the model that will actually serve the request, when its
  # accepted set is known first-hand. The union above says the value exists
  # somewhere in this API; this says it exists on the model being used.
  local model_q
  model_q="$(model_qualities "$model")"
  if [ -n "$model_q" ] && ! list_contains "$quality" "$model_q"; then
    echo "ERROR: --quality '$quality' is not accepted by '$model', the model this request would use. It accepts: $model_q." >&2
    if [ -n "$model_from_chain" ]; then
      echo "  No --model was passed, so '$model' came from the priority chain (MODEL_CHAIN), not from anything you typed — but it is still the model that would have run." >&2
    fi
    echo "  That set is the API's own enumeration rather than a guess; model_qualities() in this script quotes the refusal it was read off. Two fixes: pass a --quality from that list, or pin a --model that accepts '$quality'." >&2
    if [ "$quality" = "standard" ]; then
      echo "  For 'standard' specifically: microsoft/mai-image-2.5-flash accepted it on nine real runs, so '--model microsoft/mai-image-2.5-flash --quality standard' is the pin that keeps this value." >&2
    fi
    echo "  Caught before the request, which is the point of catching it at all: this combination used to pass --dry-run and then fail at submission with HTTP 400." >&2
    return 1
  fi

  if [ -n "$size" ] && ! list_contains "$size" "$VALID_SIZES"; then
    echo "ERROR: --size '$size' is not a documented value. Valid values: $VALID_SIZES" >&2
    return 1
  fi

  # --- the target ratio, and the request size that best serves it ---
  #
  # 16:9 and 9:16 are not in VALID_SIZES and cannot be — see the geometry
  # section above for the ratio table. So a caller who needs one of those
  # states it here and this script owns the crop, instead of every caller
  # re-deriving "measure the file, then crop" and one of them forgetting.
  local target_active="" target_label=""
  local target_rw="" target_rh="" target_px_w="" target_px_h=""
  local pair reduced

  if [ -n "$target_aspect" ] && [ -n "$target_size" ]; then
    echo "ERROR: pass --target-aspect or --target-size, not both — --target-size '$target_size' already fixes the ratio." >&2
    return 1
  fi

  if [ -n "$target_aspect" ]; then
    if ! pair="$(parse_ratio_pair "$target_aspect" ':')"; then
      echo "ERROR: --target-aspect must be W:H with two positive integers (got '$target_aspect'). Examples: 16:9, 9:16, 4:3, 1:1." >&2
      return 1
    fi
    reduced="$(reduce_ratio "${pair% *}" "${pair#* }")"
    target_rw="${reduced% *}"
    target_rh="${reduced#* }"
    target_label="${target_rw}:${target_rh}"
    target_active=1
  elif [ -n "$target_size" ]; then
    if ! pair="$(parse_ratio_pair "$target_size" 'x')"; then
      echo "ERROR: --target-size must be WxH with two positive integers (got '$target_size'). Examples: 1280x720, 1792x1008." >&2
      return 1
    fi
    target_px_w="${pair% *}"
    target_px_h="${pair#* }"
    reduced="$(reduce_ratio "$target_px_w" "$target_px_h")"
    target_rw="${reduced% *}"
    target_rh="${reduced#* }"
    target_label="${target_px_w}x${target_px_h} (${target_rw}:${target_rh})"
    target_active=1
  fi

  if [ -n "$target_active" ]; then
    # Checked before anything is quoted or spent: these flags promise an
    # exact ratio, and the promise needs ffprobe to measure and ffmpeg to
    # crop.
    if ! check_image_tools; then return 2; fi

    if [ -z "$size" ]; then
      local picked
      if ! picked="$(select_size_for_target "$target_rw" "$target_rh" "$target_px_w" "$target_px_h")"; then
        echo "ERROR: no --size this API accepts can be cropped to $target_label without upscaling." >&2
        echo "  Accepted sizes: $VALID_SIZES" >&2
        echo "  Ask for fewer pixels, or drop --target-size and crop the result yourself." >&2
        return 1
      fi
      size="$picked"
      echo "NOTE: requesting --size $size, the size that best serves the target $target_label (chosen from: $VALID_SIZES)." >&2
      echo "  The delivered file will be centre-cropped to $target_label. This API's size enum contains no 16:9 or 9:16 entry, so a crop is unavoidable, not a fallback." >&2
    elif [ "$size" = "auto" ]; then
      echo "NOTE: --size auto leaves the request size to the model, so there is nothing to check the target $target_label against up front." >&2
      echo "  The crop still happens: whatever comes back is measured and cropped to $target_label, or the run fails loudly." >&2
    else
      # An explicit --size is respected, never silently replaced. It is only
      # checked against the target, and only warned about.
      local ecw="${size%x*}" ech="${size#*x}" edims
      if edims="$(crop_dims_for "$ecw" "$ech" "$target_rw" "$target_rh")"; then
        if [ -n "$target_px_w" ] &&
          { [ "${edims% *}" -lt "$target_px_w" ] || [ "${edims#* }" -lt "$target_px_h" ]; }; then
          echo "NOTE: --size $size cannot cover the target ${target_px_w}x${target_px_h} — cropped to ${target_rw}:${target_rh} it is only ${edims% *}x${edims#* }, and this script never upscales." >&2
          echo "  Keeping your explicit --size; the run will fail after generating rather than deliver an upscaled frame. Drop --size to let it pick, or ask for fewer pixels." >&2
        fi
      else
        echo "NOTE: --size $size is smaller than one whole unit of ${target_rw}:${target_rh}; the crop will fail after generating. Drop --size to let this script pick a size." >&2
      fi
    fi
  fi

  if [ -n "$n" ]; then
    case "$n" in
      ''|*[!0-9]*)
        echo "ERROR: --n must be a positive integer (got '$n')." >&2
        return 1
        ;;
    esac
    if [ "$n" -lt 1 ] || [ "$n" -gt 10 ]; then
      echo "ERROR: --n must be between 1 and 10 (got $n)." >&2
      return 1
    fi
    if [ "$model" = "$NO_N_MODEL" ]; then
      echo "ERROR: --n is not supported by $NO_N_MODEL at all (documented gotcha: passing n, even n=1, errors for this model). Omit --n." >&2
      return 1
    fi
  fi

  if [ -n "$output_format" ] && ! list_contains "$output_format" "$VALID_OUTPUT_FORMATS"; then
    echo "ERROR: --output-format '$output_format' is not a documented value. Valid values: $VALID_OUTPUT_FORMATS" >&2
    return 1
  fi

  if [ -n "$background" ] && ! list_contains "$background" "$VALID_BACKGROUNDS"; then
    echo "ERROR: --background '$background' is not a documented value. Valid values: $VALID_BACKGROUNDS" >&2
    return 1
  fi

  if [ -n "$out_name" ]; then
    case "$out_name" in
      */*)
        echo "ERROR: --out-name must be a bare filename with no path separators (got '$out_name')." >&2
        return 1
        ;;
      "")
        echo "ERROR: --out-name must not be empty." >&2
        return 1
        ;;
    esac
  fi

  # An explicitly empty --extra-json is an error; omitting the flag behaves
  # byte-for-byte as it always did. The asymmetry is the point — no existing
  # caller that leaves the flag off is affected, and the one shape that used
  # to be dropped in silence now stops the run before anything is billed.
  if [ -n "$extra_json_seen" ] && [ -z "$extra_json" ]; then
    echo "ERROR: --extra-json was given an empty value." >&2
    echo "This usually means a command substitution produced nothing. Before 1.14.0 that empty string was treated as 'flag not passed': no JSON check, nothing merged, and the request sent and billed without your extra fields." >&2
    echo "Build the JSON into a variable, check it with 'jq -e .', then pass it — or drop the flag if you meant to send nothing." >&2
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
    # Merged last, so its keys win over the flags — including over the model,
    # size and n that the estimate was just computed from. A field this
    # script owns through a flag is therefore refused here, exactly as the
    # edit path already refuses one through --extra-form. Everything without
    # a flag (extra_body.provider.type, the documented case) still passes.
    local clash
    clash=$(printf '%s' "$extra_json" | jq -r '
      ["model","prompt","quality","size","n","output_format","background"] as $guarded
      | [ keys_unsorted[] | select(. as $k | $guarded | index($k)) ] | join(", ")')
    if [ -n "$clash" ]; then
      echo "ERROR: --extra-json sets $clash, which this script validates and prices from its own flag(s). Use the flag instead: --model, --prompt, --quality, --size, --n, --output-format, --background." >&2
      echo "A key merged through --extra-json wins over the flags and is applied AFTER the cost estimate is computed, so this would send a request that does not match the price anyone approved." >&2
      echo "Fields with no flag are unaffected — extra_body.provider.type still passes through here." >&2
      return 1
    fi
    if printf '%s' "$extra_json" | jq -e 'has("input_images")' >/dev/null 2>&1; then
      echo "ERROR: --extra-json sets 'input_images' — image-to-image is out of scope for ofox-image-core v1 (text-to-image only). See SKILL.md." >&2
      return 1
    fi
    if printf '%s' "$extra_json" | jq -e '.stream == true' >/dev/null 2>&1; then
      echo "ERROR: --extra-json sets 'stream: true' — this script only parses a plain JSON response body, not a streamed one. Omit stream or leave it false." >&2
      return 1
    fi
    # There used to be a narrower rule here, rejecting an `n` key only when
    # the resolved model was $NO_N_MODEL. The clash rule above now refuses
    # `n` for every model — `n` has a flag — so that branch could never run
    # again and was removed rather than left as a check nobody can make fire.
    # Passing n through --n is still refused for $NO_N_MODEL specifically,
    # above, where that message lives.
  fi

  # --out-dir is resolved (created if needed) and validated BEFORE the
  # network call — a local filesystem problem should never be discovered
  # only after a real, billable request has already been sent.
  local out_dir_input="$out_dir"
  mkdir -p "$out_dir" 2>/dev/null
  out_dir=$(cd "$out_dir" 2>/dev/null && pwd)
  if [ -z "$out_dir" ]; then
    echo "ERROR: --out-dir '$out_dir_input' could not be created or entered (bad path or missing permissions)." >&2
    return 4
  fi

  # A dry run sends no authenticated request, so it must not demand a key:
  # pricing a job is exactly what someone does *before* signing up, and this
  # repo's rule is to guide a keyless user rather than dead-end them.
  if [ -z "$dry_run" ]; then
    if ! check_api_key; then return 2; fi
  fi

  # --- build the request payload ---

  local payload='{}'
  payload=$(printf '%s' "$payload" | jq --arg v "$model" '.model=$v')
  payload=$(printf '%s' "$payload" | jq --arg v "$prompt" '.prompt=$v')
  payload=$(printf '%s' "$payload" | jq --arg v "$quality" '.quality=$v')
  [ -n "$size" ] && payload=$(printf '%s' "$payload" | jq --arg v "$size" '.size=$v')
  [ -n "$n" ] && payload=$(printf '%s' "$payload" | jq --argjson v "$n" '.n=$v')
  [ -n "$output_format" ] && payload=$(printf '%s' "$payload" | jq --arg v "$output_format" '.output_format=$v')
  [ -n "$background" ] && payload=$(printf '%s' "$payload" | jq --arg v "$background" '.background=$v')

  if [ -n "$extra_json" ]; then
    # Through a temp file and --slurpfile, not --argjson: a command-line
    # value is bound by ARG_MAX, and --extra-json is exactly where a caller
    # might embed something large. Same fix the video script's frame_images
    # build already carries.
    local tmp_extra merged
    tmp_extra=$(mktemp)
    printf '%s' "$extra_json" >"$tmp_extra"
    merged=$(printf '%s' "$payload" | jq --slurpfile extra "$tmp_extra" '. * $extra[0]')
    rm -f "$tmp_extra"
    # A failed merge leaves the command substitution empty, which without
    # this would POST an empty body to a billable endpoint.
    if [ -z "$merged" ]; then
      echo "ERROR: merging --extra-json into the request body failed, so nothing was submitted and nothing was billed." >&2
      return 1
    fi
    payload="$merged"
  fi

  # Say what this will cost before spending anything. The quality and size
  # go in because an image anchor is only valid for the pair it was measured
  # at — and $size here is the EFFECTIVE one, after --target-aspect has
  # picked a request size, not the flag the caller typed.
  print_estimate "$model" "${n:-1}" "$quality" "$size"

  if [ -n "$dry_run" ]; then
    # Everything above already ran: arguments parsed, model resolved against
    # the chain, parameters validated, out-dir created, payload built, price
    # quoted. Nothing below runs — the POST is the next statement — so nothing
    # is submitted and nothing is billed.
    echo "DRY RUN — nothing was submitted and nothing was billed." >&2
    echo "Re-run without --dry-run to generate." >&2
    echo "STATUS dry_run"
    echo "MODEL $model"
    echo "QUALITY $quality"
    [ -n "$size" ] && echo "SIZE $size"
    if [ -n "$target_active" ]; then
      # What an approval table needs: the size that will be REQUESTED and the
      # ratio the delivered file is promised at. The exact cropped pixels are
      # deliberately not predicted here — they are computed from the written
      # file, because the response's own size field is not evidence of what
      # was written on two of the three models measured.
      echo "TARGET_ASPECT ${target_rw}:${target_rh}"
      [ -n "$target_px_w" ] && echo "TARGET_SIZE ${target_px_w}x${target_px_h}"
    fi
    echo "N ${n:-1}"
    if [ -n "$MODEL_FALLBACK_FROM" ]; then
      echo "MODEL_FALLBACK_FROM $MODEL_FALLBACK_FROM"
      echo "MODEL_FALLBACK_REASON $MODEL_FALLBACK_REASON"
      echo "MODEL_PRICE_DELTA $MODEL_PRICE_DELTA"
    fi
    [ -n "$MODEL_CHAIN_EXHAUSTED" ] && echo "MODEL_CHAIN_EXHAUSTED $MODEL_CHAIN_EXHAUSTED"
    return 0
  fi

  # --- the one and only network call ---

  echo "Requesting image generation from Ofox (model=$model)..." >&2
  local tmp_body http_code curl_rc body
  tmp_body=$(mktemp)
  http_code=$(curl -sS -o "$tmp_body" -w '%{http_code}' \
    --connect-timeout "$CONNECT_TIMEOUT" --max-time "$GENERATE_MAX_TIME" \
    -X POST "$API_BASE/images/generations" \
    -H "Authorization: Bearer $OFOX_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$payload")
  curl_rc=$?
  body=$(cat "$tmp_body")
  rm -f "$tmp_body"

  if [ "$curl_rc" -ne 0 ]; then
    echo "ERROR: could not reach the Ofox API (curl exit $curl_rc) — no HTTP response was received at all." >&2
    echo "This is a synchronous, no-job-id endpoint: there is no poll/dashboard job entry to check by id." >&2
    echo "Check your usage/billing history at ${GET_KEY_URL} before deciding whether to retry." >&2
    return 5
  fi

  if [ "$http_code" != "200" ]; then
    print_api_error "generate" "$http_code" "$body"
    return 3
  fi

  # --- decode and save ---

  local count
  count=$(printf '%s' "$body" | jq -r '.data | length' 2>/dev/null)
  if [ -z "$count" ] || [ "$count" = "null" ] || ! [ "$count" -gt 0 ] 2>/dev/null; then
    echo "ERROR: got HTTP 200 but the response has no usable data[] entries — unexpected response shape." >&2
    echo "Raw response body:" >&2
    printf '%s\n' "$body" >&2
    return 3
  fi

  local ext base_name
  ext=$(infer_extension "$output_format")
  base_name="${out_name:-ofox_image_$(date +%Y%m%d%H%M%S)_$$}"

  local idx=0 item b64 stem outpath rawpath paths=() raw_paths=()
  local measured_size="" final_size="" crop_dims
  while IFS= read -r item; do
    b64=$(printf '%s' "$item" | jq -r '.b64_json // empty')
    if [ -z "$b64" ]; then
      echo "ERROR: data[$idx] has no b64_json field — unexpected response shape." >&2
      echo "Raw response body:" >&2
      printf '%s\n' "$body" >&2
      return 3
    fi
    if [ "$count" -gt 1 ]; then
      stem="${out_dir%/}/${base_name}_${idx}"
    else
      stem="${out_dir%/}/${base_name}"
    fi
    # With a target, the API's own bytes land at <stem>-uncropped and the
    # cropped frame takes the plain <stem> name. Two reasons for that split:
    # a caller (or an older one, parsing IMAGE_PATH) gets the file that
    # actually meets the target without changing how it reads the output, and
    # the untouched original survives for a human who wants to re-crop
    # differently. If the crop fails, <stem> never appears and the run exits
    # nonzero — there is no path at which a wrong-ratio frame is sitting where
    # the right one was promised.
    if [ -n "$target_active" ]; then
      rawpath="${stem}-uncropped.${ext}"
      outpath="${stem}.${ext}"
    else
      rawpath="${stem}.${ext}"
      outpath="$rawpath"
    fi
    if ! decode_b64_to_file "$b64" "$rawpath"; then
      echo "ERROR: failed to base64-decode image data[$idx] to $rawpath." >&2
      return 3
    fi
    raw_paths+=("$rawpath")

    # Measure the FILE. Never the response's size field: on
    # microsoft/mai-image-2.5-flash the request, the response and the file
    # have disagreed three ways on three separate runs.
    local this_measured=""
    this_measured="$(measure_image_file "$rawpath")" || this_measured=""
    [ "$idx" -eq 0 ] && measured_size="$this_measured"

    if [ -n "$target_active" ]; then
      if [ -z "$this_measured" ]; then
        echo "ERROR: could not measure '$rawpath', so the target ${target_rw}:${target_rh} cannot be guaranteed." >&2
        echo "The generated image is on disk and was billed; it is NOT cropped and its ratio is unverified." >&2
        echo "Do not attach it to a video job without measuring it by hand — an attached frame's ratio becomes the video's ratio." >&2
        return 3
      fi
      local mw="${this_measured%x*}" mh="${this_measured#*x}"
      if ! crop_dims="$(crop_dims_for "$mw" "$mh" "$target_rw" "$target_rh")"; then
        echo "ERROR: '$rawpath' measured ${this_measured}, too small to hold one whole unit of ${target_rw}:${target_rh}." >&2
        echo "The image was generated and billed; it is on disk uncropped. Nothing wrong-ratio was written to ${outpath}." >&2
        return 3
      fi
      local cw="${crop_dims% *}" ch="${crop_dims#* }"
      if [ -n "$target_px_w" ] &&
        { [ "$cw" -lt "$target_px_w" ] || [ "$ch" -lt "$target_px_h" ]; }; then
        echo "ERROR: '$rawpath' measured ${this_measured}; cropped to ${target_rw}:${target_rh} that is only ${cw}x${ch}, short of the requested ${target_px_w}x${target_px_h}." >&2
        echo "This script crops and scales down, never up — an upscaled frame is a worse deliverable than a loud failure here." >&2
        echo "The image was generated and billed and is on disk at the -uncropped path. Ask for fewer pixels, or drop --size so a larger request size can be chosen." >&2
        return 3
      fi
      if ! crop_image_to "$rawpath" "$outpath" "$cw" "$ch" "$target_px_w" "$target_px_h"; then
        echo "ERROR: ffmpeg could not crop '$rawpath' to ${cw}x${ch}." >&2
        echo "The image was generated and billed and is on disk uncropped at that path." >&2
        return 3
      fi
      if [ "$idx" -eq 0 ]; then
        if [ -n "$target_px_w" ]; then
          final_size="${target_px_w}x${target_px_h}"
        else
          final_size="${cw}x${ch}"
        fi
      fi
    fi
    paths+=("$outpath")
    idx=$((idx + 1))
  done < <(printf '%s' "$body" | jq -c '.data[]')

  local resp_model resp_size resp_quality input_tokens output_tokens total_tokens
  resolve_response_model "$model" "$body"
  resp_model="$RESPONSE_MODEL"
  resp_size=$(printf '%s' "$body" | jq -r '.size // "unknown"')
  resp_quality=$(printf '%s' "$body" | jq -r '.quality // "unknown"')
  input_tokens=$(printf '%s' "$body" | jq -r '.usage.input_tokens // "unknown"')
  output_tokens=$(printf '%s' "$body" | jq -r '.usage.output_tokens // "unknown"')
  total_tokens=$(printf '%s' "$body" | jq -r '.usage.total_tokens // "unknown"')

  echo "STATUS completed"
  for outpath in "${paths[@]}"; do
    echo "IMAGE_PATH $outpath"
  done
  # Only when a crop happened, so the untouched original is findable and the
  # single IMAGE_PATH above stays unambiguously "the file to attach".
  if [ -n "$target_active" ]; then
    for rawpath in "${raw_paths[@]}"; do
      echo "IMAGE_PATH_UNCROPPED $rawpath"
    done
  fi
  echo "MODEL $resp_model"
  echo "MODEL_SOURCE $RESPONSE_MODEL_SOURCE"
  # Only worth a line when the two disagree — and then it is the single most
  # important line in the block, because it is the difference between a bill
  # that reconciles and one that does not.
  if [ "$resp_model" != "$model" ]; then
    echo "MODEL_REQUESTED $model"
  fi
  # Three different facts, and conflating any two of them is the mistake this
  # skill keeps paying for:
  #   SIZE         what the API says it produced — not evidence of anything
  #   SIZE_ACTUAL  what the written file really measures
  #   SIZE_FINAL   what the cropped deliverable is (only when a target was set)
  # With --n > 1 the last two describe the first image; one request produces
  # one size.
  echo "SIZE $resp_size"
  if [ -n "$measured_size" ]; then
    echo "SIZE_ACTUAL $measured_size"
    if [ "$measured_size" != "$resp_size" ] && [ "$resp_size" != "unknown" ]; then
      echo "NOTE: the API reported SIZE $resp_size but the file measures $measured_size. The file is the fact; the response field is not." >&2
    fi
  else
    echo "SIZE_ACTUAL unmeasured"
    echo "NOTE: could not measure the written file's real dimensions (ffprobe missing or unreadable file), so SIZE above is unverified — and on two of the three models measured here it has been wrong. Install ffmpeg to have this checked: brew install ffmpeg / sudo apt-get install ffmpeg." >&2
  fi
  if [ -n "$final_size" ]; then
    echo "SIZE_FINAL $final_size"
    echo "TARGET_ASPECT ${target_rw}:${target_rh}"
  fi
  echo "QUALITY $resp_quality"
  echo "USAGE_INPUT_TOKENS $input_tokens"
  echo "USAGE_OUTPUT_TOKENS $output_tokens"
  echo "USAGE_TOTAL_TOKENS $total_tokens"

  # Needs the model list for the rates; it may not have loaded (offline, no
  # cache). Report the cost when it can be computed, and say why not when it
  # can't — never split the difference with an approximation.
  local image_cost=""
  load_models >/dev/null 2>&1 || true
  image_cost="$(image_cost_for "$resp_model" "$input_tokens" "$output_tokens")" || image_cost=""
  if [ -n "$image_cost" ]; then
    echo "IMAGE_COST $image_cost"
  else
    echo "NOTE: could not compute a cost — no published rates available for" >&2
    echo "'$resp_model' (offline, or the model is missing from the list)." >&2
    echo "The token counts above are exact; see references/pricing.md for the" >&2
    echo "formula to apply by hand." >&2
  fi
  return 0
}

# ---------------------------------------------------------------------------
# edit: validate params, assemble a multipart form, POST, decode, save
#
# POST /v1/images/edits takes an image you already have and changes it. The
# measured contract, all of it from real calls rather than from documentation:
#
#   multipart ONLY. An application/json body with "model" set came back
#     "You must provide a model parameter" — the field was not even seen. So
#     this builds -F form fields; there is no JSON payload to print.
#   an image is required. Neither image nor image_url -> 400
#     invalid_request_error, "at least one image or image_url is required".
#   input formats are enumerated by the API's own refusal: image/jpeg,
#     image/png, image/webp.
#   the model is checked BEFORE any parameter. A model whose catalog entry
#     omits /v1/images/edits is refused with endpoint_not_supported, and that
#     refusal fires ahead of any field validation.
#   and the one that costs money: PARAMETERS ARE BARELY VALIDATED. --quality
#     ultra_not_a_value was accepted and rendered, six times, on six models.
#     The generations endpoint refuses a bad quality for free; this one bills
#     you for it. Every client-side check below is therefore load-bearing in a
#     way the same check on generate is not.
#
# What an edit really is, checked against the artifact rather than against
# STATUS completed (2026-09-15, openai/gpt-image-2, an 854x480 UI screenshot
# in, "change only the blue button to green, leave every other pixel alone"):
# every string in the source survived verbatim — "Billing Settings",
# "$29.00", "Seats included 3" — and the button turned green. Mean absolute
# difference against the rescaled source was 5.27/255 overall but 84.27 inside
# the button, which is 1.1% of the frame and accounted for 58% of all
# substantially changed pixels. A text-to-image generation from that prompt
# could not have reproduced that text. It edits the image.
# ---------------------------------------------------------------------------

cmd_edit() {
  if ! check_curl_jq; then return 2; fi

  local model=""
  local image=""
  local image_url=""
  local prompt=""
  local quality=""
  local size=""
  local n=""
  local output_format=""
  local background=""
  local out_dir="$PWD"
  local out_name=""
  local dry_run=""
  local target_aspect=""
  local target_size=""
  local extra_form=()
  local key val

  while [ $# -gt 0 ]; do
    key="$1"
    case "$key" in
      --model|--image|--image-url|--prompt|--quality|--size|--n|--output-format|--background|--out-dir|--out-name|--target-aspect|--target-size|--extra-form)
        if [ $# -lt 2 ]; then
          echo "ERROR: $key requires a value." >&2
          return 1
        fi
        val="$2"
        shift 2
        ;;
      --dry-run)
        dry_run=1
        shift
        continue
        ;;
      *)
        echo "ERROR: unknown option '$key' for edit." >&2
        return 1
        ;;
    esac
    case "$key" in
      --model) model="$val" ;;
      --image) image="$val" ;;
      --image-url) image_url="$val" ;;
      --prompt) prompt="$val" ;;
      --quality) quality="$val" ;;
      --size) size="$val" ;;
      --n) n="$val" ;;
      --output-format) output_format="$val" ;;
      --background) background="$val" ;;
      --out-dir) out_dir="$val" ;;
      --out-name) out_name="$val" ;;
      --target-aspect) target_aspect="$val" ;;
      --target-size) target_size="$val" ;;
      --extra-form) extra_form+=("$val") ;;
    esac
  done

  # --- validation: all of it before the one billable call. On this endpoint
  #     that is not a nicety. The API validates almost nothing itself, so a
  #     check skipped here is a bill, not a round trip. ---

  [ -n "$dry_run" ] && DRY_RUN_ACTIVE=1

  # --- the input image ---
  if [ -n "$image" ] && [ -n "$image_url" ]; then
    echo "ERROR: pass --image or --image-url, not both." >&2
    return 1
  fi
  if [ -z "$image" ] && [ -z "$image_url" ]; then
    echo "ERROR: an input image is required — pass --image PATH (a local file, the primary path) or --image-url URL." >&2
    echo "  The API says the same thing if you don't: 'at least one image or image_url is required'." >&2
    return 1
  fi

  local image_ext=""
  if [ -n "$image" ]; then
    if [ ! -f "$image" ]; then
      echo "ERROR: --image '$image' is not a file that exists." >&2
      return 1
    fi
    if [ ! -r "$image" ]; then
      echo "ERROR: --image '$image' exists but cannot be read (permissions)." >&2
      return 1
    fi
    if [ ! -s "$image" ]; then
      echo "ERROR: --image '$image' is empty." >&2
      return 1
    fi
    # Absolute, like every path this script reports. INPUT_IMAGE is printed
    # next to IMAGE_PATH so the two can be compared, and a relative path is
    # only resolvable from whatever directory the caller happened to be in.
    local image_dir image_base
    image_dir="$(cd "$(dirname "$image")" 2>/dev/null && pwd)" || image_dir=""
    image_base="$(basename "$image")"
    [ -n "$image_dir" ] && image="${image_dir%/}/$image_base"
    # Extension check against the set the API enumerated in its own refusal.
    # Cheap, and it turns "upload 4MB then get told no" into an instant local
    # error. It is a format check only — the API reads the real mimetype and
    # has the final say, so a correctly-named file with the wrong bytes still
    # comes back as invalid_request_error (free, nothing rendered).
    image_ext="${image##*.}"
    image_ext="$(printf '%s' "$image_ext" | tr '[:upper:]' '[:lower:]')"
    if ! list_contains "$image_ext" "$EDIT_INPUT_FORMATS"; then
      echo "ERROR: --image '$image' does not look like a supported format. This endpoint enumerates exactly three: image/jpeg, image/png, image/webp (so .$EDIT_INPUT_FORMATS)." >&2
      echo "  That list is the API's own wording from a real rejection, not a guess. Convert the file first, e.g. 'ffmpeg -i in.gif out.png'." >&2
      return 1
    fi
  fi

  # --- the model, resolved against the EDITS endpoint ---
  local model_from_chain=""
  if [ -z "$model" ] || [ "$model" = "auto" ]; then
    model_from_chain=1
    resolve_model "$EDITS_ENDPOINT"
    model="$RESOLVED_MODEL"
    if [ -n "$MODEL_FALLBACK_FROM" ]; then
      echo "NOTE: falling back to '$model' — the preferred '$MODEL_FALLBACK_FROM' is $MODEL_FALLBACK_REASON. Price: $MODEL_PRICE_DELTA." >&2
    elif [ -n "$MODEL_CHAIN_EXHAUSTED" ]; then
      echo "NOTE: no model in the priority chain can serve an edit ('$model', the preferred one, is $MODEL_CHAIN_EXHAUSTED). It is being used anyway so there is a definite model to quote, but expect the API to reject it — say so before asking anyone to approve this." >&2
    fi
  fi

  if [ "${OFOX_SKIP_MODEL_VALIDATION:-}" != "1" ] && load_models; then
    local entry
    entry="$(model_entry "$model")"
    if [ -z "$entry" ]; then
      if [ "$MODELS_SOURCE" = "snapshot" ] || [ "$MODELS_SOURCE" = "stale-cache" ]; then
        echo "NOTE: '$model' is not in the $MODELS_SOURCE model list, which may just be out of date. Sending it anyway; the API will validate it." >&2
      else
        echo "ERROR: --model '$model' is not in the Ofox model list. Run 'ofox-image.sh models --endpoint edits' to see what can edit." >&2
        return 1
      fi
    elif ! printf '%s' "$entry" | jq -e --arg e "$EDITS_ENDPOINT" '(.supported_endpoints // []) | index($e)' >/dev/null 2>&1; then
      # Caught locally against the same field the API decides on, so this
      # costs nothing. Left to the API it is a free rejection too, but
      # only because the model check happens to run before anything renders —
      # not a property worth depending on.
      echo "ERROR: --model '$model' exists but does not serve $EDITS_ENDPOINT, so it cannot edit an image." >&2
      if [ -n "$model_from_chain" ]; then
        echo "  No --model was passed, so '$model' came from the priority chain (MODEL_CHAIN), not from anything you typed." >&2
      fi
      echo "  Run 'ofox-image.sh models --endpoint edits' for the models that can. That list is read live from each model's supported_endpoints; this script keeps no edit-support table of its own." >&2
      return 1
    elif printf '%s' "$entry" | jq -e '.is_deprecated == true' >/dev/null 2>&1; then
      echo "NOTE: '$model' is marked deprecated by Ofox. It still runs for now; consider moving to a current model." >&2
    fi
  fi

  # --- the rest of the parameters ---
  if [ -z "$prompt" ]; then
    echo "ERROR: --prompt is required — it is the instruction describing what to change." >&2
    echo "  Required by this script, not known to be required by the API: the only way to find that out is to send an edit without one, and on this endpoint anything that is not rejected renders and bills." >&2
    return 1
  fi

  # --quality: the union check only, and deliberately NOT the per-model
  # enumeration model_qualities() holds. That set was read off a rejection
  # from /v1/images/generations, and this repo has already been bitten by
  # assuming two endpoints of one API behave symmetrically — image models
  # carry no image_attributes to match video_attributes, and this endpoint's
  # response shape differs from generations' too. Applying a generations
  # enumeration here would be inferring, not measuring.
  #
  # The union check stays, and matters more here than it does on generate:
  # generate's version saves a free round trip, this one is the only thing
  # that catches a typo before it is billed.
  if [ -n "$quality" ] && ! list_contains "$quality" "$VALID_QUALITIES"; then
    echo "ERROR: --quality '$quality' is not a documented value. Valid values: $VALID_QUALITIES" >&2
    echo "  Worth catching locally: measured 2026-09-15, this endpoint does NOT reject an unknown --quality the way /v1/images/generations does — it ignored the value and rendered a billable image anyway. A typo here costs money, not a round trip." >&2
    return 1
  fi

  if [ -n "$size" ] && ! list_contains "$size" "$VALID_SIZES"; then
    echo "ERROR: --size '$size' is not a documented value. Valid values: $VALID_SIZES" >&2
    return 1
  fi

  if [ -n "$n" ]; then
    case "$n" in
      ''|*[!0-9]*)
        echo "ERROR: --n must be a positive integer (got '$n')." >&2
        return 1
        ;;
    esac
    if [ "$n" -lt 1 ] || [ "$n" -gt 10 ]; then
      echo "ERROR: --n must be between 1 and 10 (got $n)." >&2
      return 1
    fi
    if [ "$model" = "$NO_N_MODEL" ]; then
      echo "ERROR: --n is not supported by $NO_N_MODEL at all (documented gotcha: passing n, even n=1, errors for this model). Omit --n." >&2
      return 1
    fi
  fi

  if [ -n "$output_format" ] && ! list_contains "$output_format" "$VALID_OUTPUT_FORMATS"; then
    echo "ERROR: --output-format '$output_format' is not a documented value. Valid values: $VALID_OUTPUT_FORMATS" >&2
    return 1
  fi

  if [ -n "$background" ] && ! list_contains "$background" "$VALID_BACKGROUNDS"; then
    echo "ERROR: --background '$background' is not a documented value. Valid values: $VALID_BACKGROUNDS" >&2
    return 1
  fi

  if [ -n "$out_name" ]; then
    case "$out_name" in
      */*)
        echo "ERROR: --out-name must be a bare filename with no path separators (got '$out_name')." >&2
        return 1
        ;;
      "")
        echo "ERROR: --out-name must not be empty." >&2
        return 1
        ;;
    esac
  fi

  local form_item
  for form_item in ${extra_form+"${extra_form[@]}"}; do
    case "$form_item" in
      *=*) : ;;
      *)
        echo "ERROR: --extra-form must be KEY=VALUE (got '$form_item')." >&2
        return 1
        ;;
    esac
    # Every field this function adds to the form from a flag. The list used to
    # be image/image_url/model/prompt while the builder below also set
    # quality, size, n, output_format and background — the guard and the
    # builder had drifted, and the comment on --extra-json above claimed the
    # two hatches were symmetric, which made the gap read as covered.
    # A duplicate part is not a harmless
    # duplicate: the server picks one of the two (which one is not this
    # script's to decide), the value that arrived here skipped the flag's
    # validation — `quality` is checked per-model, and the union-table defect
    # this repo already has a gotcha for lives on that path — and it is added
    # to the form AFTER print_edit_estimate has been computed from the flags.
    # `n` is the sharp one: it multiplies the bill directly, so
    # `--extra-form "n=10"` quoted one image, printed `N 1`, and asked for
    # ten. That is the never-under-quote rule broken through the escape
    # hatch, which is the same shape --extra-json is refused for in
    # cmd_generate above. Keep the two lists in step with what each path
    # actually sends.
    case "${form_item%%=*}" in
      ''|image|image_url|model|prompt|quality|size|n|output_format|background)
        echo "ERROR: --extra-form '${form_item%%=*}' collides with a field this script sets from a flag. Use the flag: --model, --prompt, --quality, --size, --n, --output-format, --background, --image/--image-url." >&2
        echo "A second multipart part with the same name skips that flag's validation and is added after the cost estimate is computed, so this would send a request that does not match the price anyone approved — '--extra-form \"n=10\"' quoted one image and asked for ten." >&2
        return 1
        ;;
    esac
    # curl's -F reads two prefixes on a VALUE as filesystem instructions:
    # '@path' uploads that file, '<path' reads the file and sends its
    # contents as the field value. Passed straight through, --extra-form was
    # therefore a way to make this script upload any file the user can read
    # (`--extra-form "mask=@$HOME/.ssh/id_rsa"`) to whatever API_BASE points
    # at. The field itself stays available; only the two curl prefixes are
    # refused, so every ordinary key=value pair is untouched.
    #
    # The script's own -F "image=@$image" / -F "image_url=<$url_file" are
    # built from --image / --image-url, which are validated paths this
    # function chose. They do not come through here.
    case "${form_item#*=}" in
      @*|\<*)
        echo "ERROR: --extra-form '${form_item%%=*}' has a value starting with '$(printf '%s' "${form_item#*=}" | cut -c1)', which curl reads as a filesystem instruction: '@path' uploads that file and '<path' sends that file's contents as the field value." >&2
        echo "This script will not use --extra-form to read local files — it is an escape hatch for extra FIELDS, not a file picker. To send an image, use --image (upload) or --image-url." >&2
        echo "If the value is genuinely meant to start with that character, there is no way to send it through this flag today; say what you need it for rather than working around this." >&2
        return 1
        ;;
    esac
  done

  # --- the target ratio (same contract, same reason, as generate) ---
  local target_active="" target_label=""
  local target_rw="" target_rh="" target_px_w="" target_px_h=""
  local pair reduced

  if [ -n "$target_aspect" ] && [ -n "$target_size" ]; then
    echo "ERROR: pass --target-aspect or --target-size, not both — --target-size '$target_size' already fixes the ratio." >&2
    return 1
  fi
  if [ -n "$target_aspect" ]; then
    if ! pair="$(parse_ratio_pair "$target_aspect" ':')"; then
      echo "ERROR: --target-aspect must be W:H with two positive integers (got '$target_aspect'). Examples: 16:9, 9:16, 4:3, 1:1." >&2
      return 1
    fi
    reduced="$(reduce_ratio "${pair% *}" "${pair#* }")"
    target_rw="${reduced% *}"
    target_rh="${reduced#* }"
    target_label="${target_rw}:${target_rh}"
    target_active=1
  elif [ -n "$target_size" ]; then
    if ! pair="$(parse_ratio_pair "$target_size" 'x')"; then
      echo "ERROR: --target-size must be WxH with two positive integers (got '$target_size'). Examples: 1280x720, 1792x1008." >&2
      return 1
    fi
    target_px_w="${pair% *}"
    target_px_h="${pair#* }"
    reduced="$(reduce_ratio "$target_px_w" "$target_px_h")"
    target_rw="${reduced% *}"
    target_rh="${reduced#* }"
    target_label="${target_px_w}x${target_px_h} (${target_rw}:${target_rh})"
    target_active=1
  fi
  if [ -n "$target_active" ]; then
    if ! check_image_tools; then return 2; fi
    # No size is picked for the caller here, unlike generate. On generate the
    # requested --size decides the delivered pixels, so choosing it well is
    # what makes a target reachable. On edits all four measured runs passed no
    # --size and got back a size in no enum, matching the INPUT's ratio at a
    # near-constant ~1.57 MP (1672x941 from three 16:9 inputs, 1254x1254 from a
    # 1:1 one). Whether --size is even honoured here is untested, so picking
    # one on the caller's behalf would be acting on a guess. The crop still
    # happens; it just works from whatever comes back.
    echo "NOTE: the delivered file will be measured and centre-cropped to $target_label." >&2
    echo "  No --size is chosen for you on this endpoint: the four measured edits each returned a size matching the INPUT image's aspect ratio at a near-constant ~1.57 megapixels (854x480, 320x180 and 1792x1008 all gave 1672x941; 256x256 gave 1254x1254), and whether --size is honoured here has not been established. So the delivered ratio follows your input, not your target — the crop works from the real file either way, and will fail loudly rather than hand back the wrong ratio if your input's shape cannot cover $target_label." >&2
  fi

  # --out-dir before the network call, same as generate.
  local out_dir_input="$out_dir"
  mkdir -p "$out_dir" 2>/dev/null
  out_dir=$(cd "$out_dir" 2>/dev/null && pwd)
  if [ -z "$out_dir" ]; then
    echo "ERROR: --out-dir '$out_dir_input' could not be created or entered (bad path or missing permissions)." >&2
    return 4
  fi

  if [ -z "$dry_run" ]; then
    if ! check_api_key; then return 2; fi
  fi

  # --- assemble the multipart form ---
  #
  # curl argument pairs, built once and used by both --dry-run (to print) and
  # the real call (to send). Two spellings matter here and are not
  # interchangeable:
  #   -F "image=@PATH"        attach the file at PATH as an upload
  #   -F "image_url=<PATH"    read the FIELD VALUE out of PATH
  # The second is what keeps a data: URI off the command line. A base64 data
  # URI of any real photo runs past this machine's ARG_MAX (1,048,576 bytes)
  # and dies with "Argument list too long" before a single byte is sent — the
  # exact failure ofox-video.sh's frame_images build already had to fix.
  #
  # Which is also why every field whose value this script sets LITERALLY uses
  # `--form-string`, not `-F`. Those two prefixes are not opt-in: curl applies
  # them to any -F value, including one that arrived as free text. `--prompt`
  # is free text, and a prompt may legitimately open with '@' ("@golden hour,
  # ...") or '<'. Measured 2026-09-18 against a local listener, curl 8.7.1:
  # `-F "prompt=@secret.txt"` sent that file's contents as the prompt field,
  # with `filename="secret.txt"` in the part header; pointed at a file that
  # does not exist it aborts with exit 26 before connecting. `--form-string`
  # takes the value verbatim, whatever it starts with.
  #
  # `--extra-form` keeps plain `-F` on purpose: its values are screened above,
  # and moving it to --form-string would make that screen unfalsifiable while
  # quietly re-opening the '@path' spelling this version refuses (ADR D1).
  local -a form=()
  local url_file=""
  if [ -n "$image" ]; then
    form+=(-F "image=@$image")
  else
    url_file="$(mktemp "${TMPDIR:-/tmp}/ofox-edit-url.XXXXXX")" || url_file=""
    if [ -z "$url_file" ]; then
      echo "ERROR: could not create a temp file to hold --image-url." >&2
      return 4
    fi
    printf '%s' "$image_url" >"$url_file"
    form+=(-F "image_url=<$url_file")
  fi
  form+=(--form-string "model=$model")
  form+=(--form-string "prompt=$prompt")
  [ -n "$quality" ] && form+=(--form-string "quality=$quality")
  [ -n "$size" ] && form+=(--form-string "size=$size")
  [ -n "$n" ] && form+=(--form-string "n=$n")
  [ -n "$output_format" ] && form+=(--form-string "output_format=$output_format")
  [ -n "$background" ] && form+=(--form-string "background=$background")
  for form_item in ${extra_form+"${extra_form[@]}"}; do
    form+=(-F "$form_item")
  done

  # Measure the input so the estimate can say whether the anchor's input size
  # matches this request's. Best-effort: a missing ffprobe must not block an
  # edit, since no target was asked for (CONTRIBUTING rule 6, fail open).
  local input_measured=""
  if [ -n "$image" ]; then
    input_measured="$(measure_image_file "$image")" || input_measured=""
  fi

  print_edit_estimate "$model" "${n:-1}" "$quality" "$input_measured"

  if [ -n "$dry_run" ]; then
    [ -n "$url_file" ] && rm -f "$url_file"
    echo "DRY RUN — nothing was submitted and nothing was billed." >&2
    echo "Re-run without --dry-run to edit." >&2
    echo "STATUS dry_run"
    echo "MODEL $model"
    echo "ENDPOINT $EDITS_ENDPOINT"
    if [ -n "$image" ]; then
      echo "INPUT_IMAGE $image"
      [ -n "$input_measured" ] && echo "INPUT_SIZE_ACTUAL $input_measured"
    else
      echo "INPUT_IMAGE_URL_BYTES ${#image_url}"
    fi
    [ -n "$quality" ] && echo "QUALITY $quality"
    [ -n "$size" ] && echo "SIZE $size"
    echo "N ${n:-1}"
    if [ -n "$target_active" ]; then
      echo "TARGET_ASPECT ${target_rw}:${target_rh}"
      [ -n "$target_px_w" ] && echo "TARGET_SIZE ${target_px_w}x${target_px_h}"
    fi
    # The multipart field list, the edits equivalent of generate's payload.
    # Names only — never the values, because --extra-form is a passthrough and
    # this line must not become somewhere a secret can be printed. The uploaded
    # file's path is shown above as INPUT_IMAGE and its bytes are never echoed.
    local f names=""
    for f in "${form[@]}"; do
      case "$f" in
        -F|--form-string) continue ;;
      esac
      names="$names ${f%%=*}"
    done
    echo "FORM_FIELDS${names}"
    if [ -n "$MODEL_FALLBACK_FROM" ]; then
      echo "MODEL_FALLBACK_FROM $MODEL_FALLBACK_FROM"
      echo "MODEL_FALLBACK_REASON $MODEL_FALLBACK_REASON"
      echo "MODEL_PRICE_DELTA $MODEL_PRICE_DELTA"
    fi
    [ -n "$MODEL_CHAIN_EXHAUSTED" ] && echo "MODEL_CHAIN_EXHAUSTED $MODEL_CHAIN_EXHAUSTED"
    return 0
  fi

  # --- the one and only network call ---

  echo "Requesting image edit from Ofox (model=$model)..." >&2
  local tmp_body http_code curl_rc body
  tmp_body=$(mktemp)
  http_code=$(curl -sS -o "$tmp_body" -w '%{http_code}' \
    --connect-timeout "$CONNECT_TIMEOUT" --max-time "$GENERATE_MAX_TIME" \
    -X POST "$API_BASE/images/edits" \
    -H "Authorization: Bearer $OFOX_API_KEY" \
    "${form[@]}")
  curl_rc=$?
  body=$(cat "$tmp_body")
  rm -f "$tmp_body"
  [ -n "$url_file" ] && rm -f "$url_file"

  if [ "$curl_rc" -ne 0 ]; then
    echo "ERROR: could not reach the Ofox API (curl exit $curl_rc) — no HTTP response was received at all." >&2
    echo "This is a synchronous, no-job-id endpoint: there is no poll/dashboard job entry to check by id." >&2
    echo "Check your usage/billing history at ${GET_KEY_URL} before deciding whether to retry." >&2
    return 5
  fi

  if [ "$http_code" != "200" ]; then
    print_api_error "edit" "$http_code" "$body"
    return 3
  fi

  # --- decode and save ---

  local count
  count=$(printf '%s' "$body" | jq -r '.data | length' 2>/dev/null)
  if [ -z "$count" ] || [ "$count" = "null" ] || ! [ "$count" -gt 0 ] 2>/dev/null; then
    echo "ERROR: got HTTP 200 but the response has no usable data[] entries — unexpected response shape." >&2
    echo "Raw response body:" >&2
    printf '%s\n' "$body" >&2
    return 3
  fi

  # The edits response DOES carry output_format (generations' does not), so
  # prefer what the API says it wrote over what we asked for, and fall back to
  # the request only when the field is absent.
  local resp_format ext base_name
  resp_format=$(printf '%s' "$body" | jq -r '.output_format // empty' 2>/dev/null)
  ext=$(infer_extension "${resp_format:-$output_format}")
  base_name="${out_name:-ofox_edit_$(date +%Y%m%d%H%M%S)_$$}"

  local idx=0 item b64 stem outpath rawpath paths=() raw_paths=()
  local measured_size="" final_size="" crop_dims
  while IFS= read -r item; do
    b64=$(printf '%s' "$item" | jq -r '.b64_json // empty')
    if [ -z "$b64" ]; then
      echo "ERROR: data[$idx] has no b64_json field — unexpected response shape." >&2
      echo "Raw response body:" >&2
      printf '%s\n' "$body" >&2
      return 3
    fi
    if [ "$count" -gt 1 ]; then
      stem="${out_dir%/}/${base_name}_${idx}"
    else
      stem="${out_dir%/}/${base_name}"
    fi
    if [ -n "$target_active" ]; then
      rawpath="${stem}-uncropped.${ext}"
      outpath="${stem}.${ext}"
    else
      rawpath="${stem}.${ext}"
      outpath="$rawpath"
    fi
    if ! decode_b64_to_file "$b64" "$rawpath"; then
      echo "ERROR: failed to base64-decode image data[$idx] to $rawpath." >&2
      return 3
    fi
    raw_paths+=("$rawpath")

    local this_measured=""
    this_measured="$(measure_image_file "$rawpath")" || this_measured=""
    [ "$idx" -eq 0 ] && measured_size="$this_measured"

    if [ -n "$target_active" ]; then
      if [ -z "$this_measured" ]; then
        echo "ERROR: could not measure '$rawpath', so the target ${target_rw}:${target_rh} cannot be guaranteed." >&2
        echo "The edited image is on disk and was billed; it is NOT cropped and its ratio is unverified." >&2
        return 3
      fi
      local mw="${this_measured%x*}" mh="${this_measured#*x}"
      if ! crop_dims="$(crop_dims_for "$mw" "$mh" "$target_rw" "$target_rh")"; then
        echo "ERROR: '$rawpath' measured ${this_measured}, too small to hold one whole unit of ${target_rw}:${target_rh}." >&2
        echo "The edit was performed and billed; it is on disk uncropped. Nothing wrong-ratio was written to ${outpath}." >&2
        return 3
      fi
      local cw="${crop_dims% *}" ch="${crop_dims#* }"
      if [ -n "$target_px_w" ] &&
        { [ "$cw" -lt "$target_px_w" ] || [ "$ch" -lt "$target_px_h" ]; }; then
        echo "ERROR: '$rawpath' measured ${this_measured}; cropped to ${target_rw}:${target_rh} that is only ${cw}x${ch}, short of the requested ${target_px_w}x${target_px_h}." >&2
        echo "This script crops and scales down, never up. The edit was performed and billed and is on disk at the -uncropped path." >&2
        return 3
      fi
      if ! crop_image_to "$rawpath" "$outpath" "$cw" "$ch" "$target_px_w" "$target_px_h"; then
        echo "ERROR: ffmpeg could not crop '$rawpath' to ${cw}x${ch}." >&2
        echo "The edit was performed and billed and is on disk uncropped at that path." >&2
        return 3
      fi
      if [ "$idx" -eq 0 ]; then
        if [ -n "$target_px_w" ]; then
          final_size="${target_px_w}x${target_px_h}"
        else
          final_size="${cw}x${ch}"
        fi
      fi
    fi
    paths+=("$outpath")
    idx=$((idx + 1))
  done < <(printf '%s' "$body" | jq -c '.data[]')

  local resp_model resp_size resp_quality
  local input_tokens output_tokens total_tokens in_image_tokens in_text_tokens
  resolve_response_model "$model" "$body"
  resp_model="$RESPONSE_MODEL"
  resp_size=$(printf '%s' "$body" | jq -r '.size // "unknown"')
  resp_quality=$(printf '%s' "$body" | jq -r '.quality // "unknown"')
  input_tokens=$(printf '%s' "$body" | jq -r '.usage.input_tokens // "unknown"')
  output_tokens=$(printf '%s' "$body" | jq -r '.usage.output_tokens // "unknown"')
  total_tokens=$(printf '%s' "$body" | jq -r '.usage.total_tokens // "unknown"')
  in_image_tokens=$(printf '%s' "$body" | jq -r '.usage.input_tokens_details.image_tokens // empty')
  in_text_tokens=$(printf '%s' "$body" | jq -r '.usage.input_tokens_details.text_tokens // empty')

  echo "STATUS completed"
  for outpath in "${paths[@]}"; do
    echo "IMAGE_PATH $outpath"
  done
  if [ -n "$target_active" ]; then
    for rawpath in "${raw_paths[@]}"; do
      echo "IMAGE_PATH_UNCROPPED $rawpath"
    done
  fi
  # The source, printed next to the result on purpose: the question that
  # decides whether an edit worked is "how does this compare with the input",
  # and an agent that has to go and find the input is an agent that will
  # answer from STATUS completed instead.
  [ -n "$image" ] && echo "INPUT_IMAGE $image"
  [ -n "$input_measured" ] && echo "INPUT_SIZE_ACTUAL $input_measured"
  echo "MODEL $resp_model"
  echo "MODEL_SOURCE $RESPONSE_MODEL_SOURCE"
  if [ "$resp_model" != "$model" ]; then
    echo "MODEL_REQUESTED $model"
  fi
  echo "SIZE $resp_size"
  if [ -n "$measured_size" ]; then
    echo "SIZE_ACTUAL $measured_size"
    if [ "$measured_size" != "$resp_size" ] && [ "$resp_size" != "unknown" ]; then
      echo "NOTE: the API reported SIZE $resp_size but the file measures $measured_size. The file is the fact; the response field is not." >&2
    fi
  else
    echo "SIZE_ACTUAL unmeasured"
    echo "NOTE: could not measure the written file's real dimensions (ffprobe missing or unreadable file), so SIZE above is unverified. Install ffmpeg to have this checked: brew install ffmpeg / sudo apt-get install ffmpeg." >&2
  fi
  if [ -n "$final_size" ]; then
    echo "SIZE_FINAL $final_size"
    echo "TARGET_ASPECT ${target_rw}:${target_rh}"
  fi
  echo "QUALITY $resp_quality"
  echo "USAGE_INPUT_TOKENS $input_tokens"
  # The line a generation has no equivalent of, and the reason edit_cost_for
  # exists: on the measured run 576 of 608 input tokens were the uploaded
  # picture, billed at a rate the catalog publishes separately.
  [ -n "$in_image_tokens" ] && echo "USAGE_INPUT_IMAGE_TOKENS $in_image_tokens"
  [ -n "$in_text_tokens" ] && echo "USAGE_INPUT_TEXT_TOKENS $in_text_tokens"
  echo "USAGE_OUTPUT_TOKENS $output_tokens"
  echo "USAGE_TOTAL_TOKENS $total_tokens"

  local cost=""
  load_models >/dev/null 2>&1 || true
  cost="$(edit_cost_for "$resp_model" "$input_tokens" "$output_tokens" "$in_image_tokens" "$in_text_tokens")" || cost=""
  if [ -n "$cost" ]; then
    echo "EDIT_COST $cost"
    echo "NOTE: EDIT_COST is the DEARER of two readings of the same token counts — every input token at the prompt rate, versus the prompt's text at that rate and the uploaded image at the catalog's separate pricing.image rate. They were 13% apart on the measured run and no invoice has settled which is right, so this errs high by rule. See references/pricing.md." >&2
  else
    echo "NOTE: could not compute a cost — no published rates available for" >&2
    echo "'$resp_model' (offline, or the model is missing from the list)." >&2
    echo "The token counts above are exact; see references/pricing.md for the" >&2
    echo "formula to apply by hand." >&2
  fi

  # An edit that ran is not an edit that edited. The endpoint could in
  # principle have ignored the upload and rendered the prompt, and STATUS
  # completed cannot tell those apart — only the artifact can.
  echo "NOTE: verify the result against the input before delivering it. Open both and check that what you did NOT ask to change is unchanged; a job that completes proves the request was accepted, not that the image was edited rather than redrawn." >&2
  return 0
}

# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------

main() {
  local mode="${1:-}"
  # Every subcommand here builds its requests from API_BASE, so the base is
  # validated (and an override announced) before any of them runs. The list is
  # written out rather than applied unconditionally so that adding a local,
  # offline subcommand later is a deliberate decision about this guard too —
  # the sibling ofox-video.sh has four such commands and they are excluded.
  case "$mode" in
    check|models|generate|edit)
      validate_api_base || return 2
      ;;
  esac
  case "$mode" in
    check)
      cmd_check
      return $?
      ;;
    models)
      shift
      cmd_models "$@"
      return $?
      ;;
    generate)
      shift
      cmd_generate "$@"
      return $?
      ;;
    edit)
      shift
      cmd_edit "$@"
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
