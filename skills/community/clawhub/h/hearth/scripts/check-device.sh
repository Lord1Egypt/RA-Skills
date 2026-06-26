#!/bin/bash
# hearth/scripts/check-device.sh — probe a single device
#
# Usage: ./check-device.sh <device-name>
# Reads device config from $HEARTH_CONFIG, ~/.hearth/devices.yaml, or ./devices.yaml.

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/config.sh
. "$SCRIPT_DIR/lib/config.sh"
# shellcheck source=lib/ssh.sh
. "$SCRIPT_DIR/lib/ssh.sh"
# shellcheck source=lib/probe.sh
. "$SCRIPT_DIR/lib/probe.sh"

device_name="${1:-}"
if [ -z "$device_name" ]; then
  echo "Usage: $0 <device-name>" >&2
  exit 1
fi

config_path=$(hearth_find_config) || {
  echo "ERROR: no devices.yaml found. Set HEARTH_CONFIG or create ~/.hearth/devices.yaml" >&2
  exit 1
}

# Load device record into associative array
declare -A dev
while IFS='=' read -r k v; do
  [ -n "$k" ] && dev["$k"]="$v"
done < <(hearth_get_device "$config_path" "$device_name")

if [ -z "${dev[name]:-}" ]; then
  echo "ERROR: device '$device_name' not found in $config_path" >&2
  exit 1
fi

# Pull defaults
ping_count=$(hearth_get_default "$config_path" "ping_count" "1")
ping_timeout=$(hearth_get_default "$config_path" "ping_timeout" "2")
default_connect_timeout=$(hearth_get_default "$config_path" "ssh_connect_timeout" "4")

# Per-device overrides
connect_timeout="${dev[ssh_connect_timeout]:-$default_connect_timeout}"

# Print device header
role="${dev[role]:-}"
[ -n "$role" ] && header_role=" ($role)" || header_role=""
echo "=== ${dev[address]} ${dev[name]}${header_role} ==="

# L1 — ping
if ! hearth_ping "${dev[address]}" "$ping_count" "$ping_timeout"; then
  echo "  L1 ping:    UNREACHABLE"
  exit 0
fi
echo "  L1 ping:    OK"

# Layers 2-4 depend on auth mode
case "${dev[auth]}" in
  http-only)
    hearth_format_no_ssh "http-only"
    ;;
  local|ssh-pass|ssh-key)
    services_csv=""
    if [ -n "${dev[services]:-}" ]; then
      # services is a JSON array string from python parser, e.g. ["ssh", "nginx"]
      # Strip [ ] and quotes, replace commas with commas (already are)
      services_csv=$(echo "${dev[services]}" | sed 's/[]["]//g' | tr -d ' ')
    fi
    remote_cmd=$(hearth_build_remote_bundle "$services_csv")
    result=$(hearth_ssh_run \
      "${dev[name]}" \
      "${dev[auth]}" \
      "${dev[user]:-}" \
      "${dev[address]}" \
      "${dev[password_env]:-}" \
      "${dev[key_path]:-}" \
      "$connect_timeout" \
      "${dev[ssh_warmup]:-false}" \
      "$remote_cmd" 2>/dev/null) || result=""

    if [ -z "$result" ]; then
      echo "  L2-L4:      SSH FAILED"
    else
      echo "$result" | hearth_format_layers

      # Override L4 if no_systemd is set
      if [ "${dev[no_systemd]:-false}" = "true" ]; then
        hearth_format_no_ssh "no-systemd"
      fi
    fi
    ;;
  *)
    echo "  L2-L4:      ERROR — unknown auth type '${dev[auth]}'"
    ;;
esac

# Layer 5 — apps
# Apps come through as a JSON string from python parser. We need to iterate.
# For Phase 2 simplicity, we use python to iterate and call back per-app.
if [ -n "${dev[apps]:-}" ]; then
  apps_summary=""
  while IFS='|' read -r app_name app_type app_url app_code app_match app_auth app_tls app_resolve app_cmd; do
    [ -z "$app_name" ] && continue
    case "$app_type" in
      http)
        line=$(hearth_http_probe "$app_name" "$app_url" "$app_code" "$app_match" "$app_auth" "$app_tls" "$app_resolve")
        ;;
      command)
        # Run the command on the device (or locally if auth=local)
        if [ "${dev[auth]}" = "http-only" ]; then
          line="$app_name=skipped (http-only host)"
        else
          out=$(hearth_ssh_run \
            "${dev[name]}" \
            "${dev[auth]}" \
            "${dev[user]:-}" \
            "${dev[address]}" \
            "${dev[password_env]:-}" \
            "${dev[key_path]:-}" \
            "$connect_timeout" \
            "false" \
            "$app_cmd" 2>/dev/null)
          if [ -n "$app_match" ]; then
            if echo "$out" | grep -qE "$app_match"; then
              line="$app_name=OK ($out)"
            else
              line="$app_name=MISMATCH ($out)"
            fi
          else
            line="$app_name=$out"
          fi
        fi
        ;;
      *)
        line="$app_name=ERROR (unknown type $app_type)"
        ;;
    esac
    [ -z "$apps_summary" ] && apps_summary="$line" || apps_summary="$apps_summary | $line"
  done < <(python3 -c "
import yaml, json, sys
with open('$config_path') as f:
    d = yaml.safe_load(f)
for dev in d.get('devices', []):
    if dev.get('name') == '$device_name':
        for app in dev.get('apps', []) or []:
            print('|'.join([
                app.get('name', ''),
                app.get('type', ''),
                app.get('url', ''),
                str(app.get('expect_code', '200')),
                app.get('expect_match', '') or '',
                app.get('auth_header_env', '') or '',
                str(app.get('verify_tls', 'true')).lower(),
                app.get('resolve', '') or '',
                app.get('command', '') or '',
            ]))
")

  if [ -n "$apps_summary" ]; then
    echo "  L5 app:     $apps_summary"
  fi
fi