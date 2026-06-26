#!/bin/bash
# hearth/scripts/lib/config.sh — YAML config loading
# Read-only library — sourced by other scripts.

# Locate the user's devices.yaml. Honours $HEARTH_CONFIG, then ~/.hearth/devices.yaml,
# then ./devices.yaml as a last resort.
hearth_find_config() {
  if [ -n "$HEARTH_CONFIG" ] && [ -f "$HEARTH_CONFIG" ]; then
    echo "$HEARTH_CONFIG"
    return 0
  fi
  if [ -f "$HOME/.hearth/devices.yaml" ]; then
    echo "$HOME/.hearth/devices.yaml"
    return 0
  fi
  if [ -f "./devices.yaml" ]; then
    echo "./devices.yaml"
    return 0
  fi
  return 1
}

# Detect available YAML parser. Prefers `yq` (Go), falls back to Python's PyYAML.
# Echoes "yq" or "python" or returns 1 if neither found.
hearth_detect_yaml_parser() {
  if command -v yq >/dev/null 2>&1; then
    # Verify it's mikefarah's yq (Go), not Python yq
    if yq --version 2>&1 | grep -q "mikefarah\|github\.com\|version v[0-9]"; then
      echo "yq"
      return 0
    fi
  fi
  if command -v python3 >/dev/null 2>&1; then
    if python3 -c 'import yaml' 2>/dev/null; then
      echo "python"
      return 0
    fi
  fi
  return 1
}

# Read the list of device names from the config.
# Args: config_path
hearth_list_devices() {
  local cfg="$1"
  local parser
  parser=$(hearth_detect_yaml_parser) || {
    echo "ERROR: no YAML parser available. Install yq or python3-yaml." >&2
    return 1
  }

  case "$parser" in
    yq)
      yq eval '.devices[].name' "$cfg"
      ;;
    python)
      python3 -c "
import yaml, sys
with open('$cfg') as f:
    d = yaml.safe_load(f)
for dev in d.get('devices', []):
    print(dev.get('name', ''))
"
      ;;
  esac
}

# Read a single device's full record as a single line of `key=value` pairs.
# Args: config_path device_name
# Echoes lines like:
#   name=fileserver
#   address=192.0.2.20
#   auth=ssh-pass
#   user=admin
#   ...
hearth_get_device() {
  local cfg="$1"
  local name="$2"
  local parser
  parser=$(hearth_detect_yaml_parser) || return 1

  case "$parser" in
    yq)
      yq eval ".devices[] | select(.name == \"$name\") | to_entries | .[] | .key + \"=\" + (.value | tostring)" "$cfg"
      ;;
    python)
      python3 -c "
import yaml, sys, json
with open('$cfg') as f:
    d = yaml.safe_load(f)
for dev in d.get('devices', []):
    if dev.get('name') == '$name':
        for k, v in dev.items():
            if isinstance(v, (list, dict)):
                print(f'{k}={json.dumps(v)}')
            else:
                print(f'{k}={v}')
        break
"
      ;;
  esac
}

# Read default value for a key from the defaults: section
# Args: config_path key fallback
hearth_get_default() {
  local cfg="$1"
  local key="$2"
  local fallback="$3"
  local parser
  parser=$(hearth_detect_yaml_parser) || { echo "$fallback"; return 0; }

  local val
  case "$parser" in
    yq)
      val=$(yq eval ".defaults.$key // \"\"" "$cfg")
      ;;
    python)
      val=$(python3 -c "
import yaml
with open('$cfg') as f:
    d = yaml.safe_load(f)
print(d.get('defaults', {}).get('$key', ''))
")
      ;;
  esac
  [ -z "$val" ] || [ "$val" = "null" ] && echo "$fallback" || echo "$val"
}