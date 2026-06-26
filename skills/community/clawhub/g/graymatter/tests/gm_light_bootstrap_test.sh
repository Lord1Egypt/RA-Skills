#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$(mktemp -d "${TMPDIR:-/tmp}/gm-light-bundle.XXXXXX")"
trap 'rm -rf "$OUT" >/dev/null 2>&1 || true' EXIT

assert_file() {
  if [[ ! -f "$1" ]]; then
    echo "Missing generated file: $1" >&2
    exit 1
  fi
}

assert_executable() {
  if [[ ! -x "$1" ]]; then
    echo "Generated file is not executable: $1" >&2
    exit 1
  fi
}

assert_contains() {
  local pattern="$1"
  local file="$2"
  if ! grep -q "$pattern" "$file"; then
    echo "Expected '$pattern' in $file" >&2
    exit 1
  fi
}

"$ROOT/scripts/gm-light-bootstrap" "$OUT" >/dev/null

assert_file "$OUT/api.hbs.yaml"
assert_file "$OUT/api.yaml"
assert_file "$OUT/docker-compose.yaml"
assert_file "$OUT/dashboard/index.html"
assert_file "$OUT/UPGRADE.md"
assert_file "$OUT/application-bundle/template.json"
assert_file "$OUT/application-bundle/openapi.json"
assert_file "$OUT/application-bundle/workflows/graymatter-local-bootstrap.workflow.json"
assert_file "$OUT/application-bundle/thorapi/graymatter-local.bundle.yaml"
assert_file "$OUT/application-bundle/components/graymatter-dashboard.yaml"
assert_file "$OUT/application-bundle/components/memory-workbench.yaml"
assert_file "$OUT/application-bundle/components/mothership-sync.yaml"
assert_file "$OUT/application-bundle/components/swarm-protocol.yaml"
assert_file "$OUT/application-bundle/components/live-telemetry.yaml"
assert_file "$OUT/application-bundle/valkyr-components/rbac-core.yaml"
assert_file "$OUT/application-bundle/valkyr-components/data-workbooks.yaml"
assert_file "$OUT/local-server/pom.xml"
assert_file "$OUT/local-server/README.md"
assert_file "$OUT/local-server/manifest.json"
assert_executable "$OUT/local-server/bin/graymatter-local-server"
assert_file "$OUT/local-server/src/main/java/com/valkyrlabs/graymatter/localserver/GrayMatterLocalServerApplication.java"
assert_file "$OUT/local-server/src/main/java/com/valkyrlabs/graymatter/localserver/model/MemoryEntry.java"
assert_file "$OUT/local-server/src/main/java/com/valkyrlabs/graymatter/localserver/model/PrincipalRecord.java"
assert_file "$OUT/local-server/src/main/java/com/valkyrlabs/graymatter/localserver/model/UserPreferences.java"
assert_file "$OUT/local-server/src/main/java/com/valkyrlabs/graymatter/localserver/model/WorkbookRecord.java"
assert_file "$OUT/local-server/src/main/java/com/valkyrlabs/graymatter/localserver/config/SecurityConfig.java"
assert_file "$OUT/local-server/src/main/java/com/valkyrlabs/graymatter/localserver/controller/LiveTelemetryController.java"
assert_file "$OUT/local-server/src/main/java/com/valkyrlabs/graymatter/localserver/controller/MothershipSyncController.java"
assert_file "$OUT/local-server/src/main/java/com/valkyrlabs/graymatter/localserver/controller/OpenApiController.java"
assert_file "$OUT/local-server/src/main/java/com/valkyrlabs/graymatter/localserver/controller/SwarmProtocolController.java"
assert_file "$OUT/local-server/src/main/java/com/valkyrlabs/graymatter/localserver/controller/WorkbookController.java"
assert_file "$OUT/local-server/src/main/java/com/valkyrlabs/graymatter/localserver/repository/WorkbookRecordRepository.java"
assert_file "$OUT/local-server/src/main/resources/application.properties"
assert_file "$OUT/local-server/src/main/resources/openapi.json"
assert_file "$OUT/local-server/src/main/resources/static/index.html"

assert_contains "graymatter-light" "$OUT/docker-compose.yaml"
assert_contains "starter 500 credits" "$OUT/UPGRADE.md"
assert_contains "\${THORAPI_IMAGE:-ghcr.io/valkyrlabs/thorapi:latest}" "$OUT/docker-compose.yaml"
assert_contains "\${GRAYMATTER_LIGHT_PORT:-8080}:8080" "$OUT/docker-compose.yaml"
assert_contains "THORAPI_TEMPLATE=/app/api.hbs.yaml" "$OUT/docker-compose.yaml"
assert_contains "THORAPI_SPEC=/app/api.yaml" "$OUT/docker-compose.yaml"
assert_contains "/api/graymatter/dashboard" "$OUT/api.hbs.yaml"
assert_contains "/api/graymatter/dashboard" "$OUT/api.yaml"
assert_contains "/Workbook" "$OUT/api.hbs.yaml"
assert_contains "Principal" "$OUT/api.hbs.yaml"
assert_contains "UserPreferences" "$OUT/api.hbs.yaml"
assert_contains "MemoryEntry" "$OUT/api.hbs.yaml"
assert_contains "/MemoryEntry/{id}" "$OUT/api.hbs.yaml"
assert_contains "/MemoryEntry/query" "$OUT/api.hbs.yaml"
assert_contains "/SwarmOps/graph" "$OUT/api.hbs.yaml"
assert_contains "x-graymatter-mcp-contract" "$OUT/api.hbs.yaml"
assert_contains "memory_write" "$OUT/api.hbs.yaml"
assert_contains "memory_read" "$OUT/api.hbs.yaml"
assert_contains "memory_query" "$OUT/api.hbs.yaml"
assert_contains "graph_get" "$OUT/api.hbs.yaml"
assert_contains "schema_summary" "$OUT/api.hbs.yaml"
assert_contains "ThorAPI must expose these paths so the standalone GrayMatter MCP server can target this base URL" "$OUT/api.hbs.yaml"
assert_contains "{{server_url}}" "$OUT/api.hbs.yaml"
assert_contains "http://localhost:8080" "$OUT/api.yaml"
if grep -q "{{server_url}}" "$OUT/api.yaml"; then
  echo "Rendered api.yaml should not contain template placeholders" >&2
  exit 1
fi
assert_contains "/MemoryEntry/query" "$OUT/application-bundle/openapi.json"
assert_contains "/SwarmOps/graph" "$OUT/application-bundle/openapi.json"
assert_contains "x-graymatter-mcp-contract" "$OUT/application-bundle/openapi.json"
assert_contains "GrayMatter Light Control Panel" "$OUT/dashboard/index.html"
assert_contains "/MemoryEntry" "$OUT/dashboard/index.html"
assert_contains "/Workbook" "$OUT/dashboard/index.html"
assert_contains '"generationMode": "thorapi-febe"' "$OUT/local-server/manifest.json"
assert_contains '"sourceTemplate": "graymatter-local"' "$OUT/local-server/manifest.json"
assert_contains "MothershipPromotionBridge" "$OUT/local-server/manifest.json"
assert_contains "SwarmProtocolBridge" "$OUT/local-server/manifest.json"
assert_contains "LiveTelemetryPanel" "$OUT/local-server/manifest.json"
assert_contains '"data-workbooks"' "$OUT/application-bundle/template.json"
assert_contains '"swarm-protocol"' "$OUT/application-bundle/template.json"
assert_contains "GrayMatterDashboard" "$OUT/application-bundle/components/graymatter-dashboard.yaml"
assert_contains "MemoryEntryWorkbench" "$OUT/application-bundle/components/memory-workbench.yaml"
assert_contains "MothershipPromotionBridge" "$OUT/application-bundle/components/mothership-sync.yaml"
assert_contains "SwarmProtocolBridge" "$OUT/application-bundle/components/swarm-protocol.yaml"
assert_contains "LiveTelemetryPanel" "$OUT/application-bundle/components/live-telemetry.yaml"
assert_contains "/api/graymatter/sync/mothership" "$OUT/application-bundle/openapi.json"
assert_contains "/api/graymatter/swarm/protocol" "$OUT/application-bundle/openapi.json"
assert_contains "/api/graymatter/telemetry/status" "$OUT/application-bundle/openapi.json"
assert_contains "/Workbook" "$OUT/application-bundle/openapi.json"
assert_contains "/api-docs" "$OUT/local-server/src/main/resources/openapi.json"
assert_contains "x-graymatter-mcp-contract" "$OUT/local-server/src/main/resources/openapi.json"
assert_contains "Data Workbooks" "$OUT/application-bundle/valkyr-components/data-workbooks.yaml"
assert_contains "spring-boot-starter-parent" "$OUT/local-server/pom.xml"
assert_contains "<java.version>17</java.version>" "$OUT/local-server/pom.xml"
assert_contains "native-maven-plugin" "$OUT/local-server/pom.xml"
assert_contains '@Table(name = "memory_entry")' "$OUT/local-server/src/main/java/com/valkyrlabs/graymatter/localserver/model/MemoryEntry.java"
assert_contains '@Table(name = "principal")' "$OUT/local-server/src/main/java/com/valkyrlabs/graymatter/localserver/model/PrincipalRecord.java"
assert_contains '@Table(name = "user_preferences")' "$OUT/local-server/src/main/java/com/valkyrlabs/graymatter/localserver/model/UserPreferences.java"
assert_contains '@Table(name = "workbook")' "$OUT/local-server/src/main/java/com/valkyrlabs/graymatter/localserver/model/WorkbookRecord.java"
assert_contains "RBAC" "$OUT/local-server/src/main/resources/static/index.html"
assert_contains "Data Workbooks" "$OUT/local-server/src/main/resources/static/index.html"
assert_contains "Valkyr Labs" "$OUT/local-server/src/main/resources/static/index.html"
assert_contains 'id="loginPanel"' "$OUT/local-server/src/main/resources/static/index.html"
assert_contains '.authenticated #loginPanel' "$OUT/local-server/src/main/resources/static/index.html"
assert_contains 'body.classList.add("authenticated")' "$OUT/local-server/src/main/resources/static/index.html"
assert_contains "Memory Graph Workspace" "$OUT/local-server/src/main/resources/static/index.html"
assert_contains "Promote / Synchronize" "$OUT/local-server/src/main/resources/static/index.html"
assert_contains "valkyrlabs.com" "$OUT/local-server/src/main/resources/static/index.html"
assert_contains "Swarm Protocol" "$OUT/local-server/src/main/resources/static/index.html"
assert_contains "Live Telemetry" "$OUT/local-server/src/main/resources/static/index.html"
assert_contains "System Equalizer" "$OUT/local-server/src/main/resources/static/index.html"
assert_contains "/api/graymatter/telemetry/status" "$OUT/local-server/src/main/resources/static/index.html"
assert_contains "memory.entries" "$OUT/local-server/src/main/java/com/valkyrlabs/graymatter/localserver/controller/LiveTelemetryController.java"
assert_contains "system.equalizer" "$OUT/local-server/src/main/java/com/valkyrlabs/graymatter/localserver/controller/LiveTelemetryController.java"
assert_contains "graymatter-swarm-v0.1" "$OUT/local-server/src/main/java/com/valkyrlabs/graymatter/localserver/controller/SwarmProtocolController.java"
assert_contains "PROMOTION_PREPARED" "$OUT/local-server/src/main/java/com/valkyrlabs/graymatter/localserver/controller/MothershipSyncController.java"
assert_contains "GrayMatter Local Server" "$OUT/local-server/README.md"

echo "gm_light_bootstrap_test: ok"
