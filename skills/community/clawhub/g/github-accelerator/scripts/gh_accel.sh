#!/usr/bin/env bash
# gh_accel.sh - GitHub 网络加速工具（直连优先，镜像兜底；仅只读操作）
# 自建/私有加速代理经本地配置文件注入（自动优先于内置镜像），无需改动本脚本：
#   ~/.config/gh-accelerator/proxies.conf   （可用环境变量 GH_ACCEL_CONFIG 覆盖路径）
# 输出语言: GH_ACCEL_LANG=zh（默认，面向 CN 网络用户）或 en
# 依赖: curl, git, sha256sum/shasum。镜像状态易变，用前建议先跑 check。
set -uo pipefail

CONFIG_FILE="${GH_ACCEL_CONFIG:-$HOME/.config/gh-accelerator/proxies.conf}"
LANG_SEL="${GH_ACCEL_LANG:-zh}"

# msg <zh-text> <en-text>
msg() {
  if [ "$LANG_SEL" = "en" ]; then printf '%s\n' "$2"; else printf '%s\n' "$1"; fi
}

# 内置公共镜像梯次（按序自动降级）
DL_PROXIES=(https://ghfast.top https://gh-proxy.com)
CLONE_PROXIES=(
  "https://gitclone.com/github.com"
  "https://gh-proxy.com/https://github.com"
)
TEST_RAW="https://raw.githubusercontent.com/hunshcn/gh-proxy/master/README.md"

# ---------- 本地私有代理加载（排在公共梯次之前） ----------
# 格式（每行一条，# 注释；裸域名自动补 https://）:
#   DOWNLOAD_PROXY=https://your-proxy.example.com
#   CLONE_PROXY=https://your-proxy.example.com/https://github.com
LOCAL_DL=(); LOCAL_CLONE=()
if [ ! -f "$CONFIG_FILE" ]; then
  mkdir -p "$(dirname "$CONFIG_FILE")" 2>/dev/null \
    && cat > "$CONFIG_FILE" <<'TMPL' 2>/dev/null || true
# gh-accelerator 本地私有代理配置（机器本地文件，禁止提交到仓库）
# Local private proxy config. Machine-local; never commit it.
# 每行一条，去掉行首 # 并改成你的代理地址即可生效；会自动排在公共镜像之前。
# One entry per line: uncomment and set your proxy; local entries outrank public mirrors.
# DOWNLOAD_PROXY=https://your-proxy.example.com
# CLONE_PROXY=https://your-proxy.example.com/https://github.com
TMPL
  true
fi
if [ -f "$CONFIG_FILE" ]; then
  while IFS= read -r line; do
    line="${line%%#*}"
    line="${line#"${line%%[![:space:]]*}"}"; line="${line%"${line##*[![:space:]]}"}"
    [ -z "$line" ] && continue
    case "$line" in
      DOWNLOAD_PROXY=*)
        v="${line#DOWNLOAD_PROXY=}"; case "$v" in http*) ;; *) v="https://$v";; esac
        LOCAL_DL+=("$v") ;;
      CLONE_PROXY=*)
        v="${line#CLONE_PROXY=}"; case "$v" in http*) ;; *) v="https://$v";; esac
        LOCAL_CLONE+=("$v") ;;
    esac
  done < "$CONFIG_FILE"
fi
DL_PROXIES=("${LOCAL_DL[@]+"${LOCAL_DL[@]}"}" "${DL_PROXIES[@]}")
CLONE_PROXIES=("${LOCAL_CLONE[@]+"${LOCAL_CLONE[@]}"}" "${CLONE_PROXIES[@]}")

is_local() {
  local u
  for u in "${LOCAL_DL[@]+"${LOCAL_DL[@]}"}" "${LOCAL_CLONE[@]+"${LOCAL_CLONE[@]}"}"; do
    [ "$u" = "$1" ] && return 0
  done
  return 1
}

# 仅接受 GitHub 官方域名的 https URL；拒绝查询串/片段与内嵌凭据，避免令牌经镜像泄露。
github_url_ok() {
  [[ "$1" =~ ^https://[^/@]+@ ]] && return 3
  case "$1" in
    https://github.com/*|\
    https://raw.githubusercontent.com/*|\
    https://gist.githubusercontent.com/*|\
    https://objects.githubusercontent.com/*|\
    https://release-assets.githubusercontent.com/*|\
    https://github-releases.githubusercontent.com/*|\
    https://codeload.github.com/*) ;;
    *) return 1 ;;
  esac
  case "$1" in
    *\?*|*\#*) return 2 ;;
  esac
  return 0
}

sha256_file() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  else
    return 1
  fi
}

usage() {
  msg "用法:" "Usage:"
  msg "  gh_accel.sh check                        探测直连与各镜像可用性" \
      "  gh_accel.sh check                        probe direct links and mirrors"
  msg "  gh_accel.sh dl [--no-direct] [--sha256 H] <github-url>" \
      "  gh_accel.sh dl [--no-direct] [--sha256 H] <github-url>"
  msg "  gh_accel.sh clone [--no-direct] <owner/repo> [dir]" \
      "  gh_accel.sh clone [--no-direct] <owner/repo> [dir]"
  msg "" ""
  msg "仅接受 GitHub 官方域名 URL；目标文件已存在时拒绝覆盖。" \
      "Only official GitHub-host URLs are accepted; existing output files are never overwritten."
  msg "语言: GH_ACCEL_LANG=zh|en（默认 zh）" \
      "Language: GH_ACCEL_LANG=zh|en (default: zh)"
  msg "本地私有代理配置: \$GH_ACCEL_CONFIG（默认 ~/.config/gh-accelerator/proxies.conf）" \
      "Private proxies: \$GH_ACCEL_CONFIG (default: ~/.config/gh-accelerator/proxies.conf)"
  exit 1
}

# fetch <url> <outfile> <max-sec> -> echo http_code (000=失败)
fetch() {
  local code rc
  code=$(curl -sL --max-time "$3" -o "$2" -w '%{http_code}' "$1" 2>/dev/null)
  rc=$?
  [ $rc -ne 0 ] && code=000
  echo "${code:-000}"
}

# probe <url> <max-sec> -> echo http_code (000=失败)；不跟随重定向，2xx/3xx/404 均视为存活
probe() {
  local code
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time "$2" "$1" 2>/dev/null)
  [ $? -ne 0 ] && code="000"
  echo "${code:-000}"
}

cmd_check() {
  echo "本地配置: $CONFIG_FILE ($((${#LOCAL_DL[@]} + ${#LOCAL_CLONE[@]})) 条私有代理)"
  echo "== 直连探测 =="
  for d in "api.github.com/zen" "$TEST_RAW" "codeload.github.com/hunshcn/gh-proxy/tar.gz/master" "github.com/"; do
    code=$(probe "https://$d" 8)
    case "$code" in
      200|301|302|404) echo "  ✓ $d ($code)" ;;
      *)               echo "  ✗ $d ($code)" ;;
    esac
  done
  echo "== 下载镜像（拉测试文件验内容）=="
  for p in "${DL_PROXIES[@]}"; do
    tag=""; is_local "$p" && tag="  [本地]"
    out=$(mktemp)
    code=$(fetch "$p/$TEST_RAW" "$out" 15)
    if [ "$code" = "200" ] && grep -q "gh-proxy" "$out" 2>/dev/null; then
      echo "  ✓ $p$tag"
    else
      echo "  ✗ $p$tag (http=$code)"
    fi
    rm -f "$out"
  done
  echo "== clone 镜像（ls-remote 探测公开仓库）=="
  for base in "${CLONE_PROXIES[@]}"; do
    tag=""; is_local "$base" && tag="  [本地]"
    if timeout 20 git ls-remote "$base/hunshcn/gh-proxy.git" HEAD >/dev/null 2>&1; then
      echo "  ✓ $base$tag"
    else
      echo "  ✗ $base$tag"
    fi
  done
}

cmd_dl() {
  local no_direct=0 expect_sha="" url=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --no-direct) no_direct=1 ;;
      --sha256)
        [ $# -ge 2 ] || usage
        expect_sha="$2"; shift ;;
      -*) usage ;;
      *)
        [ -z "$url" ] || usage
        url="$1" ;;
    esac
    shift
  done
  [ -n "$url" ] || usage

  case "$url" in
    https://*) ;;
    http://*) url="https://${url#http://}" ;;
    *) url="https://$url" ;;
  esac
  github_url_ok "$url"
  case $? in
    1) msg "❌ 仅支持 GitHub 官方域名 URL（github.com / *.githubusercontent.com / codeload.github.com）" \
           "ERROR: only official GitHub-host URLs are supported"; return 1 ;;
    2) msg "❌ 拒绝含查询串/片段的 URL（可能携带令牌）" \
           "ERROR: URLs with query strings or fragments are rejected (possible token leakage)"; return 1 ;;
    3) msg "❌ 拒绝内嵌凭据的 URL" \
           "ERROR: URLs with embedded credentials are rejected"; return 1 ;;
  esac

  local out="$(basename "${url%%\?*}")"
  [ -z "$out" ] && out="download.bin"
  case "$out" in
    -*) msg "❌ 拒绝非安全文件名: $out" "ERROR: unsafe output filename: $out"; return 1 ;;
  esac
  if [ -e "$out" ]; then
    msg "❌ 目标文件已存在，拒绝覆盖: $out（请先移走或改名）" \
        "ERROR: output file already exists, refusing to overwrite: $out"
    return 1
  fi
  local tmp="$(mktemp "./.${out}.XXXXXX")"

  local code got_sha p
  try_channel() {
    code=$(fetch "$1" "$tmp" "$2")
    if [ "$code" = "200" ] && [ -s "$tmp" ]; then
      if [ -n "$expect_sha" ]; then
        got_sha="$(sha256_file "$tmp")" || {
          rm -f "$tmp"
          msg "  ✗ 无法计算 sha256（缺少 sha256sum/shasum）" \
              "  FAIL: cannot compute sha256 (sha256sum/shasum missing)"
          return 1
        }
        if [ "$got_sha" != "$expect_sha" ]; then
          rm -f "$tmp"
          msg "  ✗ sha256 不匹配（期望 ${expect_sha:0:12}…，得到 ${got_sha:0:12}…）" \
              "  FAIL: sha256 mismatch (expected ${expect_sha:0:12}..., got ${got_sha:0:12}...)"
          return 1
        fi
      fi
      mv "$tmp" "$out" || { rm -f "$tmp"; return 1; }
      got_sha="$(sha256_file "$out" 2>/dev/null)" || got_sha="unknown"
      msg "✅ 经 $3 下载成功 -> $out ($(du -h "$out" | cut -f1), sha256=$got_sha)" \
          "OK: downloaded via $3 -> $out ($(du -h "$out" | cut -f1), sha256=$got_sha)"
      [ -z "$expect_sha" ] && msg "⚠️  未提供 --sha256，请自行校验后再使用" \
                                  "WARN: no --sha256 given; verify before use"
      return 0
    fi
    rm -f "$tmp"
    return 1
  }

  if [ $no_direct -eq 0 ]; then
    msg "→ 直连: $url" "-> direct: $url"
    try_channel "$url" 60 "直连/direct" && return 0
    msg "  ✗ 直连失败 (http=$code)，降级镜像…" "  FAIL: direct link (http=$code), falling back to mirrors..."
  fi

  for p in "${DL_PROXIES[@]}"; do
    msg "→ 镜像: $p" "-> mirror: $p"
    try_channel "$p/$url" 90 "$p" && return 0
    msg "  ✗ $p 失败 (http=$code)" "  FAIL: $p (http=$code)"
  done
  rm -f "$tmp"
  msg "❌ 全部通道失败。跑 'gh_accel.sh check' 看镜像状态，或找新镜像更新 DL_PROXIES" \
      "ERROR: all channels failed. Run 'gh_accel.sh check' or update DL_PROXIES"
  return 1
}

cmd_clone() {
  local no_direct=0 repo="" dir="" dir_pre_existed=0
  while [ $# -gt 0 ]; do
    case "$1" in
      --no-direct) no_direct=1 ;;
      -*) usage ;;
      *)
        if [ -z "$repo" ]; then repo="$1"
        elif [ -z "$dir" ]; then dir="$1"
        else usage; fi ;;
    esac
    shift
  done
  [ -n "$repo" ] || usage
  repo="${repo#https://github.com/}"; repo="${repo%.git}"
  case "$repo" in
    */*/*|.*|*..*|*[[:space:]]*|"") msg "❌ 非法仓库标识: $repo（格式 owner/repo）" \
                                       "ERROR: invalid repository id: $repo (expected owner/repo)"; return 1 ;;
  esac
  [ -z "$dir" ] && dir="$(basename "$repo")"
  case "$dir" in
    -*) msg "❌ 拒绝非安全目录名: $dir" "ERROR: unsafe destination directory: $dir"; return 1 ;;
  esac
  if [ -e "$dir" ] && [ -n "$(ls -A "$dir" 2>/dev/null)" ]; then
    msg "❌ 目标目录已存在且非空，拒绝克隆: $dir" \
        "ERROR: destination exists and is not empty, refusing to clone: $dir"
    return 1
  fi
  [ -e "$dir" ] && dir_pre_existed=1

  if [ $no_direct -eq 0 ]; then
    msg "→ 直连: https://github.com/$repo" "-> direct: https://github.com/$repo"
    if git clone "https://github.com/$repo" "$dir"; then
      msg "✅ 直连 clone 成功 -> $dir" "OK: direct clone -> $dir"
      return 0
    fi
    if [ "$dir_pre_existed" -eq 0 ]; then rmdir "$dir" 2>/dev/null || true; fi
    msg "  ✗ 直连失败，降级镜像…" "  FAIL: direct clone, falling back to mirrors..."
  fi

  for base in "${CLONE_PROXIES[@]}"; do
    msg "→ 镜像: $base/$repo" "-> mirror: $base/$repo"
    if git clone "$base/$repo" "$dir"; then
      msg "✅ 经镜像 clone 成功 -> $dir" "OK: mirror clone -> $dir"
      msg "⚠️  remote 指向镜像，push 前执行:" "WARN: remote points to the mirror; before pushing run:"
      msg "   git -C $dir remote set-url origin https://github.com/$repo.git" \
          "   git -C $dir remote set-url origin https://github.com/$repo.git"
      return 0
    fi
    if [ "$dir_pre_existed" -eq 0 ]; then rmdir "$dir" 2>/dev/null || true; fi
    msg "  ✗ 失败" "  FAIL"
  done
  msg "❌ 全部通道失败。跑 'gh_accel.sh check' 探测" "ERROR: all channels failed. Run 'gh_accel.sh check'."
  return 1
}

[ $# -lt 1 ] && usage
case "$1" in
  check) cmd_check ;;
  dl)    [ $# -ge 2 ] || usage; cmd_dl "${@:2}" ;;
  clone) [ $# -ge 2 ] || usage; cmd_clone "${@:2}" ;;
  *)     usage ;;
esac
