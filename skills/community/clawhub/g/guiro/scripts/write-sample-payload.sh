#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_FILE="${1:-./payload.json}"
SAMPLE_KIND="${2:-dashboard}"
API_KEY="${GUIRO_API_KEY:-}"
CAPABILITIES_FILE="${GUIRO_CAPABILITIES_FILE:-.guiro/runtime-capabilities.json}"

DEFAULT_STORAGE_VERSION="1"
DEFAULT_A2UI_VERSION="0.9"
DEFAULT_CATALOG_ID="guiro.shadcn.detached.v1"

CAP_STORAGE_VERSION="${DEFAULT_STORAGE_VERSION}"
CAP_A2UI_VERSION="${DEFAULT_A2UI_VERSION}"
CAP_CATALOG_ID="${DEFAULT_CATALOG_ID}"
CAP_SOURCE="defaults"

json_extract_first() {
  local payload_file="$1"
  local jq_expr="$2"
  local py_expr="$3"

  if command -v jq >/dev/null 2>&1; then
    jq -r "${jq_expr}" "${payload_file}" 2>/dev/null || true
    return
  fi

  if command -v python >/dev/null 2>&1; then
    python - "${payload_file}" "${py_expr}" <<'PY'
import json
import sys

payload_file = sys.argv[1]
selector = sys.argv[2]

try:
    with open(payload_file, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception:
    print("")
    sys.exit(0)

if selector == "storage_versions":
    value = (data.get("storage_versions") or [""])[0]
elif selector == "a2ui_versions":
    value = (data.get("a2ui_versions") or [""])[0]
elif selector == "catalog_id":
    catalogs = data.get("catalogs") or []
    value = (catalogs[0] or {}).get("id", "") if catalogs else ""
else:
    value = ""

print(value)
PY
    return
  fi

  echo ""
}

load_capabilities() {
  local fetched="false"
  local args=()

  if [ -n "${API_KEY}" ]; then
    args+=(--out "${CAPABILITIES_FILE}")
    args+=(--api-key "${API_KEY}")
    if bash "${SCRIPT_DIR}/fetch-capabilities.sh" "${args[@]}" >/dev/null 2>&1; then
      CAP_SOURCE="fetched"
      fetched="true"
    fi
  fi

  if [ "${fetched}" != "true" ] && [ -f "${CAPABILITIES_FILE}" ]; then
    CAP_SOURCE="cache"
  fi

  if [ "${CAP_SOURCE}" = "defaults" ]; then
    return
  fi

  CAP_STORAGE_VERSION="$(json_extract_first "${CAPABILITIES_FILE}" '.storage_versions[0] // ""' 'storage_versions')"
  CAP_A2UI_VERSION="$(json_extract_first "${CAPABILITIES_FILE}" '.a2ui_versions[0] // ""' 'a2ui_versions')"
  CAP_CATALOG_ID="$(json_extract_first "${CAPABILITIES_FILE}" '.catalogs[0].id // ""' 'catalog_id')"

  if [ -z "${CAP_STORAGE_VERSION}" ]; then
    CAP_STORAGE_VERSION="${DEFAULT_STORAGE_VERSION}"
  fi
  if [ -z "${CAP_A2UI_VERSION}" ]; then
    CAP_A2UI_VERSION="${DEFAULT_A2UI_VERSION}"
  fi
  if [ -z "${CAP_CATALOG_ID}" ]; then
    CAP_CATALOG_ID="${DEFAULT_CATALOG_ID}"
  fi
}

case "${SAMPLE_KIND}" in
  dashboard|calendar|chart|donut)
    ;;
  -h|--help|help)
    cat <<EOF
Usage: bash ${SCRIPT_DIR}/write-sample-payload.sh [out-file] [dashboard|calendar|chart|donut]
EOF
    exit 0
    ;;
  *)
    echo "unsupported_sample_kind=${SAMPLE_KIND}" >&2
    echo "expected one of: dashboard, calendar, chart, donut" >&2
    exit 1
    ;;
esac

load_capabilities

if [[ "${SAMPLE_KIND}" == "dashboard" ]]; then
cat >"${OUT_FILE}" <<'JSON'
{
  "storage_version": "__STORAGE_VERSION__",
  "a2ui_version": "__A2UI_VERSION__",
  "catalog_id": "__CATALOG_ID__",
  "theme": {
    "primary": "#0f766e",
    "secondary": "#0f172a"
  },
  "messages": [
    {
      "version": "v0.9",
      "createSurface": {
        "surfaceId": "share-main",
        "catalogId": "__CATALOG_ID__"
      }
    },
    {
      "version": "v0.9",
      "updateComponents": {
        "surfaceId": "share-main",
        "components": [
          {
            "id": "root",
            "component": "Card",
            "child": "page"
          },
          {
            "id": "page",
            "component": "Column",
            "gap": "lg",
            "children": ["eyebrow", "title", "subtitle", "metrics-section", "table-section", "timeline-section"]
          },
          {
            "id": "eyebrow",
            "component": "Badge",
            "label": "Published Snapshot",
            "variant": "secondary",
            "size": "sm"
          },
          {
            "id": "title",
            "component": "Text",
            "text": "Job Market & Hiring Analytics Snapshot",
            "variant": "h1"
          },
          {
            "id": "subtitle",
            "component": "Text",
            "text": "Sample bundle for validate/create smoke tests.",
            "tone": "muted"
          },
          {
            "id": "metrics-section",
            "component": "Column",
            "gap": "sm",
            "children": ["metrics-title", "metrics-row", "offer-rate"]
          },
          {
            "id": "metrics-title",
            "component": "Text",
            "text": "Hiring Pulse",
            "variant": "h2"
          },
          {
            "id": "metrics-row",
            "component": "Row",
            "gap": "md",
            "children": ["open-roles", "applicants", "api-health"]
          },
          {
            "id": "open-roles",
            "component": "Badge",
            "label": "Open Roles: 142",
            "variant": "outline"
          },
          {
            "id": "applicants",
            "component": "Badge",
            "label": "Applicants: 923",
            "variant": "outline"
          },
          {
            "id": "offer-rate",
            "component": "ProgressIndicator",
            "value": 21,
            "max": 100
          },
          {
            "id": "api-health",
            "component": "Badge",
            "label": "API healthy",
            "variant": "success"
          },
          {
            "id": "table-section",
            "component": "Column",
            "gap": "sm",
            "children": ["table-title", "pipelines-table"]
          },
          {
            "id": "table-title",
            "component": "Text",
            "text": "Top Hiring Pipelines",
            "variant": "h2"
          },
          {
            "id": "pipelines-table",
            "component": "DataTable",
            "columns": [
              { "key": "role", "header": "Role" },
              { "key": "stage", "header": "Stage" },
              { "key": "count", "header": "Count" }
            ],
            "data": [
              { "role": "Software Engineer", "stage": "Interview", "count": 27 },
              { "role": "Data Analyst", "stage": "Screen", "count": 19 },
              { "role": "Product Manager", "stage": "Offer", "count": 6 }
            ]
          },
          {
            "id": "timeline-section",
            "component": "Column",
            "gap": "sm",
            "children": ["timeline-title", "timeline"]
          },
          {
            "id": "timeline-title",
            "component": "Text",
            "text": "This Week",
            "variant": "h2"
          },
          {
            "id": "timeline",
            "component": "List",
            "children": ["event-mon", "event-wed", "event-fri"]
          },
          {
            "id": "event-mon",
            "component": "Text",
            "text": "Mon: Campaign Launch"
          },
          {
            "id": "event-wed",
            "component": "Text",
            "text": "Wed: Hiring Event"
          },
          {
            "id": "event-fri",
            "component": "Text",
            "text": "Fri: Offer Batch"
          }
        ]
      }
    }
  ]
}
JSON
elif [[ "${SAMPLE_KIND}" == "calendar" ]]; then
cat >"${OUT_FILE}" <<'JSON'
{
  "storage_version": "__STORAGE_VERSION__",
  "a2ui_version": "__A2UI_VERSION__",
  "catalog_id": "__CATALOG_ID__",
  "theme": {
    "primary": "oklch(0.527 0.154 150.069)",
    "secondary": "oklch(0.967 0.001 286.375)"
  },
  "messages": [
    {
      "version": "v0.9",
      "createSurface": {
        "surfaceId": "calendar-main",
        "catalogId": "__CATALOG_ID__"
      }
    },
    {
      "version": "v0.9",
      "updateComponents": {
        "surfaceId": "calendar-main",
        "components": [
          {
            "id": "root",
            "component": "Card",
            "child": "page"
          },
          {
            "id": "page",
            "component": "Column",
            "gap": "lg",
            "children": ["eyebrow", "title-row", "subtitle", "release-calendar"]
          },
          {
            "id": "title-row",
            "component": "Row",
            "gap": "md",
            "children": ["title-icon", "title"]
          },
          {
            "id": "title-icon",
            "component": "Icon",
            "name": "calendar-days",
            "size": 28,
            "color": "oklch(0.527 0.154 150.069)",
            "label": "Calendar view"
          },
          {
            "id": "eyebrow",
            "component": "Badge",
            "label": "Calendar Sample",
            "variant": "secondary",
            "size": "sm"
          },
          {
            "id": "title",
            "component": "Text",
            "text": "Product Launch Calendar",
            "variant": "h1"
          },
          {
            "id": "subtitle",
            "component": "Text",
            "text": "Example bundle showing the read-only Calendar display with highlighted days, details below, and a catalog icon.",
            "tone": "muted"
          },
          {
            "id": "release-calendar",
            "component": "Calendar",
            "title": "April 2026 Milestones",
            "description": "Marked days represent launch and campaign events; details follow below the month view.",
            "selectionMode": "single",
            "selected": "2026-04-16",
            "month": "2026-04-01",
            "events": [
              {
                "date": "2026-04-09",
                "label": "Beta readiness review",
                "detail": "Cross-functional go/no-go with product, QA, and support.",
                "tone": "muted"
              },
              {
                "date": "2026-04-16",
                "label": "Public launch day",
                "detail": "Homepage refresh, release notes, and campaign send all go live.",
                "tone": "accent"
              },
              {
                "date": "2026-04-23",
                "label": "Partner webinar",
                "detail": "Enablement session covering adoption highlights and rollout steps.",
                "tone": "default"
              }
            ]
          }
        ]
      }
    }
  ]
}
JSON
elif [[ "${SAMPLE_KIND}" == "chart" ]]; then
cat >"${OUT_FILE}" <<'JSON'
{
  "storage_version": "__STORAGE_VERSION__",
  "a2ui_version": "__A2UI_VERSION__",
  "catalog_id": "__CATALOG_ID__",
  "theme": {
    "primary": "oklch(0.448 0.119 151.328)",
    "secondary": "oklch(0.274 0.006 286.033)"
  },
  "messages": [
    {
      "version": "v0.9",
      "createSurface": {
        "surfaceId": "chart-main",
        "catalogId": "__CATALOG_ID__"
      }
    },
    {
      "version": "v0.9",
      "updateComponents": {
        "surfaceId": "chart-main",
        "components": [
          {
            "id": "root",
            "component": "Card",
            "child": "page"
          },
          {
            "id": "page",
            "component": "Column",
            "gap": "lg",
            "children": ["eyebrow", "title", "subtitle", "revenue-chart"]
          },
          {
            "id": "eyebrow",
            "component": "Badge",
            "label": "Chart Sample",
            "variant": "secondary",
            "size": "sm"
          },
          {
            "id": "title",
            "component": "Text",
            "text": "Quarterly Revenue Mix",
            "variant": "h1"
          },
          {
            "id": "subtitle",
            "component": "Text",
            "text": "Example bundle showing the custom Chart component with two revenue series.",
            "tone": "muted"
          },
          {
            "id": "revenue-chart",
            "component": "Chart",
            "title": "New vs Expansion Revenue",
            "description": "Revenue by quarter in USD.",
            "chartType": "bar",
            "xKey": "quarter",
            "valueFormat": "currency",
            "currency": "USD",
            "series": [
              {
                "key": "newRevenue",
                "label": "New Revenue"
              },
              {
                "key": "expansionRevenue",
                "label": "Expansion Revenue"
              }
            ],
            "data": [
              {
                "quarter": "Q1",
                "newRevenue": 184000,
                "expansionRevenue": 92000
              },
              {
                "quarter": "Q2",
                "newRevenue": 228000,
                "expansionRevenue": 108000
              },
              {
                "quarter": "Q3",
                "newRevenue": 251000,
                "expansionRevenue": 133000
              },
              {
                "quarter": "Q4",
                "newRevenue": 289000,
                "expansionRevenue": 157000
              }
            ]
          }
        ]
      }
    }
  ]
}
JSON
else
cat >"${OUT_FILE}" <<'JSON'
{
  "storage_version": "__STORAGE_VERSION__",
  "a2ui_version": "__A2UI_VERSION__",
  "catalog_id": "__CATALOG_ID__",
  "theme": {
    "primary": "oklch(0.448 0.119 151.328)",
    "secondary": "oklch(0.274 0.006 286.033)"
  },
  "messages": [
    {
      "version": "v0.9",
      "createSurface": {
        "surfaceId": "donut-main",
        "catalogId": "__CATALOG_ID__"
      }
    },
    {
      "version": "v0.9",
      "updateComponents": {
        "surfaceId": "donut-main",
        "components": [
          {
            "id": "root",
            "component": "Card",
            "child": "page"
          },
          {
            "id": "page",
            "component": "Column",
            "gap": "lg",
            "children": ["eyebrow", "title", "subtitle", "savings-chart"]
          },
          {
            "id": "eyebrow",
            "component": "Badge",
            "label": "Donut Sample",
            "variant": "secondary",
            "size": "sm"
          },
          {
            "id": "title",
            "component": "Text",
            "text": "Savings Goal Progress",
            "variant": "h1"
          },
          {
            "id": "subtitle",
            "component": "Text",
            "text": "Example bundle showing the custom Chart component in donut mode.",
            "tone": "muted"
          },
          {
            "id": "savings-chart",
            "component": "Chart",
            "title": "House Fund",
            "description": "$24,000 saved toward a $30,000 target.",
            "chartType": "donut",
            "xKey": "segment",
            "valueFormat": "currency",
            "currency": "USD",
            "series": [
              {
                "key": "amount",
                "label": "Saved"
              }
            ],
            "data": [
              {
                "segment": "Saved",
                "amount": 24000,
                "color": "oklch(0.696 0.17 162.48)"
              },
              {
                "segment": "Remaining",
                "amount": 6000,
                "color": "oklch(0.432 0.095 166.913)"
              }
            ]
          }
        ]
      }
    }
  ]
}
JSON
fi

if command -v python >/dev/null 2>&1; then
  python - "${OUT_FILE}" "${CAP_STORAGE_VERSION}" "${CAP_A2UI_VERSION}" "${CAP_CATALOG_ID}" <<'PY'
import json
import sys

path = sys.argv[1]
storage = sys.argv[2]
a2ui = sys.argv[3]
catalog = sys.argv[4]

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

data["storage_version"] = storage
data["a2ui_version"] = a2ui
data["catalog_id"] = catalog

for message in data.get("messages", []):
    create_surface = message.get("createSurface")
    if isinstance(create_surface, dict):
        create_surface["catalogId"] = catalog

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
PY
else
  sed -i.bak "s/__STORAGE_VERSION__/${CAP_STORAGE_VERSION}/g" "${OUT_FILE}"
  sed -i.bak "s/__A2UI_VERSION__/${CAP_A2UI_VERSION}/g" "${OUT_FILE}"
  sed -i.bak "s/__CATALOG_ID__/${CAP_CATALOG_ID}/g" "${OUT_FILE}"
  rm -f "${OUT_FILE}.bak"
fi

echo "sample_payload_written=${OUT_FILE}"
echo "sample_payload_kind=${SAMPLE_KIND}"
echo "sample_payload_runtime_source=${CAP_SOURCE}"
echo "sample_payload_storage_version=${CAP_STORAGE_VERSION}"
echo "sample_payload_a2ui_version=${CAP_A2UI_VERSION}"
echo "sample_payload_catalog_id=${CAP_CATALOG_ID}"
echo "next_step=bash ${SCRIPT_DIR}/create-guiro.sh --payload ${OUT_FILE}"
