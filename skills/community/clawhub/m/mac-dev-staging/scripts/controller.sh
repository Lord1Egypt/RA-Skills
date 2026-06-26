#!/usr/bin/env bash
set -euo pipefail

export PATH=/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'EOF'
usage:
  controller.sh status
  controller.sh ports [port...]
  controller.sh env
  controller.sh verify
  controller.sh gateway-ping [url]
  controller.sh build [cwd] [script]
  controller.sh start <apache|php|mariadb|nginx>
  controller.sh stop <apache|php|mariadb|nginx>
  controller.sh restart <apache|php|mariadb|nginx>
  controller.sh receipt --action NAME --status STATUS [--detail TEXT] [--target NAME]
EOF
}

service_action() {
  local action="$1"
  local service="${2:-}"
  case "$service" in
    apache)
      case "$action" in
        start|stop|restart)
          sudo apachectl "$action"
          ;;
        *)
          echo "unsupported apache action: $action" >&2
          exit 1
          ;;
      esac
      ;;
    php|mariadb|nginx)
      brew services "$action" "$service"
      ;;
    *)
      echo "unknown service: $service" >&2
      exit 1
      ;;
  esac
}

cmd="${1:-}"
shift || true

case "$cmd" in
  status)
    echo "=== brew services ==="
    brew services list | egrep 'php|mariadb|nginx' || true
    echo
    echo "=== apache ==="
    apachectl -S 2>/dev/null | sed -n '1,12p' || true
    echo
    echo "=== ports ==="
    "$SCRIPT_DIR/detect-ports.sh"
    ;;
  ports)
    "$SCRIPT_DIR/detect-ports.sh" "$@"
    ;;
  env)
    "$SCRIPT_DIR/render-local-gateway-env.sh"
    ;;
  verify)
    "$SCRIPT_DIR/verify-stack.sh"
    ;;
  gateway-ping)
    url="${1:-http://127.0.0.1:28789/}"
    curl -IsS "$url" | sed -n '1,5p'
    ;;
  build)
    build_cwd="${1:-$PWD}"
    build_script="${2:-build}"
    if [ ! -d "$build_cwd" ]; then
      echo "missing build directory: $build_cwd" >&2
      exit 1
    fi
    (
      cd "$build_cwd"
      npm run "$build_script"
    )
    ;;
  start|stop|restart)
    service_action "$cmd" "${1:-}"
    ;;
  receipt)
    "$SCRIPT_DIR/write-receipt.sh" "$@"
    ;;
  ""|-h|--help|help)
    usage
    ;;
  *)
    echo "unknown command: $cmd" >&2
    usage >&2
    exit 1
    ;;
esac
