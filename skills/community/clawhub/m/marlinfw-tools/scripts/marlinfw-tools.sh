#!/bin/bash
set -euo pipefail
trap 'log ERROR "command failed exit=$?"' ERR

readonly default_image='psyb0t/marlinfw-tools:latest'
readonly stable_port_prefix='/dev/serial/by-id/'

log() {
    local level="$1"
    shift
    local time file line func message
    time=$(date -u '+%Y-%m-%dT%H:%M:%S.%3NZ')
    file="${BASH_SOURCE[1]##*/}"
    line="${BASH_LINENO[0]}"
    func="${FUNCNAME[1]:-main}"
    message="$*"
    printf '{"time":"%s","level":"%s","file":"%s","line":%s,"func":"%s","msg":"%s"}\n' \
        "$time" "$level" "$file" "$line" "$func" "$message" >&2
}

usage() {
    cat <<'EOF'
Usage:
  marlinfw-tools.sh discover
  marlinfw-tools.sh inspect --port /dev/serial/by-id/<printer> [--baudrate N] [--timeout S]
  marlinfw-tools.sh sd-files --port /dev/serial/by-id/<printer> [--baudrate N] [--timeout S]
  marlinfw-tools.sh record --port /dev/serial/by-id/<printer> \
      [--duration S] [--poll-interval S] [--baudrate N] [--timeout S]
  marlinfw-tools.sh home --port /dev/serial/by-id/<printer> \\
      --apply --confirm-risk --confirm-supervised [--baudrate N] [--timeout S]
  marlinfw-tools.sh sd-print-monitor --port /dev/serial/by-id/<printer> --file NAME \
      --apply --confirm-risk --confirm-supervised [--first-layer-timeout S] \
      [--observe-seconds S] [--poll-interval S] [--baudrate N] [--timeout S]
  marlinfw-tools.sh send --port /dev/serial/by-id/<printer> --command 'M92 E...' \\
      --apply --confirm-risk [--save --confirm-persist]

MARLINFW_TOOLS_IMAGE overrides psyb0t/marlinfw-tools:latest.
Arbitrary G-code is unsupported.
EOF
}

image="${MARLINFW_TOOLS_IMAGE:-$default_image}"

docker_base_args=(
    run
    --rm
    --init
    --network=none
    --read-only
    --cap-drop=ALL
    --security-opt=no-new-privileges:true
    --pids-limit=64
    --memory=128m
    --cpus=0.50
    --tmpfs
    "/tmp:rw,noexec,nosuid,size=16m"
)

require_stable_port() {
    local port="$1"
    local device_name="${port#"$stable_port_prefix"}"
    if [[ "$port" != "$stable_port_prefix"* ]] \
        || [[ -z "$device_name" ]] \
        || [[ "$device_name" == */* ]] \
        || [[ "$device_name" == '.' ]] \
        || [[ "$device_name" == '..' ]]; then
        log ERROR "port must use stable /dev/serial/by-id path"
        exit 2
    fi
}

device_group_id_for_port() {
    local port="$1"
    local host_port="/host-dev/${port#/dev/}"
    local device_group_id
    if ! device_group_id=$(docker "${docker_base_args[@]}" \
        --mount type=bind,source=/dev,target=/host-dev,readonly \
        --entrypoint stat \
        "$image" -Lc '%g' -- "$host_port"); then
        log ERROR "cannot read printer device group port=$port"
        return 2
    fi
    if [[ ! "$device_group_id" =~ ^[0-9]+$ ]]; then
        log ERROR "printer device group is not a numeric GID port=$port"
        return 2
    fi
    printf '%s\n' "$device_group_id"
}

if (($# == 0)); then
    usage >&2
    exit 2
fi

operation="$1"
shift

case "$operation" in
    discover)
        if (($# != 0)); then
            usage >&2
            exit 2
        fi
        log INFO "discovering stable serial ports"
        exec docker "${docker_base_args[@]}" \
            --mount type=bind,source=/dev,target=/host-dev,readonly \
            "$image" ports --device-root /host-dev
        ;;
    inspect | sd-files | record | home | send | sd-print-monitor)
        port=''
        arguments=("$operation")
        while (($# > 0)); do
            case "$1" in
                --port)
                    if (($# < 2)); then
                        log ERROR "--port requires a value"
                        exit 2
                    fi
                    port="$2"
                    arguments+=("$1" "$2")
                    shift 2
                    ;;
                *)
                    arguments+=("$1")
                    shift
                    ;;
            esac
        done
        if [[ -z "$port" ]]; then
            log ERROR "--port is required"
            exit 2
        fi
        require_stable_port "$port"
        if ! device_group_id=$(device_group_id_for_port "$port"); then
            exit 2
        fi
        if [[ "$operation" == 'send' ]] && [[ " ${arguments[*]} " != *' --apply '* ]]; then
            log ERROR "send requires --apply"
            exit 2
        fi
        if [[ "$operation" == 'send' ]] && [[ " ${arguments[*]} " != *' --confirm-risk '* ]]; then
            log ERROR "send requires --confirm-risk after direct user approval"
            exit 2
        fi
        if [[ "$operation" == 'send' ]] && [[ " ${arguments[*]} " == *' --save '* ]] \
            && [[ " ${arguments[*]} " != *' --confirm-persist '* ]]; then
            log ERROR "--save requires --confirm-persist after follow-up inspection"
            exit 2
        fi
        if [[ "$operation" == 'home' ]] && [[ " ${arguments[*]} " != *' --apply '* ]]; then
            log ERROR "home requires --apply"
            exit 2
        fi
        if [[ "$operation" == 'home' ]] && [[ " ${arguments[*]} " != *' --confirm-risk '* ]]; then
            log ERROR "home requires --confirm-risk after direct user approval"
            exit 2
        fi
        if [[ "$operation" == 'home' ]] \
            && [[ " ${arguments[*]} " != *' --confirm-supervised '* ]]; then
            log ERROR "home requires --confirm-supervised with an operator present"
            exit 2
        fi
        if [[ "$operation" == 'sd-print-monitor' ]] \
            && [[ " ${arguments[*]} " != *' --apply '* ]]; then
            log ERROR "sd-print-monitor requires --apply"
            exit 2
        fi
        if [[ "$operation" == 'sd-print-monitor' ]] \
            && [[ " ${arguments[*]} " != *' --confirm-risk '* ]]; then
            log ERROR "sd-print-monitor requires --confirm-risk after direct user approval"
            exit 2
        fi
        if [[ "$operation" == 'sd-print-monitor' ]] \
            && [[ " ${arguments[*]} " != *' --confirm-supervised '* ]]; then
            log ERROR "sd-print-monitor requires --confirm-supervised with an operator present"
            exit 2
        fi
        log INFO "running printer operation"
        exec docker "${docker_base_args[@]}" \
            --group-add "$device_group_id" \
            --device "$port:$port:rwm" \
            "$image" "${arguments[@]}"
        ;;
    help | --help | -h)
        usage
        ;;
    *)
        log ERROR "unsupported operation"
        usage >&2
        exit 2
        ;;
esac
