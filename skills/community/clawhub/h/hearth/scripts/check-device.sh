#!/bin/bash
# hearth/scripts/check-device.sh — probe a single device (5-layer, read-only)
#
# Usage: ./check-device.sh [--json] [--no-color] <device-name>
# Reads device config from $HEARTH_CONFIG, ~/.hearth/devices.yaml, or ./devices.yaml.
#
# Exit code reflects health:  0 = healthy   1 = degraded   2 = down/unreachable

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/config.sh
. "$SCRIPT_DIR/lib/config.sh"
# shellcheck source=lib/ssh.sh
. "$SCRIPT_DIR/lib/ssh.sh"
# shellcheck source=lib/probe.sh
. "$SCRIPT_DIR/lib/probe.sh"

json_out=false
device_name=""
while [ $# -gt 0 ]; do
  case "$1" in
    --json) json_out=true; shift ;;
    --no-color) HEARTH_COLOR=never; export HEARTH_COLOR; shift ;;
    --) shift; device_name="${1:-}"; shift || true ;;
    -*) echo "Unknown option: $1" >&2; exit 64 ;;
    *) device_name="$1"; shift ;;
  esac
done

if [ -z "$device_name" ]; then
  echo "Usage: $0 [--json] [--no-color] <device-name>" >&2
  exit 64
fi

hearth_color_init

config_path=$(hearth_find_config) || {
  echo "ERROR: no devices.yaml found. Set HEARTH_CONFIG or create ~/.hearth/devices.yaml" >&2
  exit 2
}

# Load device record into associative array
declare -A dev
while IFS='=' read -r k v; do
  [ -n "$k" ] && dev["$k"]="$v"
done < <(hearth_get_device "$config_path" "$device_name")

if [ -z "${dev[name]:-}" ]; then
  echo "ERROR: device '$device_name' not found in $config_path" >&2
  exit 2
fi

# Defaults / thresholds
ping_count=$(hearth_get_default "$config_path" "ping_count" "1")
ping_timeout=$(hearth_get_default "$config_path" "ping_timeout" "2")
default_connect_timeout=$(hearth_get_default "$config_path" "ssh_connect_timeout" "4")
disk_warn=$(hearth_get_default "$config_path" "disk_warn_pct" "90")
mem_warn=$(hearth_get_default "$config_path" "mem_warn_pct" "90")
load_per_cpu=$(hearth_get_default "$config_path" "load_warn_per_cpu" "2")
temp_warn=$(hearth_get_default "$config_path" "temp_warn_c" "75")
connect_timeout="${dev[ssh_connect_timeout]:-$default_connect_timeout}"

addr="${dev[address]:-}"
role="${dev[role]:-}"
auth="${dev[auth]:-}"
no_systemd="${dev[no_systemd]:-false}"

# ---- Collected state -------------------------------------------------------
l1="OK"
up=""; load=""; load1="0"; ncpu="1"
mem_summary=""; disk_summary=""; disk_pct=""; mem_total_kb=""; mem_avail_kb=""; temp_c=""
svc_raw=""
ssh_state="ok"          # ok | failed | n/a
status="healthy"
warnings=()

mark_degraded() { [ "$status" = "down" ] || status="degraded"; warnings+=("$1"); }

# ---- L1: ping --------------------------------------------------------------
if ! hearth_ping "$addr" "$ping_count" "$ping_timeout"; then
  l1="UNREACHABLE"
  status="down"
  warnings+=("L1 ping: unreachable")
fi

# ---- L2-L4: depends on auth mode ------------------------------------------
if [ "$status" != "down" ]; then
  case "$auth" in
    http-only)
      ssh_state="n/a"
      ;;
    local|ssh-pass|ssh-key)
      services_csv=""
      if [ -n "${dev[services]:-}" ]; then
        services_csv=$(echo "${dev[services]}" | sed 's/[]["]//g' | tr -d ' ')
      fi
      remote_cmd=$(hearth_build_remote_bundle "$services_csv")
      result=$(hearth_ssh_run \
        "${dev[name]}" "$auth" "${dev[user]:-}" "$addr" \
        "${dev[password_env]:-}" "${dev[key_path]:-}" \
        "$connect_timeout" "${dev[ssh_warmup]:-false}" \
        "$remote_cmd" 2>/dev/null) || result=""

      if [ -z "$result" ]; then
        ssh_state="failed"
        mark_degraded "SSH failed (L2-L4 unmeasured)"
      else
        while IFS='|' read -r tag a b c d e f; do
          case "$tag" in
            L2) up="$a"; load="$b" ;;
            L3) mem_summary="$a"; disk_summary="$b" ;;
            L3R) disk_pct="$a"; load1="$b"; ncpu="$c"; mem_total_kb="$d"; mem_avail_kb="$e"; temp_c="$f" ;;
            L4) svc_raw="${a#"${a%%[![:space:]]*}"}" ;;
          esac
        done <<< "$result"
      fi
      ;;
    *)
      ssh_state="failed"
      mark_degraded "unknown auth type '$auth'"
      ;;
  esac
fi

# ---- Threshold evaluation (only where we actually measured) -----------------
if [ "$status" != "down" ] && [ "$ssh_state" = "ok" ]; then
  # disk
  if [ -n "$disk_pct" ] && [ "$disk_pct" -ge "$disk_warn" ] 2>/dev/null; then
    mark_degraded "disk ${disk_pct}% >= ${disk_warn}%"
    disk_warn_hit=1
  fi
  # memory used %
  if [ -n "$mem_total_kb" ] && [ -n "$mem_avail_kb" ] && [ "$mem_total_kb" -gt 0 ] 2>/dev/null; then
    mem_used_pct=$(awk -v t="$mem_total_kb" -v a="$mem_avail_kb" 'BEGIN{printf "%d", (t-a)*100/t}')
    if [ "$mem_used_pct" -ge "$mem_warn" ] 2>/dev/null; then
      mark_degraded "memory ${mem_used_pct}% >= ${mem_warn}%"
      mem_warn_hit=1
    fi
  fi
  # load vs cpu
  load_ceiling=$(awk -v n="$ncpu" -v f="$load_per_cpu" 'BEGIN{printf "%.2f", n*f}')
  if hearth_gt "$load1" "$load_ceiling"; then
    mark_degraded "load ${load1} > ${load_ceiling} (${ncpu} cpu x ${load_per_cpu})"
    load_warn_hit=1
  fi
  # temperature
  if [ -n "$temp_c" ] && hearth_gt "$temp_c" "$temp_warn"; then
    mark_degraded "temp ${temp_c}°C >= ${temp_warn}°C"
    temp_warn_hit=1
  fi
  # services (skip when no_systemd; honour expected_failed_units)
  if [ "$no_systemd" != "true" ] && [ -n "$svc_raw" ]; then
    efu=""
    if [ -n "${dev[expected_failed_units]:-}" ]; then
      efu=" $(echo "${dev[expected_failed_units]}" | sed 's/[]["]//g' | tr ',' ' ') "
    fi
    for pair in $svc_raw; do
      svcname="${pair%%=*}"; st="${pair#*=}"
      if [ "$st" != "active" ]; then
        case "$efu" in *" $svcname "*) continue ;; esac
        mark_degraded "service ${pair}"
      fi
    done
  fi
fi

# ---- L5: apps --------------------------------------------------------------
apps_results=()
if [ "$status" != "down" ] && [ -n "${dev[apps]:-}" ]; then
  while IFS='|' read -r app_name app_type app_url app_code app_match app_auth app_tls app_resolve app_cmd app_nomatch; do
    [ -z "$app_name" ] && continue
    case "$app_type" in
      http)
        line=$(hearth_http_probe "$app_name" "$app_url" "$app_code" "$app_match" "$app_auth" "$app_tls" "$app_resolve")
        ;;
      command)
        if [ "$auth" = "http-only" ]; then
          line="$app_name=skipped (http-only host)"
        else
          out=$(hearth_ssh_run \
            "${dev[name]}" "$auth" "${dev[user]:-}" "$addr" \
            "${dev[password_env]:-}" "${dev[key_path]:-}" \
            "$connect_timeout" "false" "$app_cmd" 2>/dev/null)
          if [ -n "$app_match" ] && ! echo "$out" | grep -qE "$app_match"; then
            line="$app_name=MISMATCH ($out)"
          elif [ -n "$app_nomatch" ] && echo "$out" | grep -qE "$app_nomatch"; then
            line="$app_name=MISMATCH ($out)"
          elif [ -n "$app_match" ] || [ -n "$app_nomatch" ]; then
            line="$app_name=OK ($out)"
          else
            line="$app_name=$out"
          fi
        fi
        ;;
      *)
        line="$app_name=ERROR (unknown type $app_type)"
        ;;
    esac
    apps_results+=("$line")
    if ! hearth_http_ok "$line"; then
      mark_degraded "app ${line}"
    fi
  done < <(HEARTH_CFG="$config_path" HEARTH_DEV="$device_name" python3 -c "
import yaml, os
with open(os.environ['HEARTH_CFG']) as f:
    d = yaml.safe_load(f) or {}
target = os.environ['HEARTH_DEV']
for dev in d.get('devices', []) or []:
    if dev.get('name') == target:
        for app in dev.get('apps', []) or []:
            print('|'.join([
                str(app.get('name', '')),
                str(app.get('type', '')),
                str(app.get('url', '')),
                str(app.get('expect_code', '200')),
                str(app.get('expect_match', '') or ''),
                str(app.get('auth_header_env', '') or ''),
                str(app.get('verify_tls', 'true')).lower(),
                str(app.get('resolve', '') or ''),
                str(app.get('command', '') or ''),
                str(app.get('expect_no_match', '') or ''),
            ]))
        break
")
fi

# ===========================================================================
# RENDER
# ===========================================================================
rc=0
case "$status" in healthy) rc=0 ;; degraded) rc=1 ;; down) rc=2 ;; esac

if [ "$json_out" = "true" ]; then
  svc_json_src=""
  if [ "$ssh_state" = "ok" ] && [ "$no_systemd" != "true" ]; then svc_json_src="$svc_raw"; fi
  HEARTH_J_NAME="${dev[name]}" HEARTH_J_ADDR="$addr" HEARTH_J_ROLE="$role" \
  HEARTH_J_AUTH="$auth" HEARTH_J_STATUS="$status" HEARTH_J_L1="$l1" \
  HEARTH_J_UP="$up" HEARTH_J_LOAD="$load" HEARTH_J_MEM="$mem_summary" \
  HEARTH_J_DISK="$disk_summary" HEARTH_J_DISKPCT="$disk_pct" \
  HEARTH_J_TEMP="$temp_c" HEARTH_J_SSH="$ssh_state" HEARTH_J_NOSYS="$no_systemd" \
  HEARTH_J_SVC="$svc_json_src" \
  HEARTH_J_APPS="$(printf '%s\n' "${apps_results[@]:-}")" \
  HEARTH_J_WARN="$(printf '%s\n' "${warnings[@]:-}")" \
  python3 -c "
import os, json
def env(k): return os.environ.get(k, '')
obj = {
  'name': env('HEARTH_J_NAME'),
  'address': env('HEARTH_J_ADDR'),
  'role': env('HEARTH_J_ROLE'),
  'auth': env('HEARTH_J_AUTH'),
  'status': env('HEARTH_J_STATUS'),
  'ping': 'ok' if env('HEARTH_J_L1') == 'OK' else 'unreachable',
}
layers = {}
if env('HEARTH_J_UP'): layers['uptime'] = env('HEARTH_J_UP')
if env('HEARTH_J_LOAD'): layers['load'] = env('HEARTH_J_LOAD').split()
if env('HEARTH_J_MEM'): layers['mem'] = env('HEARTH_J_MEM')
if env('HEARTH_J_DISK'):
    layers['disk'] = env('HEARTH_J_DISK')
    if env('HEARTH_J_DISKPCT'):
        try: layers['disk_used_pct'] = int(env('HEARTH_J_DISKPCT'))
        except ValueError: pass
if env('HEARTH_J_TEMP'):
    try: layers['temp_c'] = float(env('HEARTH_J_TEMP'))
    except ValueError: pass
svc = {}
for pair in env('HEARTH_J_SVC').split():
    if '=' in pair:
        k, v = pair.split('=', 1); svc[k] = v
if svc: layers['services'] = svc
elif env('HEARTH_J_NOSYS') == 'true': layers['services'] = 'no-systemd (N/A)'
elif env('HEARTH_J_SSH') == 'n/a': layers['services'] = 'unmanaged (no SSH)'
apps = {}
for line in env('HEARTH_J_APPS').splitlines():
    line = line.strip()
    if not line: continue
    if '=' in line:
        k, v = line.split('=', 1); apps[k] = v
    else:
        apps[line] = ''
if apps: layers['apps'] = apps
obj['layers'] = layers
warns = [w for w in env('HEARTH_J_WARN').splitlines() if w.strip()]
if warns: obj['warnings'] = warns
print(json.dumps(obj, separators=(',', ':')))
"
  exit $rc
fi

# ---- Text render -----------------------------------------------------------
[ -n "$role" ] && header_role=" ($role)" || header_role=""
printf '=== %s %s%s === %s\n' "$addr" "${dev[name]}" "$header_role" "$(hearth_status_tag "$status")"

# L1
if [ "$l1" = "OK" ]; then
  printf '  L1 ping:    %sOK%s\n' "$C_GREEN" "$C_RESET"
else
  printf '  L1 ping:    %sUNREACHABLE%s\n' "$C_RED" "$C_RESET"
  # L2-L5 skipped
  if [ ${#warnings[@]} -gt 0 ]; then
    printf '  %sreason:%s     %s\n' "$C_DIM" "$C_RESET" "$(IFS='; '; echo "${warnings[*]}")"
  fi
  exit $rc
fi

case "$ssh_state" in
  n/a)
    printf '  L2 uptime:  %sunmanaged-host (no SSH)%s\n' "$C_DIM" "$C_RESET"
    printf '  L3 mem:     %sunmanaged-host (no SSH)%s\n' "$C_DIM" "$C_RESET"
    printf '  L4 svc:     %sunmanaged-host (no SSH/WMI access)%s\n' "$C_DIM" "$C_RESET"
    ;;
  failed)
    printf '  L2-L4:      %sSSH FAILED%s\n' "$C_RED" "$C_RESET"
    ;;
  ok)
    # L2
    if [ "${load_warn_hit:-0}" = "1" ]; then
      printf '  L2 uptime:  %s, load: %s%s%s ⚠%s\n' "$up" "$C_AMBER" "$load" "$C_BOLD" "$C_RESET"
    else
      printf '  L2 uptime:  %s, load: %s\n' "$up" "$load"
    fi
    # L3 (mem + disk, with optional temp)
    mem_disp="$mem_summary"; [ "${mem_warn_hit:-0}" = "1" ] && mem_disp="${C_AMBER}${mem_summary} ⚠${C_RESET}"
    disk_disp="$disk_summary"; [ "${disk_warn_hit:-0}" = "1" ] && disk_disp="${C_AMBER}${disk_summary} ⚠${C_RESET}"
    temp_disp=""
    if [ -n "$temp_c" ]; then
      if [ "${temp_warn_hit:-0}" = "1" ]; then
        temp_disp=" | temp: ${C_AMBER}${temp_c}°C ⚠${C_RESET}"
      else
        temp_disp=" | temp: ${temp_c}°C"
      fi
    fi
    printf '  L3 mem:     %s | disk: %s%s\n' "$mem_disp" "$disk_disp" "$temp_disp"
    # L4 services (coloured per state)
    if [ "$no_systemd" = "true" ]; then
      printf '  L4 svc:     %sno-systemd (chroot — N/A)%s\n' "$C_DIM" "$C_RESET"
    elif [ -n "$svc_raw" ]; then
      svc_disp=""
      for pair in $svc_raw; do
        st="${pair#*=}"
        case "$st" in
          active)  col="$C_GREEN" ;;
          failed)  col="$C_RED" ;;
          *)       col="$C_AMBER" ;;
        esac
        svc_disp="$svc_disp ${col}${pair}${C_RESET}"
      done
      printf '  L4 svc:    %s\n' "$svc_disp"
    else
      printf '  L4 svc:     %s(none configured)%s\n' "$C_DIM" "$C_RESET"
    fi
    ;;
esac

# L5 apps
if [ ${#apps_results[@]} -gt 0 ]; then
  app_disp=""
  for line in "${apps_results[@]}"; do
    if hearth_http_ok "$line"; then col="$C_GREEN"; else col="$C_AMBER"; fi
    [ -z "$app_disp" ] && app_disp="${col}${line}${C_RESET}" || app_disp="$app_disp | ${col}${line}${C_RESET}"
  done
  printf '  L5 app:     %s\n' "$app_disp"
fi

# Degraded reason summary
if [ "$status" = "degraded" ] && [ ${#warnings[@]} -gt 0 ]; then
  reason="$(IFS=$'\n'; printf '%s; ' "${warnings[@]}")"
  reason="${reason%; }"
  printf '  %sreason:%s     %s%s%s\n' "$C_DIM" "$C_RESET" "$C_AMBER" "$reason" "$C_RESET"
fi

exit $rc
