#!/usr/bin/env bash
set -euo pipefail

CONFIG_PATH="${HOME}/.openclaw/workspace/config/mcporter.json"
PIXCAKE_APP=""
PIXCAKE_MCP=""
PIXCAKE_APP_SOURCE=""
PIXCAKE_MCP_SOURCE=""
CHECK_ONLY=false

usage() {
  cat >&2 <<'EOF'
Usage:
  setup.sh [--pixcake-app <path>] [--pixcake-mcp <path>] [--config-path <path>]
  setup.sh --check-only [--pixcake-app <path>] [--pixcake-mcp <path>] [--config-path <path>]

Options:
  --pixcake-app   Explicit PixCake app path or executable path
  --pixcake-mcp   Explicit pixcake-mcp executable path
  --config-path   mcporter config file path (default: ~/.openclaw/workspace/config/mcporter.json)
  --check-only    Only inspect environment, do not modify anything
  -h, --help      Show this help
EOF
  exit 2
}

log() {
  printf '%s\n' "$*"
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

is_executable_file() {
  [[ -f "$1" && -x "$1" ]]
}

platform_id() {
  case "$(uname -s)" in
    Darwin) echo "darwin" ;;
    CYGWIN*|MINGW*|MSYS*) echo "windows" ;;
    *) echo "unknown" ;;
  esac
}

canonicalize_path() {
  local input="$1"

  if [[ -z "$input" ]]; then
    return 1
  fi

  node -e "
    const fs = require('fs');
    const path = process.argv[1];
    try {
      console.log(fs.realpathSync(path));
    } catch {
      process.exit(1);
    }
  " "$input"
}

first_line() {
  awk 'NF { print; exit }'
}

lower_basename() {
  basename "$1" | tr '[:upper:]' '[:lower:]'
}

is_pixcake_app_candidate() {
  local base=""

  base="$(lower_basename "$1")"
  [[ "$base" == *pixcake* && "$base" != *mcp* ]]
}

is_pixcake_mcp_candidate() {
  local base=""

  base="$(lower_basename "$1")"
  [[ "$base" == "pixcake-mcp" || "$base" == "pixcake-mcp.exe" ]]
}

discover_mac_process_candidates() {
  local pattern="$1"

  if ! command -v pgrep >/dev/null 2>&1; then
    return 1
  fi

  pgrep -af "$pattern" 2>/dev/null | awk 'NF { print $2 }'
}

discover_mac_app_bundle() {
  find /Applications "${HOME}/Applications" -maxdepth 3 -type d -iname '*pixcake*.app' 2>/dev/null | sort | first_line
}

discover_mac_app_executable_from_bundle() {
  local app_bundle="$1"
  local macos_dir=""
  local candidate=""

  [[ -n "$app_bundle" ]] || return 1

  macos_dir="${app_bundle}/Contents/MacOS"
  [[ -d "$macos_dir" ]] || return 1

  while IFS= read -r candidate; do
    if is_pixcake_app_candidate "$candidate"; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done < <(find "$macos_dir" -maxdepth 1 -type f -perm -u+x 2>/dev/null | sort)

  while IFS= read -r candidate; do
    if ! is_pixcake_mcp_candidate "$candidate"; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done < <(find "$macos_dir" -maxdepth 1 -type f -perm -u+x 2>/dev/null | sort)
}

discover_mac_mcp_path() {
  local from_process=""
  local candidate=""

  while IFS= read -r candidate; do
    if is_pixcake_mcp_candidate "$candidate"; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done < <(discover_mac_process_candidates 'pixcake-mcp' || true)

  find /Applications "${HOME}/Applications" -maxdepth 5 -type f \( -iname 'pixcake-mcp' -o -iname 'pixcake-mcp.exe' \) 2>/dev/null | sort | first_line
}

powershell_query() {
  local script="$1"

  if command -v powershell.exe >/dev/null 2>&1; then
    powershell.exe -NoProfile -Command "$script"
  elif command -v pwsh >/dev/null 2>&1; then
    pwsh -NoProfile -Command "$script"
  else
    return 1
  fi
}

discover_windows_app_path() {
  local from_process=""

  from_process="$(powershell_query "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; Get-Process | Where-Object { \$_.Path -and \$_.Path -match 'pixcake' -and \$_.Path -notmatch 'pixcake-mcp' } | Select-Object -ExpandProperty Path -First 1" 2>/dev/null || true)"
  if [[ -n "$from_process" ]]; then
    printf '%s\n' "$from_process" | tr -d '\r'
    return 0
  fi

  powershell_query "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; Get-ChildItem 'C:\\Program Files','C:\\Program Files (x86)','D:\\','E:\\' -Filter 'pixcake*.exe' -Recurse -ErrorAction SilentlyContinue | Where-Object { \$_.Name -notmatch 'pixcake-mcp' } | Select-Object -ExpandProperty FullName -First 1" 2>/dev/null | tr -d '\r'
}

discover_windows_mcp_path() {
  local from_process=""

  from_process="$(powershell_query "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; Get-Process | Where-Object { \$_.Path -and \$_.Path -match 'pixcake-mcp' } | Select-Object -ExpandProperty Path -First 1" 2>/dev/null || true)"
  if [[ -n "$from_process" ]]; then
    printf '%s\n' "$from_process" | tr -d '\r'
    return 0
  fi

  powershell_query "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; Get-ChildItem 'C:\\Program Files','C:\\Program Files (x86)','D:\\','E:\\' -Filter 'pixcake-mcp.exe' -Recurse -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName -First 1" 2>/dev/null | tr -d '\r'
}

detect_paths() {
  local platform=""
  local bundle=""

  platform="$(platform_id)"

  if [[ -n "$PIXCAKE_APP" ]]; then
    PIXCAKE_APP="$(canonicalize_path "$PIXCAKE_APP" || printf '%s' "$PIXCAKE_APP")"
    PIXCAKE_APP_SOURCE="explicit"
  fi

  if [[ -n "$PIXCAKE_MCP" ]]; then
    PIXCAKE_MCP="$(canonicalize_path "$PIXCAKE_MCP" || printf '%s' "$PIXCAKE_MCP")"
    PIXCAKE_MCP_SOURCE="explicit"
  fi

  case "$platform" in
    darwin)
      if [[ -z "$PIXCAKE_APP" ]]; then
        while IFS= read -r candidate; do
          if is_pixcake_app_candidate "$candidate"; then
            PIXCAKE_APP="$candidate"
            PIXCAKE_APP_SOURCE="process"
            break
          fi
        done < <(discover_mac_process_candidates 'pixcake' || true)
      fi
      if [[ -z "$PIXCAKE_APP" ]]; then
        bundle="$(discover_mac_app_bundle || true)"
        PIXCAKE_APP="$(discover_mac_app_executable_from_bundle "$bundle" || true)"
        [[ -n "$PIXCAKE_APP" ]] && PIXCAKE_APP_SOURCE="filesystem"
      fi
      if [[ -z "$PIXCAKE_MCP" ]]; then
        while IFS= read -r candidate; do
          if is_pixcake_mcp_candidate "$candidate"; then
            PIXCAKE_MCP="$candidate"
            PIXCAKE_MCP_SOURCE="process"
            break
          fi
        done < <(discover_mac_process_candidates 'pixcake-mcp' || true)
      fi
      if [[ -z "$PIXCAKE_MCP" ]]; then
        PIXCAKE_MCP="$(discover_mac_mcp_path || true)"
        [[ -n "$PIXCAKE_MCP" ]] && PIXCAKE_MCP_SOURCE="filesystem"
      fi
      ;;
    windows)
      if [[ -z "$PIXCAKE_APP" ]]; then
        PIXCAKE_APP="$(discover_windows_app_path || true)"
        [[ -n "$PIXCAKE_APP" ]] && PIXCAKE_APP_SOURCE="filesystem"
      fi
      if [[ -z "$PIXCAKE_MCP" ]]; then
        PIXCAKE_MCP="$(discover_windows_mcp_path || true)"
        [[ -n "$PIXCAKE_MCP" ]] && PIXCAKE_MCP_SOURCE="filesystem"
      fi
      ;;
    *)
      log "[WARN] Unsupported platform for auto-discovery: $platform"
      ;;
  esac

  if [[ -n "$PIXCAKE_APP" ]]; then
    PIXCAKE_APP="$(canonicalize_path "$PIXCAKE_APP" || printf '%s' "$PIXCAKE_APP")"
  fi

  if [[ -n "$PIXCAKE_MCP" ]]; then
    PIXCAKE_MCP="$(canonicalize_path "$PIXCAKE_MCP" || printf '%s' "$PIXCAKE_MCP")"
  fi
}

config_has_pixcake() {
  local path="$1"

  [[ -f "$path" ]] || return 1

  node -e "
    const fs = require('fs');
    try {
      const config = JSON.parse(fs.readFileSync(process.argv[1], 'utf8'));
      const hasServer = Boolean(config && config.mcpServers && config.mcpServers.pixcake);
      process.exit(hasServer ? 0 : 1);
    } catch {
      process.exit(1);
    }
  " "$path"
}

write_config() {
  local config_dir=""
  local platform=""

  config_dir="$(dirname "$CONFIG_PATH")"
  platform="$(platform_id)"
  mkdir -p "$config_dir"

  node - "$CONFIG_PATH" "$PIXCAKE_MCP" "$platform" <<'NODE'
const fs = require('fs');
const path = require('path');
const [configPath, mcpPath, platform] = process.argv.slice(2);

let config = {};

try {
  config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
} catch {}

if (!config || typeof config !== 'object' || Array.isArray(config)) {
  config = {};
}

if (!config.mcpServers || typeof config.mcpServers !== 'object' || Array.isArray(config.mcpServers)) {
  config.mcpServers = {};
}

if (platform === 'windows') {
  config.mcpServers.pixcake = {
    transport: 'stdio',
    command: 'cmd',
    args: ['/c', mcpPath],
    cwd: path.win32.dirname(mcpPath)
  };
} else {
  config.mcpServers.pixcake = {
    transport: 'stdio',
    command: mcpPath
  };
}

fs.writeFileSync(configPath, JSON.stringify(config, null, 2) + '\n');
NODE
}

verify_with_mcporter() {
  if ! command_exists mcporter; then
    log "[WARN] mcporter not found on PATH; config written but runtime verification skipped"
    return 0
  fi

  if mcporter --config "$CONFIG_PATH" list pixcake --json >/dev/null 2>&1; then
    log "[OK] mcporter can list pixcake server"
  else
    log "[WARN] mcporter exists, but failed to list pixcake server"
  fi
}

install_mcporter() {
  if command_exists mcporter; then
    log "[OK] mcporter already installed: $(mcporter --version 2>/dev/null || echo 'unknown version')"
    return 0
  fi

  if ! command_exists npm; then
    log "[ERROR] mcporter not found and npm is unavailable"
    exit 1
  fi

  log "[INSTALL] Installing mcporter via npm..."
  if npm install -g mcporter 2>/dev/null; then
    :
  else
    log "[WARN] First install attempt failed, cleaning npm cache and retrying..."
    npm cache clean --force 2>/dev/null || true
    npm install -g mcporter
  fi

  if command_exists mcporter; then
    log "[OK] mcporter installed: $(mcporter --version 2>/dev/null || echo 'unknown version')"
    return 0
  fi

  log "[ERROR] mcporter installation failed"
  exit 1
}

check_status() {
  local probe_output=""

  log "=== PixCake MCP Status Check ==="

  detect_paths

  if [[ -n "$PIXCAKE_APP" ]]; then
    if [[ "$PIXCAKE_APP_SOURCE" == "process" ]]; then
      log "[OK] PixCake app running: $PIXCAKE_APP"
    else
      log "[OK] PixCake app path found: $PIXCAKE_APP"
    fi
  else
    log "[MISSING] PixCake app not found"
  fi

  if [[ -n "$PIXCAKE_MCP" ]]; then
    if [[ "$PIXCAKE_MCP_SOURCE" == "process" ]]; then
      log "[OK] pixcake-mcp running: $PIXCAKE_MCP"
    else
      log "[OK] pixcake-mcp path found: $PIXCAKE_MCP"
    fi
  else
    log "[MISSING] pixcake-mcp not found"
  fi

  if command_exists mcporter; then
    log "[OK] mcporter installed: $(mcporter --version 2>/dev/null || echo 'unknown version')"
  else
    log "[MISSING] mcporter not found on PATH"
    log "  Fix: ./scripts/setup.sh"
  fi

  if [[ -f "$CONFIG_PATH" ]]; then
    log "[OK] Config file exists: $CONFIG_PATH"
    if config_has_pixcake "$CONFIG_PATH"; then
      log "[OK] pixcake MCP server configured"
    else
      log "[MISSING] pixcake MCP server not in config"
    fi
  else
    log "[MISSING] Config file not found: $CONFIG_PATH"
  fi

  if command_exists mcporter && [[ -f "$CONFIG_PATH" ]]; then
    log ""
    log "=== PixCake Tool Probe ==="
    probe_output="$(mcporter --config "$CONFIG_PATH" list pixcake --schema --json 2>/dev/null || true)"
    if [[ -z "$probe_output" ]]; then
      log "[WARN] Failed to list pixcake tools"
    elif printf '%s' "$probe_output" | grep -q '"status"[[:space:]]*:[[:space:]]*"error"'; then
      if printf '%s' "$probe_output" | grep -q 'pixcake is not running'; then
        log "[WARN] PixCake client is not running; launching PixCake will also start pixcake-mcp"
      else
        log "[WARN] Failed to list pixcake tools"
        log "$probe_output"
      fi
    else
      log "$probe_output"
    fi
  fi
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --pixcake-app)
        PIXCAKE_APP="${2:-}"
        shift 2
        ;;
      --pixcake-mcp)
        PIXCAKE_MCP="${2:-}"
        shift 2
        ;;
      --config-path)
        CONFIG_PATH="${2:-}"
        shift 2
        ;;
      --check-only)
        CHECK_ONLY=true
        shift
        ;;
      -h|--help)
        usage
        ;;
      *)
        log "Unknown arg: $1"
        usage
        ;;
    esac
  done
}

main() {
  parse_args "$@"

  if $CHECK_ONLY; then
    check_status
    exit 0
  fi

  log "=== PixCake MCP Auto Setup ==="
  detect_paths

  install_mcporter

  if [[ -z "$PIXCAKE_MCP" ]]; then
    log "[ERROR] pixcake-mcp path not found"
    log "  Fix: pass --pixcake-mcp <path> or locate it first with the commands in SKILL.md"
    exit 1
  fi

  if [[ -n "$PIXCAKE_APP" ]]; then
    log "[OK] PixCake app path: $PIXCAKE_APP"
  else
    log "[WARN] PixCake app path not found; continuing because config only requires pixcake-mcp"
  fi

  log "[OK] pixcake-mcp path: $PIXCAKE_MCP"
  write_config
  log "[OK] Config written: $CONFIG_PATH"
  verify_with_mcporter

  log ""
  log "=== Setup Complete ==="
  log "Config: $CONFIG_PATH"
  log "PixCake app: ${PIXCAKE_APP:-not found}"
  log "pixcake-mcp: $PIXCAKE_MCP"
}

main "$@"
