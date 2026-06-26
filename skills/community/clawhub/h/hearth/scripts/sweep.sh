#!/bin/bash
# hearth/scripts/sweep.sh — run check-device.sh across all devices
#
# Usage:
#   ./sweep.sh                       # run sweep across all devices
#   ./sweep.sh --device <name>       # check just one device
#   ./sweep.sh --group <name>        # check just devices in a named group
#   ./sweep.sh --dry-run             # validate config, don't probe
#   ./sweep.sh --version             # print version
#   ./sweep.sh --help                # this message

set -u

VERSION="0.1.4"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/config.sh
. "$SCRIPT_DIR/lib/config.sh"
# shellcheck source=lib/probe.sh
. "$SCRIPT_DIR/lib/probe.sh"

usage() {
  sed -n '4,12p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
}

# Parse args
single_device=""
group=""
dry_run=false
while [ $# -gt 0 ]; do
  case "$1" in
    --version) echo "hearth $VERSION"; exit 0;;
    --help|-h) usage;;
    --device)  single_device="$2"; shift 2;;
    --group)   group="$2"; shift 2;;
    --dry-run) dry_run=true; shift;;
    *) echo "Unknown argument: $1" >&2; usage;;
  esac
done

# Find config
config_path=$(hearth_find_config) || {
  echo "ERROR: no devices.yaml found." >&2
  echo "Set HEARTH_CONFIG, or create ~/.hearth/devices.yaml from examples/devices.example.yaml" >&2
  exit 1
}
echo "# config: $config_path" >&2

# Validate parser
parser=$(hearth_detect_yaml_parser) || {
  echo "ERROR: no YAML parser available. Install yq (https://github.com/mikefarah/yq) or python3 with PyYAML." >&2
  exit 1
}
echo "# yaml parser: $parser" >&2

# Build device list
devices=()
if [ -n "$single_device" ]; then
  devices=("$single_device")
elif [ -n "$group" ]; then
  # Read group members
  if [ "$parser" = "python" ]; then
    while IFS= read -r d; do
      devices+=("$d")
    done < <(python3 -c "
import yaml
with open('$config_path') as f:
    d = yaml.safe_load(f)
for name in d.get('groups', {}).get('$group', []):
    print(name)
")
  else
    while IFS= read -r d; do
      devices+=("$d")
    done < <(yq eval ".groups.${group}[]" "$config_path")
  fi
  if [ "${#devices[@]}" -eq 0 ]; then
    echo "ERROR: group '$group' is empty or undefined in $config_path" >&2
    exit 1
  fi
else
  while IFS= read -r d; do
    devices+=("$d")
  done < <(hearth_list_devices "$config_path")
fi

if [ "$dry_run" = "true" ]; then
  echo "# DRY RUN — devices that would be probed:"
  for d in "${devices[@]}"; do
    echo "  - $d"
  done
  exit 0
fi

# Run sweep
device_timeout=$(hearth_get_default "$config_path" "device_timeout" "18")

start=$(date +%s)
hearth_sweep_header ""

for d in "${devices[@]}"; do
  timeout "$device_timeout" "$SCRIPT_DIR/check-device.sh" "$d" 2>&1
  echo ""
done

end=$(date +%s)
hearth_sweep_footer "$((end - start))"