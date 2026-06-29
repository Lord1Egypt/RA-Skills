#!/usr/bin/env bash
# hello-env / check-env.sh — Universal dev-environment health check.
#
# Pure bash, zero deps. Works on macOS / Linux / containers / K8s pods.
#
# Author: Evan Song (github.com/Songhonglei)
# License: MIT
# Repo: https://github.com/Songhonglei/better-agent-skills

set -uo pipefail
# Note: we deliberately do NOT use `set -e`. A diagnostic tool must keep going
# even if individual checks fail — failures are reported, not fatal.

# ───────────────────────────────────────────────────────────────────────────
# Defaults (lowest priority)
# ───────────────────────────────────────────────────────────────────────────
DEFAULT_PROBE_ENV="KUBERNETES_SERVICE_HOST,K8S_NAMESPACE"

# ───────────────────────────────────────────────────────────────────────────
# Resolve from env vars (mid priority)
# ───────────────────────────────────────────────────────────────────────────
WORKDIR="${HELLO_ENV_WORKDIR:-}"
WATCH_DIR="${HELLO_ENV_WATCH_DIR:-}"
CONFIG_PATH="${HELLO_ENV_CONFIG:-}"
PROBE_ENV="${HELLO_ENV_PROBE_ENV:-$DEFAULT_PROBE_ENV}"
FORCE_PVC="${HELLO_ENV_FORCE_PVC:-}"
SNAPSHOT_DIR="${HELLO_ENV_SNAPSHOT_DIR:-}"

# ───────────────────────────────────────────────────────────────────────────
# CLI flags (highest priority — override env)
# ───────────────────────────────────────────────────────────────────────────
show_help() {
  cat <<'EOF'
hello-env — Universal dev-environment health check (pure bash, zero deps)

Usage:
  bash check-env.sh [flags]

Flags:
  --workdir <path>          Working directory to check (default: current dir)
  --watch-dir <path>        Directory whose subfolder count is snapshotted
                            for PVC monitoring (default: same as --workdir)
  --config <path>           Optional config file to check existence
  --probe-env "A,B,C"       Comma-separated env vars to probe for K8s/container
                            context (default: KUBERNETES_SERVICE_HOST,K8S_NAMESPACE)
  --force-pvc               Force PVC monitoring even when no probe env hits
  --snapshot-dir <path>     Where to store device/count snapshots
                            (default: <workdir>/.hello-env)
  -h, --help                Show this help and exit

Env vars (lower priority than flags):
  HELLO_ENV_WORKDIR, HELLO_ENV_WATCH_DIR, HELLO_ENV_CONFIG,
  HELLO_ENV_PROBE_ENV, HELLO_ENV_FORCE_PVC=1, HELLO_ENV_SNAPSHOT_DIR

Examples:
  bash check-env.sh
  bash check-env.sh --workdir /opt/myapp --probe-env "MY_REGION,DEPLOY_ENV"
  bash check-env.sh --force-pvc --config /etc/myapp/config.json
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --workdir)        WORKDIR="$2"; shift 2 ;;
    --workdir=*)      WORKDIR="${1#*=}"; shift ;;
    --watch-dir)      WATCH_DIR="$2"; shift 2 ;;
    --watch-dir=*)    WATCH_DIR="${1#*=}"; shift ;;
    --config)         CONFIG_PATH="$2"; shift 2 ;;
    --config=*)       CONFIG_PATH="${1#*=}"; shift ;;
    --probe-env)      PROBE_ENV="$2"; shift 2 ;;
    --probe-env=*)    PROBE_ENV="${1#*=}"; shift ;;
    --force-pvc)      FORCE_PVC=1; shift ;;
    --snapshot-dir)   SNAPSHOT_DIR="$2"; shift 2 ;;
    --snapshot-dir=*) SNAPSHOT_DIR="${1#*=}"; shift ;;
    -h|--help)        show_help; exit 0 ;;
    *)
      echo "Unknown argument: $1" >&2
      echo "Try '$0 --help' for usage." >&2
      exit 2
      ;;
  esac
done

# ───────────────────────────────────────────────────────────────────────────
# Apply fallbacks
# ───────────────────────────────────────────────────────────────────────────
WORKDIR="${WORKDIR:-$PWD}"
WATCH_DIR="${WATCH_DIR:-$WORKDIR}"
SNAPSHOT_DIR="${SNAPSHOT_DIR:-${WORKDIR}/.hello-env}"
SNAPSHOT_DEVICE="${SNAPSHOT_DIR}/last-device"
SNAPSHOT_COUNT="${SNAPSHOT_DIR}/last-watch-count"

# ───────────────────────────────────────────────────────────────────────────
# Output helpers
# ───────────────────────────────────────────────────────────────────────────
ok()   { echo "  ✅ $*"; }
warn() { echo "  ⚠️  $*"; }
fail() { echo "  ❌ $*"; }
info() { echo "  ℹ️  $*"; }

# ───────────────────────────────────────────────────────────────────────────
# Container/K8s probe — returns 0 if any var in $PROBE_ENV is set,
# or /.dockerenv exists, or cgroup says container; otherwise 1.
# Sets globals: CONTAINER_HIT_VAR, CONTAINER_HIT_REASON
# ───────────────────────────────────────────────────────────────────────────
CONTAINER_HIT_VAR=""
CONTAINER_HIT_REASON=""
probe_container_env() {
  local IFS=','
  for var in $PROBE_ENV; do
    var="$(echo "$var" | xargs)"  # trim
    [ -z "$var" ] && continue
    # Indirect expansion via eval — bash 3.x compatible (macOS default bash 3.2)
    # Validate var name is a valid shell identifier to avoid eval injection.
    case "$var" in
      [a-zA-Z_][a-zA-Z0-9_]*) ;;
      *) continue ;;
    esac
    local val=""
    eval "val=\"\${${var}:-}\""
    if [ -n "$val" ]; then
      CONTAINER_HIT_VAR="$var"
      CONTAINER_HIT_REASON="env:${var}=${val}"
      return 0
    fi
  done
  if [ -f /.dockerenv ]; then
    CONTAINER_HIT_REASON="/.dockerenv exists"
    return 0
  fi
  # /proc/1/cgroup is Linux-only; skip on macOS / Windows
  if [ "$IS_WINDOWS" = "0" ] && [ "$OS_TYPE" = "Linux" ] && [ -f /proc/1/cgroup ] && grep -qE 'docker|kubepods|containerd' /proc/1/cgroup 2>/dev/null; then
    CONTAINER_HIT_REASON="/proc/1/cgroup matches container pattern"
    return 0
  fi
  return 1
}

echo ""
echo "══════════════════════════════════════════"
echo "  hello-env — environment health check"
echo "══════════════════════════════════════════"

# ── 1. OS ───────────────────────────────────────────────────────────────
echo ""
echo "[OS]"
OS_TYPE="$(uname -s)"
IS_WINDOWS=0
case "$OS_TYPE" in
  Darwin)
    OS_VER="$(sw_vers -productVersion 2>/dev/null || echo 'unknown')"
    ok "macOS $OS_VER ($(uname -m))"
    ;;
  Linux)
    if [ -f /etc/os-release ]; then
      OS_VER="$(. /etc/os-release && echo "$PRETTY_NAME")"
    else
      OS_VER="$(uname -r)"
    fi
    ok "Linux — $OS_VER ($(uname -m))"
    ;;
  MINGW*|MSYS*|CYGWIN*)
    IS_WINDOWS=1
    ok "Windows ($OS_TYPE) — running under Git Bash / MSYS / Cygwin"
    info "Some Linux-specific checks (cgroup container detection, PVC monitoring) will be skipped."
    ;;
  *)
    warn "Unknown OS: $OS_TYPE"
    ;;
esac

# ── 2. Current user ─────────────────────────────────────────────────────
echo ""
echo "[User]"
CURRENT_USER="$(whoami 2>/dev/null || id -un 2>/dev/null || echo 'unknown')"
# On Windows (Git Bash), whoami may return "DOMAIN\user" — strip the domain prefix.
case "$CURRENT_USER" in
  *\\*) CURRENT_USER="${CURRENT_USER##*\\}" ;;
esac
UID_VAL="$(id -u 2>/dev/null || echo '?')"
GID_VAL="$(id -g 2>/dev/null || echo '?')"
HOME_DIR="${HOME:-unknown}"
ok "${CURRENT_USER} (uid=${UID_VAL}, gid=${GID_VAL})"
info "HOME: ${HOME_DIR}"
if [ "$UID_VAL" = "0" ]; then
  warn "Running as root — be careful with destructive commands"
fi

# ── 3. Node.js ──────────────────────────────────────────────────────────
echo ""
echo "[Node.js]"
if command -v node >/dev/null 2>&1; then
  NODE_PATH="$(command -v node)"
  NODE_VER="$(node --version 2>/dev/null || echo 'failed')"
  ok "${NODE_VER}"
  info "Path: ${NODE_PATH}"
  if command -v npm >/dev/null 2>&1; then
    NPM_VER="$(npm --version 2>/dev/null || echo '?')"
    info "npm:  ${NPM_VER}"
  fi
else
  warn "Node.js not installed"
fi

# ── 4. Python3 ──────────────────────────────────────────────────────────
echo ""
echo "[Python3]"
if command -v python3 >/dev/null 2>&1; then
  PY_PATH="$(command -v python3)"
  PY_VER="$(python3 --version 2>/dev/null || echo 'failed')"
  ok "${PY_VER}"
  info "Path: ${PY_PATH}"
else
  warn "python3 not installed"
fi

# ── 5. Basic tools ──────────────────────────────────────────────────────
echo ""
echo "[Basic tools]"
for tool in git curl jq make docker; do
  if command -v "$tool" >/dev/null 2>&1; then
    TOOL_PATH="$(command -v "$tool")"
    case "$tool" in
      git)    TVER="$(git --version 2>/dev/null | awk '{print $3}')" ;;
      curl)   TVER="$(curl --version 2>/dev/null | head -1 | awk '{print $2}')" ;;
      jq)     TVER="$(jq --version 2>/dev/null | sed 's/^jq-//')" ;;
      make)   TVER="$(make --version 2>/dev/null | head -1 | awk '{print $NF}')" ;;
      docker) TVER="$(docker --version 2>/dev/null | awk '{print $3}' | sed 's/,$//')" ;;
    esac
    ok "${tool} ${TVER:-?}  (${TOOL_PATH})"
  else
    info "${tool}: not installed"
  fi
done

# ── 6. Network ──────────────────────────────────────────────────────────
echo ""
echo "[Network]"
HOST_NAME="$(hostname 2>/dev/null || echo 'unknown')"
ok "Hostname: ${HOST_NAME}"

IPS=""
if command -v hostname >/dev/null 2>&1 && hostname -I >/dev/null 2>&1; then
  IPS="$(hostname -I 2>/dev/null | xargs)"
elif command -v ifconfig >/dev/null 2>&1; then
  IPS="$(ifconfig 2>/dev/null | awk '/inet /{print $2}' | grep -v '^127\.' | xargs)"
elif command -v ip >/dev/null 2>&1; then
  IPS="$(ip -4 addr 2>/dev/null | awk '/inet /{print $2}' | cut -d/ -f1 | grep -v '^127\.' | xargs)"
fi

if [ -n "$IPS" ]; then
  ok "IP: ${IPS}"
  PRIMARY_IP="$(echo "$IPS" | awk '{print $1}')"
  if echo "$PRIMARY_IP" | grep -qE '^([1-9][0-9]?|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.[0-9]+\.[0-9]+\.[0-9]+$'; then
    OCTET1="$(echo "$PRIMARY_IP" | cut -d. -f1)"
    OCTET2="$(echo "$PRIMARY_IP" | cut -d. -f2)"
    OCTET3="$(echo "$PRIMARY_IP" | cut -d. -f3)"
    if [ "$OCTET1" = "10" ]; then
      info "Subnet (inferred /16): ${OCTET1}.${OCTET2}.0.0/16"
    elif [ "$OCTET1" = "192" ] && [ "$OCTET2" = "168" ]; then
      info "Subnet (inferred /24): ${OCTET1}.${OCTET2}.${OCTET3}.0/24"
    elif [ "$OCTET1" = "172" ] && [ "$OCTET2" -ge 16 ] 2>/dev/null && [ "$OCTET2" -le 31 ] 2>/dev/null; then
      info "Subnet (inferred /16): ${OCTET1}.${OCTET2}.0.0/16"
    else
      info "Subnet: public or custom private range (not inferred)"
    fi
  fi
else
  warn "Could not determine IP address"
fi

# ── 7. Container / K8s detection ───────────────────────────────────────
echo ""
echo "[Container / K8s]"
info "Probing env vars: ${PROBE_ENV}"
if probe_container_env; then
  ok "Container/K8s context detected (${CONTAINER_HIT_REASON})"
  IS_CONTAINER=1
  # Echo any probe env that's set (bash 3.x compatible loop)
  __old_ifs="$IFS"
  IFS=','
  for var in $PROBE_ENV; do
    IFS="$__old_ifs"
    var="$(echo "$var" | xargs)"
    [ -z "$var" ] && { IFS=','; continue; }
    case "$var" in
      [a-zA-Z_][a-zA-Z0-9_]*) ;;
      *) IFS=','; continue ;;
    esac
    local_val=""
    eval "local_val=\"\${${var}:-}\""
    [ -n "$local_val" ] && info "  ${var} = ${local_val}"
    IFS=','
  done
  IFS="$__old_ifs"
else
  IS_CONTAINER=0
  info "No container/K8s indicators found"
  if [ -z "$FORCE_PVC" ]; then
    info "PVC monitoring will skip. Pass --force-pvc to enable anyway."
  fi
fi

# ── 8. Workdir ─────────────────────────────────────────────────────────
echo ""
echo "[Workdir]"
if [ -d "$WORKDIR" ]; then
  ok "Path: $WORKDIR"
  if [ -d "$WORKDIR/.git" ]; then
    ok "Git initialized"
    if command -v git >/dev/null 2>&1; then
      BRANCH="$(cd "$WORKDIR" && git symbolic-ref --short HEAD 2>/dev/null || echo 'detached')"
      info "Branch: ${BRANCH}"
    fi
  else
    warn "Git not initialized (try: cd $WORKDIR && git init)"
  fi
else
  fail "Workdir does not exist: $WORKDIR"
fi

# ── 9. Config file (only when --config provided) ───────────────────────
if [ -n "$CONFIG_PATH" ]; then
  echo ""
  echo "[Config]"
  if [ -f "$CONFIG_PATH" ]; then
    ok "Exists: $CONFIG_PATH"
    CONFIG_SIZE="$(wc -c < "$CONFIG_PATH" 2>/dev/null | xargs || echo '?')"
    info "Size: ${CONFIG_SIZE} bytes"
  else
    fail "Not found: $CONFIG_PATH"
  fi
fi

# ── 10. PVC persistence (auto in K8s, or --force-pvc) ──────────────────
if [ "$IS_WINDOWS" = "1" ]; then
  if [ "$IS_CONTAINER" = "1" ] || [ -n "$FORCE_PVC" ]; then
    echo ""
    echo "[PVC persistence]"
    info "Skipped on Windows: device-number semantics differ; PVC monitoring is Linux/macOS-only."
  fi
elif { [ "$IS_CONTAINER" = "1" ] || [ -n "$FORCE_PVC" ]; } && command -v df >/dev/null 2>&1; then
  echo ""
  echo "[PVC persistence]"

  if [ ! -d "$SNAPSHOT_DIR" ]; then
    info "First run — creating snapshot dir: $SNAPSHOT_DIR"
  fi
  mkdir -p "$SNAPSHOT_DIR" 2>/dev/null || {
    warn "Cannot create snapshot dir: $SNAPSHOT_DIR (PVC checks skipped)"
    SNAPSHOT_DIR=""
  }

  if [ -n "$SNAPSHOT_DIR" ]; then
    CURRENT_DEVICE="$(df "$WORKDIR" 2>/dev/null | awk 'NR==2{print $1}')"
    DEVICE_CHANGED=0
    if [ -n "$CURRENT_DEVICE" ]; then
      ok "Mount device: $CURRENT_DEVICE"
      if [ -f "$SNAPSHOT_DEVICE" ]; then
        LAST_DEVICE="$(cat "$SNAPSHOT_DEVICE" 2>/dev/null || echo '')"
        if [ -n "$LAST_DEVICE" ] && [ "$LAST_DEVICE" != "$CURRENT_DEVICE" ]; then
          warn "Device changed: $LAST_DEVICE → $CURRENT_DEVICE"
          warn "Likely PVC remount. Verify: $WATCH_DIR contents, config files, etc."
          DEVICE_CHANGED=1
        else
          ok "Device unchanged"
        fi
      else
        info "First-time device snapshot"
      fi
      echo "$CURRENT_DEVICE" > "$SNAPSHOT_DEVICE" 2>/dev/null || true
    fi

    if [ -d "$WATCH_DIR" ]; then
      CURRENT_COUNT="$(find "$WATCH_DIR" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l | xargs)"
      if [ -f "$SNAPSHOT_COUNT" ]; then
        LAST_COUNT="$(cat "$SNAPSHOT_COUNT" 2>/dev/null || echo '0')"
        DELTA=$((CURRENT_COUNT - LAST_COUNT))
        if [ "$DELTA" -lt 0 ]; then
          ABS_DELTA=${DELTA#-}
          if [ "$DEVICE_CHANGED" = "1" ]; then
            warn "Watch-dir count: $LAST_COUNT → $CURRENT_COUNT (−$ABS_DELTA) + device changed → high-confidence PVC remount"
          else
            info "Watch-dir count: $LAST_COUNT → $CURRENT_COUNT (−$ABS_DELTA), device unchanged → likely manual removal"
          fi
        elif [ "$DELTA" -gt 0 ]; then
          ok "Watch-dir count: $CURRENT_COUNT (+$DELTA)"
        else
          ok "Watch-dir count: $CURRENT_COUNT (unchanged)"
        fi
      else
        info "First-time watch-dir snapshot ($CURRENT_COUNT subdirs)"
      fi
      echo "$CURRENT_COUNT" > "$SNAPSHOT_COUNT" 2>/dev/null || true
    else
      info "Watch dir does not exist: $WATCH_DIR (count snapshot skipped)"
    fi
  fi
fi

echo ""
echo "══════════════════════════════════════════"
echo "  done"
echo "══════════════════════════════════════════"
echo ""
