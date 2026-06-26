#!/usr/bin/env bash
# posthog_sync.sh - PostHog dashboard management CLI
# Usage: posthog_sync.sh <create|sync|update|export> <config.json|dashboard_id>
set -euo pipefail

: "${POSTHOG_PERSONAL_API_KEY:?Set POSTHOG_PERSONAL_API_KEY}"
POSTHOG_HOST="${POSTHOG_HOST:-us.i.posthog.com}"
POSTHOG_UI_HOST="${POSTHOG_UI_HOST:-us.posthog.com}"
API_BASE="https://${POSTHOG_HOST}/api/projects/@current"

command -v jq >/dev/null 2>&1 || { echo "Error: jq is required. Install with: brew install jq / apt install jq" >&2; exit 1; }

api() {
  local method="$1" endpoint="$2"; shift 2
  curl -sS -X "$method" "${API_BASE}${endpoint}" \
    -H "Authorization: Bearer ${POSTHOG_PERSONAL_API_KEY}" \
    -H "Content-Type: application/json" "$@"
}

get_project_id() {
  api GET "/" | jq -r '.id'
}

# Map insight type to PostHog event query
build_insight_payload() {
  local name="$1" type="$2" filter_json="$3" domain="$4" math="${5:-total}" display="${6:-}" date_range="${7:--30d}"

  local event='$pageview'
  local properties="[]"

  if [[ -n "$filter_json" && "$filter_json" != "null" ]]; then
    local fkey fval
    fkey=$(echo "$filter_json" | jq -r '.key')
    fval=$(echo "$filter_json" | jq -r '.value')
    properties=$(jq -n --arg k "$fkey" --arg v "$fval" '[{"key":$k,"value":$v,"type":"event"}]')
  elif [[ -n "$domain" && "$domain" != "null" ]]; then
    properties=$(jq -n --arg d "$domain" '[{"key":"$current_url","value":$d,"operator":"icontains","type":"event"}]')
  fi

  local insight_math="$math"
  case "$type" in
    pageviews_total) display="${display:-BoldNumber}"; insight_math="total" ;;
    unique_users)    display="${display:-BoldNumber}"; insight_math="dau" ;;
    traffic_trend)   display="${display:-ActionsLineGraph}"; insight_math="total" ;;
    top_pages)       display="${display:-ActionsTable}"; insight_math="total"
      properties=$(echo "$properties" | jq '. + [{"key":"$current_url","type":"event"}]')
      ;;
  esac

  jq -n \
    --arg name "$name" \
    --arg display "$display" \
    --arg math "$insight_math" \
    --arg date_from "$date_range" \
    --arg event "$event" \
    --argjson properties "$properties" \
    '{
      name: $name,
      query: {
        kind: "EventsQuery",
        select: ["*"],
        event: $event,
        properties: $properties,
        math: $math,
        after: $date_from
      },
      filters: {
        insight: "TRENDS",
        events: [{id: $event, math: $math, properties: $properties}],
        display: $display,
        date_from: $date_from
      }
    }'
}

cmd_create() {
  local config_file="$1"
  [[ -f "$config_file" ]] || { echo "Error: Config file not found: $config_file" >&2; exit 1; }

  local name description filter domain
  name=$(jq -r '.name' "$config_file")
  description=$(jq -r '.description // ""' "$config_file")
  filter=$(jq -c '.filter // null' "$config_file")
  domain=$(jq -r '.domain_filter // null' "$config_file")

  echo "Creating dashboard: $name"
  local dash_result
  dash_result=$(api POST "/dashboards/" -d "$(jq -n --arg n "$name" --arg d "$description" '{name:$n, description:$d}')")
  local dash_id
  dash_id=$(echo "$dash_result" | jq -r '.id')

  if [[ -z "$dash_id" || "$dash_id" == "null" ]]; then
    echo "Error: Failed to create dashboard" >&2
    echo "$dash_result" >&2
    exit 1
  fi
  echo "Dashboard created: ID $dash_id"

  # Update config with dashboard_id
  local tmp
  tmp=$(mktemp)
  jq --argjson id "$dash_id" '.dashboard_id = $id' "$config_file" > "$tmp" && mv "$tmp" "$config_file"

  # Create insights
  local insight_count
  insight_count=$(jq '.insights | length' "$config_file")
  for (( i=0; i<insight_count; i++ )); do
    local iname itype imath idisplay irange
    iname=$(jq -r ".insights[$i].name" "$config_file")
    itype=$(jq -r ".insights[$i].type" "$config_file")
    imath=$(jq -r ".insights[$i].math // \"total\"" "$config_file")
    idisplay=$(jq -r ".insights[$i].display // \"\"" "$config_file")
    irange=$(jq -r ".insights[$i].date_range // \"-30d\"" "$config_file")

    echo "Creating insight: $iname"
    local payload
    payload=$(build_insight_payload "$iname" "$itype" "$filter" "$domain" "$imath" "$idisplay" "$irange")
    payload=$(echo "$payload" | jq --argjson did "$dash_id" '. + {dashboards: [$did]}')

    local result
    result=$(api POST "/insights/" -d "$payload")
    echo "$result" | jq '{id: .id, name: .name}'
  done

  local project_id
  project_id=$(get_project_id)
  echo "Dashboard URL: https://${POSTHOG_UI_HOST}/project/${project_id}/dashboard/${dash_id}"
}

cmd_sync() {
  local config_file="$1"
  [[ -f "$config_file" ]] || { echo "Error: Config file not found: $config_file" >&2; exit 1; }

  local dash_id
  dash_id=$(jq -r '.dashboard_id' "$config_file")
  [[ "$dash_id" != "null" && -n "$dash_id" ]] || { echo "Error: dashboard_id is null. Run create first." >&2; exit 1; }

  local filter domain
  filter=$(jq -c '.filter // null' "$config_file")
  domain=$(jq -r '.domain_filter // null' "$config_file")

  # Get existing insights on this dashboard
  local existing
  existing=$(api GET "/dashboards/${dash_id}/" | jq -r '[.tiles[].insight.name] | .[]' 2>/dev/null || echo "")

  local insight_count
  insight_count=$(jq '.insights | length' "$config_file")
  local created=0
  for (( i=0; i<insight_count; i++ )); do
    local iname itype imath idisplay irange
    iname=$(jq -r ".insights[$i].name" "$config_file")
    itype=$(jq -r ".insights[$i].type" "$config_file")
    imath=$(jq -r ".insights[$i].math // \"total\"" "$config_file")
    idisplay=$(jq -r ".insights[$i].display // \"\"" "$config_file")
    irange=$(jq -r ".insights[$i].date_range // \"-30d\"" "$config_file")

    if echo "$existing" | grep -qF "$iname"; then
      echo "Skipping (exists): $iname"
      continue
    fi

    echo "Creating insight: $iname"
    local payload
    payload=$(build_insight_payload "$iname" "$itype" "$filter" "$domain" "$imath" "$idisplay" "$irange")
    payload=$(echo "$payload" | jq --argjson did "$dash_id" '. + {dashboards: [$did]}')
    api POST "/insights/" -d "$payload" | jq '{id: .id, name: .name}'
    created=$((created + 1))
  done

  echo "Sync complete: $created new insights created"
}

cmd_update() {
  local config_file="$1"
  [[ -f "$config_file" ]] || { echo "Error: Config file not found: $config_file" >&2; exit 1; }

  local dash_id
  dash_id=$(jq -r '.dashboard_id' "$config_file")
  [[ "$dash_id" != "null" && -n "$dash_id" ]] || { echo "Error: dashboard_id is null." >&2; exit 1; }

  local filter domain
  filter=$(jq -c '.filter // null' "$config_file")
  domain=$(jq -r '.domain_filter // null' "$config_file")

  # Get existing insights
  local tiles
  tiles=$(api GET "/dashboards/${dash_id}/" | jq '[.tiles[] | {id: .insight.id, name: .insight.name}]')

  local insight_count
  insight_count=$(jq '.insights | length' "$config_file")
  local updated=0
  for (( i=0; i<insight_count; i++ )); do
    local iname itype imath idisplay irange
    iname=$(jq -r ".insights[$i].name" "$config_file")
    itype=$(jq -r ".insights[$i].type" "$config_file")
    imath=$(jq -r ".insights[$i].math // \"total\"" "$config_file")
    idisplay=$(jq -r ".insights[$i].display // \"\"" "$config_file")
    irange=$(jq -r ".insights[$i].date_range // \"-30d\"" "$config_file")

    local insight_id
    insight_id=$(echo "$tiles" | jq -r --arg n "$iname" '.[] | select(.name == $n) | .id')
    if [[ -z "$insight_id" ]]; then
      echo "Not found (skipping): $iname"
      continue
    fi

    echo "Updating insight: $iname (ID: $insight_id)"
    local payload
    payload=$(build_insight_payload "$iname" "$itype" "$filter" "$domain" "$imath" "$idisplay" "$irange")
    api PATCH "/insights/${insight_id}/" -d "$payload" | jq '{id: .id, name: .name}'
    updated=$((updated + 1))
  done

  echo "Update complete: $updated insights updated"
}

cmd_export() {
  local dash_id="$1"
  local dash
  dash=$(api GET "/dashboards/${dash_id}/")
  echo "$dash" | jq '{
    name: .name,
    description: .description,
    dashboard_id: .id,
    insights: [.tiles[] | {
      name: .insight.name,
      type: "custom",
      filters: .insight.filters
    }]
  }'
}

# --- Main ---
case "${1:-help}" in
  create) shift; cmd_create "$@" ;;
  sync)   shift; cmd_sync "$@" ;;
  update) shift; cmd_update "$@" ;;
  export) shift; cmd_export "$@" ;;
  help|--help|-h)
    echo "Usage: posthog_sync.sh <create|sync|update|export> <config.json|dashboard_id>"
    echo ""
    echo "Commands:"
    echo "  create <config.json>    Create dashboard + insights"
    echo "  sync   <config.json>    Add new insights (skip existing)"
    echo "  update <config.json>    Update all insights with current config"
    echo "  export <dashboard_id>   Export dashboard to JSON config"
    ;;
  *) echo "Unknown command: $1" >&2; exit 1 ;;
esac
