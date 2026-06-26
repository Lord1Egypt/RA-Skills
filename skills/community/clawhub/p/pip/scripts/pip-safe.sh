#!/usr/bin/env bash
set -euo pipefail

usage() {
  local exit_code="${1:-2}"
  cat >&2 <<'EOF'
Usage:
  pip-safe.sh detect
  pip-safe.sh ensure-venv <venv-dir>
  pip-safe.sh install [--venv <venv-dir>] [--upgrade] -- <packages...>
  pip-safe.sh requirements [--venv <venv-dir>] <requirements-file>
  pip-safe.sh uninstall [--venv <venv-dir>] -- <packages...>
  pip-safe.sh freeze [--venv <venv-dir>]

Examples:
  pip-safe.sh detect
  pip-safe.sh ensure-venv .venv
  pip-safe.sh install --venv .venv -- requests pydantic
  pip-safe.sh requirements --venv .venv requirements.txt
  pip-safe.sh uninstall --venv .venv -- requests
  pip-safe.sh freeze --venv .venv > requirements.txt
EOF
  exit "$exit_code"
}

die() {
  echo "pip-safe: $*" >&2
  exit 1
}

find_python() {
  if command -v python3 >/dev/null 2>&1; then
    command -v python3
    return
  fi
  if command -v python >/dev/null 2>&1; then
    command -v python
    return
  fi
  die "python3/python not found on PATH"
}

pip_with_venv() {
  local python_bin="$1"
  local venv_dir="$2"
  shift 2
  if [[ ! -x "$venv_dir/bin/python" ]]; then
    die "venv not found at $venv_dir (missing $venv_dir/bin/python)"
  fi
  "$venv_dir/bin/python" -m pip "$@"
}

pip_with_python() {
  local python_bin="$1"
  shift
  "$python_bin" -m pip "$@"
}

command_name="${1:-}"
if [[ -z "$command_name" || "$command_name" == "-h" || "$command_name" == "--help" ]]; then
  usage 0
fi
shift || true

python_bin="$(find_python)"

case "$command_name" in
  detect)
    pip_cmd=""
    if command -v pip >/dev/null 2>&1; then
      pip_cmd="$(command -v pip)"
    elif command -v pip3 >/dev/null 2>&1; then
      pip_cmd="$(command -v pip3)"
    fi

    echo "python=$python_bin"
    if [[ -n "$pip_cmd" ]]; then
      echo "pip=$pip_cmd"
    else
      echo "pip="
    fi
    "$python_bin" -m pip --version
    ;;

  ensure-venv)
    venv_dir="${1:-}"
    [[ -n "$venv_dir" ]] || usage
    if [[ ! -d "$venv_dir" ]]; then
      "$python_bin" -m venv "$venv_dir"
    fi
    "$venv_dir/bin/python" -m pip install --upgrade pip setuptools wheel
    ;;

  install)
    venv_dir=""
    upgrade="false"
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --venv)
          venv_dir="${2:-}"
          shift 2
          ;;
        --upgrade)
          upgrade="true"
          shift
          ;;
        --)
          shift
          break
          ;;
        *)
          die "unknown arg: $1"
          ;;
      esac
    done
    [[ $# -gt 0 ]] || die "missing packages after --"

    extra=()
    if [[ "$upgrade" == "true" ]]; then
      extra+=(--upgrade)
    fi

    if [[ -n "$venv_dir" ]]; then
      pip_with_venv "$python_bin" "$venv_dir" install "${extra[@]}" "$@"
    else
      pip_with_python "$python_bin" install "${extra[@]}" "$@"
    fi
    ;;

  requirements)
    venv_dir=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --venv)
          venv_dir="${2:-}"
          shift 2
          ;;
        *)
          break
          ;;
      esac
    done

    req_file="${1:-}"
    [[ -n "$req_file" ]] || die "missing requirements file"
    [[ -f "$req_file" ]] || die "requirements file not found: $req_file"

    if [[ -n "$venv_dir" ]]; then
      pip_with_venv "$python_bin" "$venv_dir" install -r "$req_file"
    else
      pip_with_python "$python_bin" install -r "$req_file"
    fi
    ;;

  uninstall)
    venv_dir=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --venv)
          venv_dir="${2:-}"
          shift 2
          ;;
        --)
          shift
          break
          ;;
        *)
          die "unknown arg: $1"
          ;;
      esac
    done
    [[ $# -gt 0 ]] || die "missing packages after --"

    if [[ -n "$venv_dir" ]]; then
      pip_with_venv "$python_bin" "$venv_dir" uninstall -y "$@"
    else
      pip_with_python "$python_bin" uninstall -y "$@"
    fi
    ;;

  freeze)
    venv_dir=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --venv)
          venv_dir="${2:-}"
          shift 2
          ;;
        *)
          die "unknown arg: $1"
          ;;
      esac
    done

    if [[ -n "$venv_dir" ]]; then
      pip_with_venv "$python_bin" "$venv_dir" freeze
    else
      pip_with_python "$python_bin" freeze
    fi
    ;;

  *)
    die "unknown command: $command_name"
    ;;
esac
