#!/usr/bin/env bash
set -euo pipefail

API_URL="${PRISMFY_API_URL:-https://api.prismfy.io/v1/search}"
API_URL="${API_URL%/}"
API_ROOT="${PRISMFY_API_ROOT:-}"
API_ROOT="${API_ROOT%/}"
ME_URL="${PRISMFY_ME_URL:-}"
ME_URL="${ME_URL%/}"
SKILL_VERSION="1.0.0"

die() { echo "ERROR: $*" >&2; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || die "missing dependency: $1"; }

need curl
need jq

company=""
domain=""
person=""
person_company=""
role=""
geo=""
icp=""
query_family="all"
quota=0
raw=0
engine=""
engines=""
out_file=""

usage() {
  cat <<'EOF'
Lead Enrichment helper

Usage:
  lead-enrich.sh --company "Company" [--query-family identity|core|fit|activity|disqualifier|contact|all]
  lead-enrich.sh --person "Person" [--company "Company"] [--role "Title"] [--query-family all]
  lead-enrich.sh --domain example.com [--query-family core]
  lead-enrich.sh --quota

Options:
  --company NAME
  --domain DOMAIN
  --person NAME
  --person-company NAME
  --role TITLE
  --geo GEO
  --icp TEXT
  --query-family NAME
  --engine NAME
  --engines CSV
  --out FILE
  --raw
  --quota

Notes:
  - This helper produces a conservative preliminary enrichment verdict.
  - It normalizes public-web evidence and favors ambiguity over false certainty.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --company) shift; company="${1:-}" ;;
    --domain) shift; domain="${1:-}" ;;
    --person) shift; person="${1:-}" ;;
    --person-company) shift; person_company="${1:-}" ;;
    --role) shift; role="${1:-}" ;;
    --geo) shift; geo="${1:-}" ;;
    --icp) shift; icp="${1:-}" ;;
    --query-family) shift; query_family="${1:-all}" ;;
    --engine) shift; engine="${1:-}" ;;
    --engines) shift; engines="${1:-}" ;;
    --out) shift; out_file="${1:-}" ;;
    --raw) raw=1 ;;
    --quota) quota=1 ;;
    --help|-h) usage; exit 0 ;;
    *) die "unknown arg: $1" ;;
  esac
  shift
done

if [[ "$quota" -eq 1 ]]; then
  [[ -n "${PRISMFY_API_KEY:-}" ]] || die "PRISMFY_API_KEY is not set"
  if [[ -z "$ME_URL" ]]; then
    if [[ -n "$API_ROOT" ]]; then
      ME_URL="${API_ROOT}/user/me"
    elif [[ "$API_URL" == */search ]]; then
      ME_URL="${API_URL%/search}/user/me"
    else
      die "cannot derive quota endpoint from PRISMFY_API_URL; set PRISMFY_API_ROOT or PRISMFY_ME_URL"
    fi
  fi
  curl -fsS -H "Authorization: Bearer $PRISMFY_API_KEY" "$ME_URL"
  exit 0
fi

[[ -n "${PRISMFY_API_KEY:-}" ]] || die "PRISMFY_API_KEY is not set"
[[ -n "$company" || -n "$domain" || -n "$person" ]] || { usage; die "provide --company, --domain, or --person"; }

tmp_queries="$(mktemp)"
tmp_runs="$(mktemp)"
tmp_report="$(mktemp)"
trap 'rm -f "$tmp_queries" "$tmp_runs" "$tmp_report"' EXIT
printf '' > "$tmp_queries"
echo "[]" > "$tmp_runs"

target_company="${company:-$person_company}"
target_domain="$domain"

add_query() {
  local family="$1"
  local hypothesis="$2"
  local text="$3"
  [[ -n "$text" ]] || return 0
  jq -cn --arg family "$family" --arg hypothesis "$hypothesis" --arg text "$text" \
    '{family:$family,hypothesis:$hypothesis,query:$text}' >> "$tmp_queries"
  printf '\n' >> "$tmp_queries"
}

build_identity_queries() {
  if [[ -n "$company" ]]; then
    add_query identity support "\"$company\" official site"
    add_query identity support "\"$company\" about"
    add_query identity support "\"$company\" company"
  fi
  if [[ -n "$domain" ]]; then
    add_query identity support "\"$domain\" company"
    add_query identity support "site:$domain about"
    add_query identity support "site:$domain company"
  fi
  if [[ -n "$person" ]]; then
    local co="${person_company:-$company}"
    if [[ -n "$co" ]]; then
      add_query identity support "\"$person\" \"$co\""
      add_query identity support "\"$person\" \"$co\" ${role:-role}"
    else
      add_query identity support "\"$person\" role"
      add_query identity support "\"$person\" bio"
    fi
  fi
}

build_core_queries() {
  if [[ -n "$domain" ]]; then
    add_query core support "site:$domain about"
    add_query core support "site:$domain product"
    add_query core support "site:$domain solutions"
    add_query core support "site:$domain pricing"
    add_query core support "site:$domain docs OR help"
  elif [[ -n "$company" ]]; then
    add_query core support "\"$company\" product"
    add_query core support "\"$company\" pricing"
    add_query core support "\"$company\" customers"
    add_query core support "\"$company\" docs"
  fi
  if [[ -n "$person" ]]; then
    local co="${person_company:-$company}"
    if [[ -n "$co" ]]; then
      add_query core support "\"$person\" \"$co\" title"
      add_query core support "\"$person\" \"$co\" team"
      add_query core support "\"$person\" \"$co\" leadership"
    else
      add_query core support "\"$person\" title"
      add_query core support "\"$person\" bio"
      add_query core support "\"$person\" speaker"
    fi
  fi
}

build_fit_queries() {
  local target="${company:-$domain}"
  if [[ -n "$target" ]]; then
    [[ -n "$icp" ]] && add_query fit support "\"$target\" \"$icp\""
    [[ -n "$domain" && -n "$icp" ]] && add_query fit support "site:$domain \"$icp\""
    add_query fit support "\"$target\" customers"
    add_query fit support "\"$target\" integrations"
    add_query fit support "\"$target\" use cases"
    add_query fit support "\"$target\" b2b saas"
    add_query fit support "\"$target\" developer"
    add_query fit falsify "\"$target\" agency"
    add_query fit falsify "\"$target\" consultant"
    add_query fit falsify "\"$target\" freelancer"
    add_query fit falsify "\"$target\" consumer"
    add_query fit falsify "\"$target\" student"
    add_query fit falsify "\"$target\" hobby"
  fi
  if [[ -n "$person" ]]; then
    local co="${person_company:-$company}"
    if [[ -n "$co" ]]; then
      add_query fit support "\"$person\" \"$co\" ${role:-role}"
      [[ -n "$icp" ]] && add_query fit support "\"$person\" \"$co\" \"$icp\""
      add_query fit falsify "\"$person\" former \"$co\""
      add_query fit falsify "\"$person\" advisor \"$co\""
      add_query fit falsify "\"$person\" intern \"$co\""
      add_query fit falsify "\"$person\" student"
    else
      add_query fit support "\"$person\" ${role:-role}"
      [[ -n "$icp" ]] && add_query fit support "\"$person\" \"$icp\""
      add_query fit falsify "\"$person\" student"
      add_query fit falsify "\"$person\" intern"
    fi
  fi
}

build_activity_queries() {
  local target="${company:-$domain}"
  [[ -n "$domain" ]] && {
    add_query activity support "site:$domain blog"
    add_query activity support "site:$domain news"
    add_query activity support "site:$domain changelog"
    add_query activity support "site:$domain careers"
  }
  [[ -n "$target" ]] && {
    add_query activity support "\"$target\" hiring"
    add_query activity support "\"$target\" announcement"
    add_query activity support "\"$target\" funding"
    add_query activity support "\"$target\" recent"
  }
  if [[ -n "$person" ]]; then
    local co="${person_company:-$company}"
    if [[ -n "$co" ]]; then
      add_query activity support "\"$person\" \"$co\" interview"
      add_query activity support "\"$person\" \"$co\" webinar"
    else
      add_query activity support "\"$person\" interview"
      add_query activity support "\"$person\" webinar"
    fi
  fi
}

build_disqualifier_queries() {
  local target="${company:-$domain}"
  [[ -n "$target" ]] && {
    add_query disqualifier falsify "\"$target\" shutdown"
    add_query disqualifier falsify "\"$target\" inactive"
    add_query disqualifier falsify "\"$target\" acquired"
  }
  if [[ -n "$person" ]]; then
    local co="${person_company:-$company}"
    if [[ -n "$co" ]]; then
      add_query disqualifier falsify "\"$person\" former \"$co\""
      add_query disqualifier falsify "\"$person\" ex-\"$co\""
    fi
    add_query disqualifier falsify "\"$person\" student"
    add_query disqualifier falsify "\"$person\" intern"
  fi
}

build_contact_queries() {
  if [[ -n "$domain" ]]; then
    add_query contact support "site:$domain contact"
    add_query contact support "site:$domain team"
    add_query contact support "site:$domain about"
    add_query contact support "site:$domain press"
  elif [[ -n "$company" ]]; then
    add_query contact support "\"$company\" contact"
    add_query contact support "\"$company\" team"
    add_query contact support "\"$company\" about"
    add_query contact support "\"$company\" press"
  fi
  if [[ -n "$person" ]]; then
    local co="${person_company:-$company}"
    if [[ -n "$co" ]]; then
      add_query contact support "\"$person\" \"$co\" contact"
      add_query contact support "\"$person\" \"$co\" team"
      add_query contact support "\"$person\" \"$co\" author"
    else
      add_query contact support "\"$person\" contact"
      add_query contact support "\"$person\" author"
      add_query contact support "\"$person\" email"
    fi
  fi
}

case "$query_family" in
  identity) build_identity_queries ;;
  core) build_core_queries ;;
  fit) build_fit_queries ;;
  activity) build_activity_queries ;;
  disqualifier) build_disqualifier_queries ;;
  contact) build_contact_queries ;;
  all)
    build_identity_queries
    build_core_queries
    build_fit_queries
    build_activity_queries
    build_disqualifier_queries
    ;;
  *) die "unsupported query family: $query_family" ;;
esac

mapfile -t query_lines < <(jq -cs 'unique_by(.query) | .[]' "$tmp_queries")
[[ "${#query_lines[@]}" -gt 0 ]] || die "no queries generated"

api_search() {
  local query="$1"
  local payload
  payload="$(jq -n \
    --arg q "$query" \
    --arg engine "$engine" \
    --arg engines "$engines" \
    --arg geo "$geo" \
    '{
      query: $q
    }
    + (if $engine != "" then {engine: $engine} else {} end)
    + (if $engines != "" then {engines: ($engines | split(","))} else {} end)
    + (if $geo != "" then {geo: $geo} else {} end)')"

  local attempt=0
  local max_attempts=2
  local response
  local err
  while (( attempt < max_attempts )); do
    attempt=$((attempt + 1))
    err="$(mktemp)"
    if response="$(curl -m 20 -fsS "$API_URL" \
      -H "Authorization: Bearer $PRISMFY_API_KEY" \
      -H "Content-Type: application/json" \
      -d "$payload" 2>"$err")"; then
      rm -f "$err"
      printf '%s' "$response"
      return 0
    fi
    local msg
    msg="$(cat "$err" 2>/dev/null || true)"
    rm -f "$err"
    if (( attempt >= max_attempts )); then
      printf '%s' "$msg"
      return 1
    fi
    sleep 1
  done
}

for line in "${query_lines[@]}"; do
  family="$(echo "$line" | jq -r '.family')"
  hypothesis="$(echo "$line" | jq -r '.hypothesis')"
  query="$(echo "$line" | jq -r '.query')"
   if response="$(api_search "$query")"; then
    if printf '%s' "$response" | jq -e 'type == "object" and ((has("results") | not) or (.results | type == "array"))' >/dev/null 2>&1; then
      trimmed_response="$(printf '%s' "$response" | jq -c 'if (.results? | type) == "array" then .results |= .[:5] else . end')"
      jq --arg family "$family" \
         --arg hypothesis "$hypothesis" \
         --arg query "$query" \
         --argjson response "$trimmed_response" \
         '. + [{
           family:$family,
           hypothesis:$hypothesis,
           query:$query,
           status:"ok",
           response:$response
         }]' "$tmp_runs" > "${tmp_runs}.new"
    else
      jq --arg family "$family" \
         --arg hypothesis "$hypothesis" \
         --arg query "$query" \
         --arg error "invalid_response_schema" \
         '. + [{
           family:$family,
           hypothesis:$hypothesis,
           query:$query,
           status:"error",
           error:$error
         }]' "$tmp_runs" > "${tmp_runs}.new"
    fi
  else
    jq --arg family "$family" \
       --arg hypothesis "$hypothesis" \
       --arg query "$query" \
       --arg error "$response" \
       '. + [{
         family:$family,
         hypothesis:$hypothesis,
         query:$query,
         status:"error",
         error:$error
       }]' "$tmp_runs" > "${tmp_runs}.new"
  fi
  mv "${tmp_runs}.new" "$tmp_runs"
done

jq -n \
  --arg timestamp_utc "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
  --arg skill_version "$SKILL_VERSION" \
  --arg company "$company" \
  --arg domain "$domain" \
  --arg person "$person" \
  --arg current_company "${person_company:-$company}" \
  --arg role "$role" \
  --arg icp "$icp" \
  --arg query_family "$query_family" \
  --argjson runs "$(cat "$tmp_runs")" \
  '
  def host_from_url:
    (. // "")
    | sub("^https?://";"")
    | split("/")[0]
    | sub("^www\\."; "");
  def source_type($known_domain):
    if .domain == "" then "unknown"
    elif $known_domain != "" and .domain == $known_domain then "official"
    elif (.domain | test("reddit\\.com$")) then "forum"
    elif (.domain | test("github\\.com$")) then "code"
    elif (.domain | test("news|techcrunch|crunchbase|venturebeat")) then "news"
    else "web"
    end;
  def normalized_text:
    ((.title // "") + " " + (.snippet // "")) | ascii_downcase;
  def stance($known_domain; $icp):
    . as $row
    | ($row | normalized_text) as $t
    | ($icp | ascii_downcase | split(" ") | map(select(length >= 4))) as $icp_terms
    | ($icp_terms | map(select($t | contains(.))) | length) as $icp_hits
    | if $row.family == "disqualifier" or $row.hypothesis == "falsify" then
        if ($t | test("shutdown|inactive|consultant|agency|freelancer|consumer|student|hobby|former|intern|advisor|acquired"))
           and ($t | test("not shutdown|not inactive|not a consultant|not an agency|not a freelancer") | not)
        then "falsify" else "neutral" end
      elif $row.source_type == "official" and $row.family == "activity" and ($t | test("blog|news|changelog|careers|hiring|announcement|funding|release")) then
        "support"
      elif $row.source_type == "official" and $row.family == "core" and ($t | test("product|pricing|docs|customers|solutions|integrations|help")) then
        "support"
      elif $row.source_type == "official" and $row.family == "identity" and ($t | test("about|company|team|leadership|founder|ceo|cto|official")) then
        "support"
      elif $row.source_type == "official" and $row.family == "fit" and ($icp_hits > 0 or ($t | test("customers|integrations|use cases|developer|b2b|saas"))) then
        "support"
      elif $row.family == "activity" and ($t | test("blog|news|changelog|careers|hiring|announcement|funding|release")) then
        "support"
      elif $row.family == "core" and ($t | test("product|pricing|docs|customers|solutions|integrations|help")) then
        "support"
      elif $row.family == "identity" and ($t | test("about|company|team|leadership|founder|ceo|cto|official")) then
        "support"
      elif $row.family == "fit" and ($icp_hits > 0 or ($t | test("customers|integrations|use cases|developer|b2b|saas"))) then
        "support"
      else
        "neutral"
      end;
  def limited_results:
    (.response.results // [])[:5];
  def results_to_evidence($known_domain):
    [ .runs[]
      | select(.status=="ok")
      | .family as $family
      | .hypothesis as $hypothesis
      | .query as $query
      | limited_results[]
      | {
          family: $family,
          hypothesis: $hypothesis,
          query: $query,
          title: (.title // ""),
          url: (.url // ""),
          snippet: (.snippet // ""),
          domain: ((.url // "") | host_from_url)
        }
      | .source_type = (source_type($known_domain))
      | .stance = (stance($known_domain; $icp))
    ]
    | unique_by(.url)
    | map(select(.url != ""));
  def canonical_domain($provided_domain):
    if $provided_domain != "" then $provided_domain
    else
      ([ .runs[]
         | select(.status=="ok" and .family=="identity")
         | limited_results[]
         | select((((.title // "") + " " + (.snippet // "")) | ascii_downcase | test("official|about|company|team|leadership|founder|ceo|cto")))
         | (.url // "" | host_from_url)
         | select(. != "")
         | select(test("reddit\\.com$|github\\.com$|linkedin\\.com$|x\\.com$|twitter\\.com$|youtube\\.com$") | not)
       ] | group_by(.) | map(select(length >= 2)) | sort_by(length) | reverse | .[0][0]) // ""
    end;
  def count_family($evidence; $family):
    ($evidence | map(select(.family==$family and .stance=="support")) | length);
  def count_stance($evidence; $stance):
    ($evidence | map(select(.stance==$stance)) | length);
  def count_source_type($evidence; $source_type):
    ($evidence | map(select(.stance=="support" and .source_type==$source_type)) | length);
  def domains_for($evidence; $family):
    ($evidence | map(select(.family==$family and .stance=="support") | .domain) | unique | map(select(. != "")));
  {
    runs: $runs,
    timestamp_utc: $timestamp_utc,
    skill_version: $skill_version,
    company: $company,
    domain: $domain,
    person: $person,
    current_company: $current_company,
    role: $role,
    icp: $icp,
    query_family: $query_family
  } as $root
  | $root
  | (canonical_domain($domain)) as $canonical_domain
  | (results_to_evidence($canonical_domain)) as $evidence
  | (count_family($evidence; "identity")) as $identity_support_count
  | (count_family($evidence; "core")) as $core_count
  | (count_family($evidence; "fit")) as $fit_count
  | (count_family($evidence; "activity")) as $activity_count
  | ($evidence | map(select(.family=="disqualifier" and .stance=="falsify")) | length) as $disqualifier_count
  | (count_stance($evidence; "support")) as $support_count
  | (count_stance($evidence; "falsify")) as $falsify_count
  | (count_source_type($evidence; "official")) as $official_support_count
  | ($evidence | map(.domain) | unique | map(select(. != ""))) as $domains
  | (($root.runs | map(select(.status=="error")) | length)) as $error_count
  | (($root.runs | length)) as $run_count
  | ($root.runs | map(select(.status=="error") | .error) | join(" | ")) as $error_text
  | (
      if $canonical_domain != "" and $identity_support_count >= 2 then "resolved"
      elif $identity_support_count >= 1 then "partial"
      else "unclear"
      end
    ) as $identity_status
  | (
      if $identity_status == "unclear" then "ambiguous"
      elif $error_count == $run_count then "ambiguous"
      elif $query_family != "all" and ($support_count > 0 or $activity_count > 0) then "weak_fit"
      elif $disqualifier_count >= 2 and $support_count <= 1 then "not_fit"
      elif $falsify_count >= 3 and $support_count <= 1 then "not_fit"
      elif $identity_status == "resolved" and $official_support_count >= 2 and $core_count >= 1 and $fit_count >= 1 and $activity_count >= 1 and $support_count >= 5 and ($domains | length) >= 2 and $falsify_count == 0 and $error_count == 0 then "fit"
      elif $identity_status == "resolved" and $official_support_count >= 1 and $core_count >= 1 and $fit_count >= 1 and $support_count >= 4 and $falsify_count == 0 and $error_count <= 1 then "likely_fit"
      elif $support_count >= 1 or $activity_count >= 1 then "weak_fit"
      else "ambiguous"
      end
    ) as $fit_verdict
  | (
      if ($error_text | test("timed out|timeout|429|rate")) then "RATE_LIMIT_OR_TIMEOUT"
      elif ($error_text | test("invalid_json_response|invalid_response_schema")) then "PRISMFY_INVALID_RESPONSE"
      elif $error_count == $run_count then "PRISMFY_UNAVAILABLE"
      elif $identity_status == "unclear" then "IDENTITY_UNCLEAR"
      elif ($evidence | length) == 0 then "NO_PUBLIC_EVIDENCE"
      else null
      end
    ) as $run_failure_code
  | {
      timestamp_utc: $timestamp_utc,
      skill_version: $skill_version,
      entity: {
        company_name: $company,
        domain: $canonical_domain,
        person_name: $person,
        current_company: $current_company,
        role: $role,
        icp_criteria: $icp
      },
      entity_type:
        (if $person != "" and ($company != "" or $current_company != "") then "person+company"
         elif $person != "" then "person"
         else "company"
         end),
      query_family: $query_family,
      identity_status: $identity_status,
      preliminary_fit_verdict: $fit_verdict,
      summary:
        ("identity=" + $identity_status
         + ", support_urls=" + ($support_count|tostring)
         + ", falsify_urls=" + ($falsify_count|tostring)
         + ", activity_urls=" + ($activity_count|tostring)
         + ", disqualifier_urls=" + ($disqualifier_count|tostring)
         + ", domains=" + (($domains|length)|tostring)),
      signals: [
        (if $canonical_domain != "" then "canonical_domain:" + $canonical_domain else empty end),
        (if $support_count > 0 then "support_evidence:" + ($support_count|tostring) else empty end),
        (if $activity_count > 0 then "activity_evidence:" + ($activity_count|tostring) else empty end)
      ],
      disqualifiers:
        ($evidence
         | map(select(.stance=="falsify")
               | ((.title // .snippet) | tostring))
         | map(select(length > 0))
         | .[:5]),
      ambiguities: [
        (if $identity_status != "resolved" then "identity_not_fully_resolved" else empty end),
        (if $error_count > 0 and $error_count < $run_count then "partial_query_failures" else empty end),
        (if $canonical_domain == "" and $company != "" then "canonical_domain_not_confirmed" else empty end)
      ],
      source_urls: ($evidence | map(.url) | unique | .[:10]),
      evidence: ($evidence | .[:20]),
      query_runs: $root.runs,
      run_failure_code: $run_failure_code
    }' > "$tmp_report"

if [[ -n "$out_file" ]]; then
  cp "$tmp_report" "$out_file"
fi

if [[ "$raw" -eq 1 ]]; then
  cat "$tmp_report"
  exit 0
fi

jq -r '
  .preliminary_fit_verdict as $v |
  .entity as $e |
  [
    (
      if $v == "fit" then "Fit."
      elif $v == "likely_fit" then "Likely fit."
      elif $v == "weak_fit" then "Weak fit."
      elif $v == "not_fit" then "Not fit."
      else "Ambiguous."
      end
    ),
    (
      if .entity.domain != "" then
        "1. Identity: canonical domain = " + .entity.domain
      elif .identity_status != "resolved" then
        "1. Identity: not fully resolved from public evidence"
      else
        "1. Identity: resolved from public evidence"
      end
    ),
    (
      "2. Evidence: " + .summary
    ),
    (
      if (.disqualifiers | length) > 0 then
        "3. Red flag: " + .disqualifiers[0]
      elif (.ambiguities | length) > 0 then
        "3. Caution: " + .ambiguities[0]
      else
        "3. Caution: treat this as preliminary public-web enrichment, not hidden-data certainty"
      end
    ),
    (
      if (.source_urls | length) > 0 then
        "4. Source: " + .source_urls[0]
      else
        "4. Source: no strong source URL surfaced"
      end
    )
  ] | join("\n")
' "$tmp_report"
