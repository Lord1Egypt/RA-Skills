#!/usr/bin/env bash
# Run the target-host latency measurements and print a summary.
#
# Covers tasks 1.5 (baseline) and 1.7 (grace-window sweep). Tasks 1.6 and 6.3
# are deliberately absent: 1.6 needs wall-clock marks only a human can take, and
# 6.3 needs a real authenticated session.
#
# This arms real Cloudflare Quick Tunnels. It refuses to run against an
# authenticated profile -- see the check below, which is the reason this is a
# script and not a copy-paste loop.
set -uo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/session.sh
source "$script_dir/lib/session.sh"

runs=3
grace_values=""
out_file=""
cdp_url_default="http://127.0.0.1:9222"

usage() {
  cat <<'EOF'
Usage: measure_handoff.sh [options]

  --baseline N          Baseline runs at the current default grace (default: 3)
  --grace-sweep "A B C" Sweep these grace values, --repeats each
  --repeats N           Runs per grace value (default: 3)
  --out FILE            Also write the summary here (e.g. baseline.md)
  -h, --help            Show this help

Examples:
  scripts/measure_handoff.sh --baseline 3
  scripts/measure_handoff.sh --grace-sweep "5 8 12 16 20" --repeats 3
  scripts/measure_handoff.sh --baseline 3 --grace-sweep "5 8 12 16 20" \
    --out openspec/changes/speed-up-login-handoff/baseline.md

Every run arms a real tunnel. Run this BEFORE logging LINE in: the measurements
do not need a session, and this refuses to run once one is authenticated.
EOF
}

repeats=3
do_baseline=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --baseline) do_baseline=1; runs="${2:-3}"; shift 2 ;;
    --grace-sweep) grace_values="${2:-}"; shift 2 ;;
    --repeats) repeats="${2:-3}"; shift 2 ;;
    --out) out_file="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) printf 'ERROR: unknown argument: %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
done
[[ "$do_baseline" == 1 || -n "$grace_values" ]] || { do_baseline=1; }

command -v cloudflared >/dev/null 2>&1 || {
  printf 'ERROR: cloudflared is required. Run scripts/doctor.sh for install instructions.\n' >&2
  exit 2
}

# --- The reason this is a script -------------------------------------------
# The runbook says to measure before logging in, because a grace sweep arms a
# handoff a dozen or more times and each arm exposes the browser. Against an
# authenticated profile that is a dozen exposures of a live LINE OA back office.
# A sentence in a document does not enforce that; this does.
if session_looks_authenticated; then
  cat >&2 <<'EOF'
ERROR: this session looks authenticated to LINE.

  Measuring arms a real tunnel on every run, and a grace sweep does so a dozen
  times or more. Each arm exposes the browser to whoever holds the URL, so
  running this against a logged-in profile means repeatedly exposing a live
  LINE OA back office.

  None of these measurements need a session: every phase is Chromium loading
  the login page. Measure first, log in afterwards.

  If you must re-measure on an authenticated host, stop the session, move the
  profile aside, and measure against a fresh one.
EOF
  exit 2
fi

# A session that this script did not start breaks the measurement quietly rather
# than loudly: start_line_oa_chromium.sh refuses when one is already live, and
# the baseline loop would then read the *previous* run's phase log and present it
# as this run's result. Refuse instead of reporting stale numbers.
if session_is_live || curl --max-time 3 -fsS "${cdp_url_default}/json/version" >/dev/null 2>&1; then
  cat >&2 <<'EOF'
ERROR: a browser session is already running.

  This script starts and stops its own sessions so each run is measured from a
  cold start. With one already up, the session it tries to start is refused and
  the timings would be read from the previous run's log -- wrong numbers that
  look plausible.

  Stop it first:
    bash scripts/stop_line_oa_chromium.sh
EOF
  exit 2
fi

runtime_dir="$(session_runtime_dir)"
report="$(mktemp)"
emit() { printf '%s\n' "$*" | tee -a "$report"; }

# Pull the elapsed seconds for a named phase out of a phase log.
# The log is column-aligned, so "elapsed=" and its value can be separate fields;
# match the whole line rather than depending on field positions.
phase_value() {
  [[ -f "${2:-}" ]] || return 0
  awk -v want="$1" '
    $1==want {
      if (match($0, /elapsed=[[:space:]]*[0-9.]+/)) {
        s = substr($0, RSTART, RLENGTH)
        gsub(/elapsed=[[:space:]]*/, "", s)
        print s
      }
    }' "$2" | head -1
}

# Time since the previous phase. For dns_resolved this is exactly the grace
# window plus however long the lookup itself took, which is what the sweep needs
# -- elapsed-from-entry also carries the tunnel registration time and would make
# every grace value look like a miss.
phase_delta() {
  [[ -f "${2:-}" ]] || return 0
  awk -v want="$1" '
    $1==want {
      if (match($0, /delta=[[:space:]]*[0-9.]+/)) {
        s = substr($0, RSTART, RLENGTH)
        gsub(/delta=[[:space:]]*/, "", s)
        print s
      }
    }' "$2" | head -1
}
newest_log() { ls -1t "$runtime_dir"/timing/"$1"-*.log 2>/dev/null | head -1; }

stats() {  # min / mean / max from stdin
  awk 'NF{v[n++]=$1; s+=$1; if(min==""||$1<min)min=$1; if($1>max)max=$1}
       END{ if(n==0){print "n/a"; exit} printf "%.2f / %.2f / %.2f", min, s/n, max }'
}

teardown() {
  bash "$script_dir/stop_line_oa_vnc_handoff.sh" --quiet >/dev/null 2>&1 || true
  bash "$script_dir/stop_line_oa_chromium.sh" >/dev/null 2>&1 || true
}
trap teardown EXIT INT TERM

emit "# Handoff measurements"
emit ""
emit "Host: \`$(uname -m)\` $( . /etc/os-release 2>/dev/null && printf '%s' "$PRETTY_NAME" || printf 'unknown' )"
emit "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
emit ""

# ---------------------------------------------------------------- baseline ---
if (( do_baseline )); then
  emit "## Baseline (task 1.5) — ${runs} runs at the current default grace"
  emit ""
  emit '| run | session total | tunnel_url | dns_resolved | url_verified | handoff total |'
  emit '| --- | --- | --- | --- | --- | --- |'
  s_tot=(); h_url=(); h_dns=(); h_ver=(); h_tot=()
  for i in $(seq 1 "$runs"); do
    bash "$script_dir/start_line_oa_chromium.sh" >/dev/null 2>&1
    slog="$(newest_log session)"
    st="$(phase_value session_recorded "$slog")"

    LINE_OA_SEND_CHAT_HANDOFF_PURPOSE=line-login \
      bash "$script_dir/start_line_oa_vnc_handoff.sh" >/dev/null 2>&1
    hlog="$(newest_log handoff)"
    tu="$(phase_value tunnel_url "$hlog")"
    dr="$(phase_value dns_resolved "$hlog")"
    uv="$(phase_value url_verified "$hlog")"
    ht="$(phase_value ttl_scheduled "$hlog")"
    [[ -n "$uv" ]] || { tu="${tu:-—}"; dr="${dr:-—}"; uv="FAILED"; ht="—"; }

    emit "| $i | ${st:-—}s | ${tu:-—}s | ${dr:-—}s | ${uv}${uv:+s} | ${ht:-—}s |"
    [[ -n "$st" ]] && s_tot+=("$st"); [[ -n "$tu" && "$tu" != "—" ]] && h_url+=("$tu")
    [[ -n "$dr" && "$dr" != "—" ]] && h_dns+=("$dr")
    [[ "$uv" != "FAILED" ]] && { h_ver+=("$uv"); h_tot+=("$ht"); }

    bash "$script_dir/stop_line_oa_vnc_handoff.sh" --quiet >/dev/null 2>&1
    bash "$script_dir/stop_line_oa_chromium.sh" >/dev/null 2>&1
    sleep 3
  done
  emit ""
  emit '| metric | min / mean / max |'
  emit '| --- | --- |'
  emit "| session total | $(printf '%s\n' "${s_tot[@]:-}" | stats) s |"
  emit "| tunnel_url | $(printf '%s\n' "${h_url[@]:-}" | stats) s |"
  emit "| dns_resolved | $(printf '%s\n' "${h_dns[@]:-}" | stats) s |"
  emit "| url_verified | $(printf '%s\n' "${h_ver[@]:-}" | stats) s |"
  emit "| handoff total | $(printf '%s\n' "${h_tot[@]:-}" | stats) s |"
  emit ""
fi

# -------------------------------------------------------------- grace sweep ---
if [[ -n "$grace_values" ]]; then
  emit "## Grace-window sweep (task 1.7) — ${repeats} runs per value"
  emit ""
  emit 'Read-off: `lookup wait` is the time from the tunnel URL being emitted to'
  emit 'the hostname resolving — the grace window plus the lookup itself. When it'
  emit 'is within ~1.5s of the grace value the first lookup hit. Meaningfully'
  emit 'larger means the first lookup missed and backoff recovered it, which is'
  emit 'already refreshing the negative cache. Pick the smallest value that hits'
  emit 'on every run.'
  emit ""
  emit '| grace | run | lookup wait | over grace | first-lookup hit? | url_verified |'
  emit '| --- | --- | --- | --- | --- | --- |'
  bash "$script_dir/start_line_oa_chromium.sh" >/dev/null 2>&1
  best=""
  for g in $grace_values; do
    all_hit=1
    for i in $(seq 1 "$repeats"); do
      LINE_OA_SEND_CHAT_HANDOFF_PURPOSE=line-login \
      LINE_OA_SEND_CHAT_HANDOFF_VERIFY_GRACE="$g" \
        bash "$script_dir/start_line_oa_vnc_handoff.sh" >/dev/null 2>&1
      hlog="$(newest_log handoff)"
      wait_s="$(phase_delta dns_resolved "$hlog")"
      uv="$(phase_value url_verified "$hlog")"
      if [[ -z "$wait_s" ]]; then
        hit="FAILED"; all_hit=0; wait_s="—"; over="—"
      else
        over="$(awk -v w="$wait_s" -v g="$g" 'BEGIN{printf "%+.2f", w-g}')"
        if awk -v w="$wait_s" -v g="$g" 'BEGIN{exit !(w <= g+1.5)}'; then
          hit="yes"
        else
          hit="no (backoff)"; all_hit=0
        fi
      fi
      emit "| ${g}s | $i | ${wait_s}${wait_s:+s} | ${over}s | $hit | ${uv:-—}${uv:+s} |"
      bash "$script_dir/stop_line_oa_vnc_handoff.sh" --quiet >/dev/null 2>&1
      sleep 5
    done
    (( all_hit )) && [[ -z "$best" ]] && best="$g"
  done
  bash "$script_dir/stop_line_oa_chromium.sh" >/dev/null 2>&1
  emit ""
  if [[ -n "$best" ]]; then
    emit "**Smallest grace with a first-lookup hit on every run: ${best}s.**"
    emit ""
    emit "Apply it as the default in \`scripts/start_line_oa_vnc_handoff.sh\`:"
    emit ''
    emit '```bash'
    emit "verify_grace=\"\${LINE_OA_SEND_CHAT_HANDOFF_VERIFY_GRACE:-${best}}\""
    emit '```'
  else
    emit "**No swept value hit on every run.** Keep the current default and"
    emit "consider sweeping higher values."
  fi
  emit ""
fi

emit "## Still manual"
emit ""
emit "- **Task 1.6** — agent-turn cost. Note the wall clock when you ask for a"
emit "  handoff (\`T0\`), the \`# started=\` line in the newest \`handoff-*.log\`"
emit "  (\`T1\`), and when the noVNC canvas becomes operable (\`T2\`)."
emit "- **Task 6.3** — send after revocation. Needs a real authenticated session,"
emit "  so run it after logging in."
emit ""
emit "Raw phase logs: \`$runtime_dir/timing/\`"

if [[ -n "$out_file" ]]; then
  cp "$report" "$out_file"
  printf '\nWritten to %s\n' "$out_file"
fi
rm -f "$report"
