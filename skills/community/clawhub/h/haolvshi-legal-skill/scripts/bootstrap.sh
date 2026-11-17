#!/bin/sh
set -eu

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

minimum_major="${HAOLVSHI_NODE_MIN_MAJOR:-${LVPIN_NODE_MIN_MAJOR:-20}}"
release_line="${HAOLVSHI_NODE_RELEASE_LINE:-${LVPIN_NODE_RELEASE_LINE:-22}}"

if [ -n "${HAOLVSHI_RUNTIME_DIR:-}" ]; then
  runtime_root="$HAOLVSHI_RUNTIME_DIR"
elif [ -n "${LVPIN_RUNTIME_DIR:-}" ]; then
  runtime_root="$LVPIN_RUNTIME_DIR"
elif [ -n "${XDG_DATA_HOME:-}" ]; then
  runtime_root="$XDG_DATA_HOME/haolvshi-legal-skill/runtime"
else
  runtime_root="${HOME:?无法确定用户目录}/.local/share/haolvshi-legal-skill/runtime"
fi

if [ -n "${XDG_DATA_HOME:-}" ]; then
  legacy_runtime_root="$XDG_DATA_HOME/lvpin-legal-skill/runtime"
else
  legacy_runtime_root="${HOME:?无法确定用户目录}/.local/share/lvpin-legal-skill/runtime"
fi

node_path_file="$runtime_root/node-path"
legacy_node_path_file="$legacy_runtime_root/node-path"

node_major() {
  "$1" --version 2>/dev/null | sed -E 's/^v([0-9]+).*/\1/'
}

node_compatible() {
  candidate="$1"
  [ -x "$candidate" ] || return 1
  major="$(node_major "$candidate" || true)"
  [ -n "$major" ] && [ "$major" -ge "$minimum_major" ]
}

resolve_node() {
  if [ -n "${HAOLVSHI_NODE_BIN:-}" ] && node_compatible "$HAOLVSHI_NODE_BIN"; then
    printf '%s\n' "$HAOLVSHI_NODE_BIN"
    return 0
  fi

  if [ -n "${LVPIN_NODE_BIN:-}" ] && node_compatible "$LVPIN_NODE_BIN"; then
    printf '%s\n' "$LVPIN_NODE_BIN"
    return 0
  fi

  system_node="$(command -v node 2>/dev/null || true)"
  if [ -n "$system_node" ] && node_compatible "$system_node"; then
    printf '%s\n' "$system_node"
    return 0
  fi

  if [ -f "$node_path_file" ]; then
    cached_node="$(sed -n '1p' "$node_path_file")"
    if node_compatible "$cached_node"; then
      printf '%s\n' "$cached_node"
      return 0
    fi
  fi

  if [ -f "$legacy_node_path_file" ]; then
    cached_node="$(sed -n '1p' "$legacy_node_path_file")"
    if node_compatible "$cached_node"; then
      printf '%s\n' "$cached_node"
      return 0
    fi
  fi

  return 1
}

download_file() {
  source_url="$1"
  target_file="$2"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$source_url" -o "$target_file"
  elif command -v wget >/dev/null 2>&1; then
    wget -q "$source_url" -O "$target_file"
  else
    printf '%s\n' '缺少 curl 或 wget，无法自动下载 Node.js 运行环境。' >&2
    return 1
  fi
}

install_node() {
  os_name="$(uname -s)"
  case "$os_name" in
    Darwin) platform='darwin' ;;
    Linux) platform='linux' ;;
    *)
      printf '当前系统 %s 请改用 scripts/bootstrap.ps1 或手动安装 Node.js %s 以上版本。\n' "$os_name" "$minimum_major" >&2
      return 1
      ;;
  esac

  machine_arch="$(uname -m)"
  case "$machine_arch" in
    x86_64|amd64) node_arch='x64' ;;
    arm64|aarch64) node_arch='arm64' ;;
    *)
      printf '暂不支持自动安装到 %s 架构，请手动安装 Node.js %s 以上版本。\n' "$machine_arch" "$minimum_major" >&2
      return 1
      ;;
  esac

  temporary_dir="$(mktemp -d "${TMPDIR:-/tmp}/haolvshi-node.XXXXXX")"
  trap 'rm -rf "$temporary_dir"' EXIT HUP INT TERM
  manifest="$temporary_dir/SHASUMS256.txt"
  release_url="https://nodejs.org/dist/latest-v${release_line}.x"

  printf '未检测到 Node.js %s 以上版本，正在从 Node.js 官方站点安装独立运行环境。\n' "$minimum_major" >&2
  download_file "$release_url/SHASUMS256.txt" "$manifest"
  suffix="-${platform}-${node_arch}.tar.gz"
  archive_name="$(awk -v suffix="$suffix" 'index($2, suffix) == length($2) - length(suffix) + 1 { print $2; exit }' "$manifest")"
  expected_hash="$(awk -v file="$archive_name" '$2 == file { print $1; exit }' "$manifest")"
  if [ -z "$archive_name" ] || [ -z "$expected_hash" ]; then
    printf '%s\n' 'Node.js 官方清单中没有找到适合当前系统的安装包。' >&2
    return 1
  fi

  archive_path="$temporary_dir/$archive_name"
  download_file "$release_url/$archive_name" "$archive_path"
  if command -v shasum >/dev/null 2>&1; then
    actual_hash="$(shasum -a 256 "$archive_path" | awk '{print $1}')"
  elif command -v sha256sum >/dev/null 2>&1; then
    actual_hash="$(sha256sum "$archive_path" | awk '{print $1}')"
  else
    printf '%s\n' '缺少 SHA-256 校验工具，已停止安装以保护下载完整性。' >&2
    return 1
  fi
  if [ "$actual_hash" != "$expected_hash" ]; then
    printf '%s\n' 'Node.js 安装包校验失败，已停止安装。' >&2
    return 1
  fi

  extract_dir="$temporary_dir/extracted"
  mkdir -p "$extract_dir" "$runtime_root/versions"
  tar -xzf "$archive_path" -C "$extract_dir"
  extracted_name="${archive_name%.tar.gz}"
  install_dir="$runtime_root/versions/$extracted_name"
  if [ ! -d "$install_dir" ]; then
    mv "$extract_dir/$extracted_name" "$install_dir"
  fi
  installed_node="$install_dir/bin/node"
  if ! node_compatible "$installed_node"; then
    printf '%s\n' 'Node.js 运行环境安装后验证失败。' >&2
    return 1
  fi

  path_temp="$runtime_root/node-path.tmp.$$"
  printf '%s\n' "$installed_node" > "$path_temp"
  mv "$path_temp" "$node_path_file"
  printf '%s\n' "$installed_node"
}

installed='false'
if resolved_node="$(resolve_node)"; then
  node_bin="$resolved_node"
else
  node_bin="$(install_node)"
  installed='true'
fi

# 宿主解压技能包时常常丢掉文件权限。等到流程中途报 Permission denied
# 再让模型去补，会白白多出一轮排查和决策。这里在准备环境时一次补齐，
# 补不上也不影响后续流程（脚本一律通过 sh / node 显式调用）。
# 只有这三个是入口，其余 .mjs 是被 import 的模块，不需要执行位。
ensure_executable() {
  chmod +x "$script_dir/run.sh" "$script_dir/bootstrap.sh" "$script_dir/legal-skill.mjs" 2>/dev/null || true
}

# 状态目录同样提前建好，避免第一次写会话状态时才失败。
ensure_state_dir() {
  state_dir="${HAOLVSHI_STATE_DIR:-${LVPIN_STATE_DIR:-${TMPDIR:-/tmp}/haolvshi-legal-skill}}"
  mkdir -p "$state_dir" 2>/dev/null || true
  chmod 700 "$state_dir" 2>/dev/null || true
}

case "${1:---ensure}" in
  --print-node)
    printf '%s\n' "$node_bin"
    ;;
  --ensure|--check)
    ensure_executable
    ensure_state_dir
    version="$($node_bin --version)"
    printf '{"ok":true,"stage":"environment_ready","installed":%s,"nodePath":"%s","nodeVersion":"%s","executableFixed":true,"stateDir":"%s"}\n' \
      "$installed" "$node_bin" "$version" "$state_dir"
    ;;
  *)
    printf '%s\n' '用法：bootstrap.sh [--ensure|--check|--print-node]' >&2
    exit 2
    ;;
esac
